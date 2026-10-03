import os
import json
import time
import uuid

class GovernanceDeniedError(Exception):
    """Raised when the governance gate denies execution."""
    pass

class CompletionRecordingError(Exception):
    """Raised when an action completed successfully, but outcome recording failed. Do not automatically retry."""
    pass

class PostureArbitrationEngine:
    def __init__(self):
        self.posture_precedence = ["BLACK_ABORT", "DEFENSIVE_BUFFER", "GREEN_NOMINAL"]

    def arbitrate(self, votes):
        if not isinstance(votes, list) or not votes:
            raise GovernanceDeniedError("DENIED: Vote set is empty or malformed.")
        
        valid_set = {"GREEN_NOMINAL", "DEFENSIVE_BUFFER", "BLACK_ABORT"}
        cleaned_votes = []
        for v in votes:
            if v not in valid_set:
                raise GovernanceDeniedError(f"DENIED: Unknown vote token: {v}")
            cleaned_votes.append(v)
            
        if "BLACK_ABORT" in cleaned_votes:
            return "BLACK_ABORT"
            
        counts = {p: cleaned_votes.count(p) for p in valid_set if p != "BLACK_ABORT"}
        max_votes = max(counts.values())
        
        top_contenders = [p for p in self.posture_precedence if counts.get(p, 0) == max_votes]
        return top_contenders[0]

class SovereignExecutionGate:
    def __init__(self, ledger_writer, arbiter):
        self.ledger_writer = ledger_writer
        self.arbiter = arbiter

    def execute_governed_action(self, action_id, votes, action_callback, *args, **kwargs):
        invocation_id = str(uuid.uuid4())
        posture = "UNKNOWN"
        callback_started = False
        execution_completed = False
        
        try:
            posture = self.arbiter.arbitrate(votes)
            
            if posture == "BLACK_ABORT":
                raise GovernanceDeniedError(f"DENIED: Absolute Veto triggered for action '{action_id}'.")
            
            if posture == "DEFENSIVE_BUFFER":
                raise GovernanceDeniedError(f"DENIED: Posture 'DEFENSIVE_BUFFER' requires active restrictions; execution prohibited.")
            
            reserved, err_msg = self.ledger_writer.reserve_execution(invocation_id, action_id, posture)
            if reserved is not True:
                if "INCOMPLETE_TAIL" in err_msg or "Incomplete" in err_msg:
                    raise GovernanceDeniedError("Incomplete ledger tail detected.")
                elif "health failure" in err_msg or "SEQUENCE_GAP" in err_msg or "HASH_MISMATCH" in err_msg or "CORRUPTED" in err_msg:
                    raise GovernanceDeniedError(f"Ledger integrity failure: {err_msg}")
                elif "Unresolved" in err_msg:
                    raise GovernanceDeniedError(f"Unresolved execution intent: {err_msg}")
                else:
                    raise GovernanceDeniedError(f"DENIED: Execution reservation failed: {err_msg}")

            callback_started = True
            result = action_callback(*args, **kwargs)
            execution_completed = True

            success_record = {
                "invocation_id": invocation_id,
                "action_id": action_id,
                "phase": "EXECUTION_SUCCESS",
                "timestamp": time.time()
            }
            if self.ledger_writer.write_entry(success_record) is not True:
                raise CompletionRecordingError("Action completed; completion logging failed. Do not automatically retry.")

            return result

        except Exception as e:
            if execution_completed:
                fail_phase = "COMPLETION_RECORDING_FAILED"
            elif callback_started:
                fail_phase = "EXECUTION_FAILED_AFTER_START"
            else:
                fail_phase = "BLOCKED_PRE_EXECUTION"

            fail_record = {
                "invocation_id": invocation_id,
                "action_id": action_id,
                "phase": fail_phase,
                "error": str(e),
                "timestamp": time.time()
            }
            try:
                self.ledger_writer.write_entry(fail_record)
            except Exception:
                pass
            
            if execution_completed:
                raise CompletionRecordingError(
                    "Action completed; completion logging failed. "
                    "Do not automatically retry."
                ) from e

            if isinstance(e, GovernanceDeniedError):
                raise e

            if not callback_started:
                raise GovernanceDeniedError(f"Execution blocked by Sovereign Gate: {e}") from e

            raise GovernanceDeniedError(f"Action failed after starting under posture '{posture}': {e}") from e
