import os
import json
import fcntl
import hashlib
import shutil
import time
import uuid
import math
import re

class LedgerIntegrityError(Exception):
    pass

class IncompleteTailError(Exception):
    pass

class AppendOnlyLedgerWriter:
    def __init__(self, output_path="~/.three-lineage/ledger.json"):
        self.output_path = os.path.expanduser(output_path)
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        self._directory_synced = False

    def _compute_hash(self, payload_dict, prev_hash):
        payload = {k: v for k, v in payload_dict.items() if k != "record_hash"}
        payload["prev_hash"] = prev_hash
        serialized = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def _is_valid_hex_hash(self, value):
        if type(value) is not str or len(value) != 64:
            return False
        return bool(re.fullmatch(r"[0-9a-fA-F]{64}", value))

    def _validate_record_schema(self, record, require_ledger_fields=False):
        if type(record) is not dict:
            return False, "Record must be a JSON object"
        
        base_required = {"invocation_id", "action_id", "phase", "timestamp"}
        if not base_required.issubset(record.keys()):
            return False, "Missing required base fields"
            
        if type(record["invocation_id"]) is not str or not record["invocation_id"].strip():
            return False, "Invalid invocation_id type or value"
            
        if type(record["action_id"]) is not str or not record["action_id"].strip():
            return False, "Invalid action_id type or value"
            
        phase = record.get("phase")
        if type(phase) is not str:
            return False, "Phase must be a string"

        allowed_phases = {
            "BLOCKED_PRE_EXECUTION",
            "PRE_EXECUTION_APPROVED",
            "EXECUTION_STARTED",
            "EXECUTION_SUCCESS",
            "EXECUTION_FAILED_AFTER_START",
            "COMPLETION_RECORDING_FAILED"
        }
        if phase not in allowed_phases:
            return False, f"Unknown or disallowed phase: {phase}"
            
        ts = record["timestamp"]
        if type(ts) not in (int, float) or not math.isfinite(ts):
            return False, "Invalid timestamp"

        if require_ledger_fields:
            ledger_required = {"sequence_number", "prev_hash", "record_hash"}
            if not ledger_required.issubset(record.keys()):
                return False, "Missing required ledger-owned fields"

            seq = record["sequence_number"]
            if type(seq) is not int or seq < 1:
                return False, "Invalid sequence_number"

            if not self._is_valid_hex_hash(record["prev_hash"]):
                return False, "Invalid prev_hash hex format"

            if not self._is_valid_hex_hash(record["record_hash"]):
                return False, "Invalid record_hash hex format"
                
        return True, None

    def _sync_containing_directory(self):
        dir_path = os.path.dirname(os.path.abspath(self.output_path))
        dir_fd = os.open(dir_path, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
            self._directory_synced = True
        finally:
            os.close(dir_fd)

    def _derive_invocation_states(self, records):
        states = {}
        action_map = {}
        for r in records:
            inv = r["invocation_id"]
            phase = r["phase"]
            action_map[inv] = r["action_id"]
            states[inv] = phase
        unresolved = {inv for inv, phase in states.items() if phase == "EXECUTION_STARTED"}
        return states, action_map, unresolved

    def _validate_lifecycle_transition(self, new_record, records):
        states, action_map, _ = self._derive_invocation_states(records)
        inv = new_record["invocation_id"]
        phase = new_record["phase"]
        action_id = new_record["action_id"]
        current_phase = states.get(inv)

        if phase in ("BLOCKED_PRE_EXECUTION", "PRE_EXECUTION_APPROVED"):
            if current_phase is not None:
                return False, f"Invocation ID {inv} already exists (reused ID)"
            return True, None
        elif phase == "EXECUTION_STARTED":
            if current_phase != "PRE_EXECUTION_APPROVED":
                return False, f"EXECUTION_STARTED without valid PRE_EXECUTION_APPROVED for {inv}"
            if action_map.get(inv) != action_id:
                return False, f"Action ID mismatch for invocation {inv}"
            return True, None
        elif phase in ("EXECUTION_SUCCESS", "EXECUTION_FAILED_AFTER_START", "COMPLETION_RECORDING_FAILED"):
            if current_phase != "EXECUTION_STARTED":
                return False, f"Terminal phase {phase} without active EXECUTION_STARTED for {inv}"
            if action_map.get(inv) != action_id:
                return False, f"Action ID mismatch for invocation {inv}"
            return True, None
        return False, f"Unknown phase transition: {phase}"

    def _scan_structural_content(self, raw_content):
        if not raw_content:
            return {"status": "VALID", "records": [], "last_valid_byte_offset": 0, "incomplete_bytes": b""}

        lines = raw_content.splitlines(keepends=True)
        valid_records = []
        prev_hash = "0" * 64
        expected_seq = 1
        current_byte_offset = 0

        for i, line_bytes in enumerate(lines):
            is_last = (i == len(lines) - 1)
            
            if not line_bytes.endswith(b"\n"):
                if is_last:
                    return {
                        "status": "INCOMPLETE_TAIL",
                        "records": valid_records,
                        "last_valid_byte_offset": current_byte_offset,
                        "incomplete_bytes": line_bytes
                    }
                else:
                    return {"status": "CORRUPTED", "error": f"Missing newline at line {i+1}"}

            try:
                decoded_str = line_bytes.decode("utf-8").strip()
                if not decoded_str:
                    current_byte_offset += len(line_bytes)
                    continue
                record = json.loads(decoded_str)
            except Exception:
                return {"status": "CORRUPTED", "error": f"Invalid JSON at line {i+1}"}

            expected_hash = self._compute_hash(record, prev_hash)
            if record.get("record_hash") != expected_hash:
                return {"status": "HASH_MISMATCH", "error": f"Record hash mismatch at line {i+1}"}

            is_valid, err_msg = self._validate_record_schema(record, require_ledger_fields=True)
            if not is_valid:
                return {"status": "CORRUPTED", "error": f"Schema violation at line {i+1}: {err_msg}"}

            if record["sequence_number"] != expected_seq:
                return {"status": "SEQUENCE_GAP", "error": f"Sequence gap at line {i+1}: expected {expected_seq}, got {record['sequence_number']}"}

            if record["prev_hash"] != prev_hash:
                return {"status": "HASH_MISMATCH", "error": f"Previous hash mismatch at line {i+1}"}

            trans_valid, trans_err = self._validate_lifecycle_transition(record, valid_records)
            if not trans_valid:
                return {"status": "CORRUPTED", "error": f"Lifecycle transition violation at line {i+1}: {trans_err}"}

            prev_hash = record["record_hash"]
            expected_seq += 1
            valid_records.append(record)
            current_byte_offset += len(line_bytes)

        return {"status": "VALID", "records": valid_records, "last_valid_byte_offset": current_byte_offset, "incomplete_bytes": b""}

    def scan_integrity(self):
        file_existed = os.path.exists(self.output_path)
        fd = os.open(self.output_path, os.O_RDWR | os.O_CREAT, 0o600)
        try:
            with os.fdopen(fd, "r+b") as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                raw_content = f.read()
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            if not file_existed and not raw_content and not self._directory_synced:
                self._sync_containing_directory()
            
            struct_scan = self._scan_structural_content(raw_content)
            if struct_scan["status"] != "VALID":
                return struct_scan

            _, _, unresolved = self._derive_invocation_states(struct_scan["records"])
            struct_scan["unresolved_invocations"] = list(unresolved)
            return struct_scan
        except Exception:
            try:
                os.close(fd)
            except Exception:
                pass
            return {"status": "CORRUPTED", "error": "Failed to read or lock ledger file"}

    def write_entry(self, entry_data):
        is_valid, err_msg = self._validate_record_schema(entry_data, require_ledger_fields=False)
        if not is_valid:
            return False

        try:
            fd = os.open(self.output_path, os.O_RDWR | os.O_CREAT, 0o600)
            with os.fdopen(fd, "r+b") as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                raw_content = f.read()
                
                scan = self._scan_structural_content(raw_content)
                if scan["status"] != "VALID":
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                    return False

                records = scan["records"]

                temp_entry = entry_data.copy()
                seq = records[-1]["sequence_number"] + 1 if records else 1
                prev_h = records[-1]["record_hash"] if records else "0" * 64
                temp_entry["sequence_number"] = seq
                temp_entry["prev_hash"] = prev_h
                temp_entry["record_hash"] = self._compute_hash(temp_entry, prev_h)

                transition_valid, _ = self._validate_lifecycle_transition(temp_entry, records)
                if not transition_valid:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                    return False

                entry_data.update(temp_entry)
                is_complete_valid, _ = self._validate_record_schema(entry_data, require_ledger_fields=True)
                if not is_complete_valid:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                    return False

                serialized = json.dumps(entry_data) + "\n"
                f.seek(0, os.SEEK_END)
                f.write(serialized.encode("utf-8"))
                f.flush()
                os.fsync(f.fileno())
                
                if not self._directory_synced:
                    self._sync_containing_directory()

                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            return True
        except Exception:
            return False

    def reserve_execution(self, invocation_id, action_id, posture):
        try:
            fd = os.open(self.output_path, os.O_RDWR | os.O_CREAT, 0o600)
            with os.fdopen(fd, "r+b") as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                raw_content = f.read()
                
                scan = self._scan_structural_content(raw_content)
                status = scan["status"]
                
                if status in ["CORRUPTED", "SEQUENCE_GAP", "HASH_MISMATCH", "INCOMPLETE_TAIL"]:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                    return False, f"Ledger structural health failure: {status}"

                records = scan["records"]
                _, _, unresolved = self._derive_invocation_states(records)
                if unresolved:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                    return False, f"Unresolved execution intent: {unresolved}"

                seq = records[-1]["sequence_number"] + 1 if records else 1
                prev_h = records[-1]["record_hash"] if records else "0" * 64
                
                pre_exec = {
                    "invocation_id": invocation_id,
                    "action_id": action_id,
                    "phase": "PRE_EXECUTION_APPROVED",
                    "posture": posture,
                    "timestamp": time.time(),
                    "sequence_number": seq,
                    "prev_hash": prev_h
                }
                pre_exec["record_hash"] = self._compute_hash(pre_exec, prev_h)

                t_valid, t_err = self._validate_lifecycle_transition(pre_exec, records)
                if not t_valid:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                    return False, f"Invalid pre-exec lifecycle transition: {t_err}"

                seq2 = seq + 1
                prev_h2 = pre_exec["record_hash"]
                start_rec = {
                    "invocation_id": invocation_id,
                    "action_id": action_id,
                    "phase": "EXECUTION_STARTED",
                    "timestamp": time.time(),
                    "sequence_number": seq2,
                    "prev_hash": prev_h2
                }
                start_rec["record_hash"] = self._compute_hash(start_rec, prev_h2)

                temp_records = records + [pre_exec]
                t_valid2, t_err2 = self._validate_lifecycle_transition(start_rec, temp_records)
                if not t_valid2:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                    return False, f"Invalid start lifecycle transition: {t_err2}"

                for rec in (pre_exec, start_rec):
                    valid, reason = self._validate_record_schema(rec, require_ledger_fields=True)
                    if not valid:
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                        return False, f"Reservation schema validation failed: {reason}"

                serialized = json.dumps(pre_exec) + "\n" + json.dumps(start_rec) + "\n"
                
                f.seek(0, os.SEEK_END)
                f.write(serialized.encode("utf-8"))
                f.flush()
                os.fsync(f.fileno())

                if not self._directory_synced:
                    self._sync_containing_directory()

                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            return True, None
        except Exception as e:
            return False, str(e)

    def explicit_recover_tail(self):
        if not os.path.exists(self.output_path):
            return False

        fd = os.open(self.output_path, os.O_RDWR | os.O_CREAT, 0o600)
        try:
            with os.fdopen(fd, "r+b") as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                raw_content = f.read()
                
                scan = self._scan_structural_content(raw_content)
                if scan["status"] != "INCOMPLETE_TAIL":
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                    return False

                backup_path = f"{self.output_path}.bak.{time.time_ns()}.{uuid.uuid4().hex[:8]}"
                with open(backup_path, "wb") as bf:
                    bf.write(raw_content)
                    bf.flush()
                    os.fsync(bf.fileno())
                self._sync_containing_directory()

                f.seek(scan["last_valid_byte_offset"])
                f.truncate()
                f.flush()
                os.fsync(f.fileno())
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            return True
        except Exception:
            return False
