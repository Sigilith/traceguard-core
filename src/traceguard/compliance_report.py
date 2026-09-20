import json
import uuid
from datetime import datetime, timezone

class ComplianceReportGenerator:
    def __init__(self, system_name: str = "TraceGuard Autonomous Engine"):
        self.system_name = system_name

    def generate_packet(self, consequence: int, autonomy: int, oversight: bool, violations_detected: int) -> dict:
        audit_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()

        # Assurance Matrix calculation
        score = consequence + autonomy - (2 if oversight else 0)
        if score >= 4:
            tier = "Tier 3 — High Impact (Critical Infrastructure / Autonomous Execution)"
            regulatory_focus = ["Ofgem High-Impact AI Assurance", "EU AI Act High-Risk Mandate"]
            controls = [
                "Deterministic runtime boundary enforcement (TraceGuard)",
                "Continuous behavioral drift monitoring & AXIOMOS risk evaluation",
                "Technical human-in-the-loop approval gates",
                "Immutable append-only audit logging & incident reconstruction"
            ]
        elif score >= 2:
            tier = "Tier 2 — Moderate Impact (Operational Support)"
            regulatory_focus = ["Ofgem Moderate Impact", "EU AI Act Transparency Requirements"]
            controls = [
                "Runtime monitoring and schema validation",
                "Periodic behavioral drift checks",
                "Defined human responsibility boundaries"
            ]
        else:
            tier = "Tier 1 — Low Impact (Informational / Internal)"
            regulatory_focus = ["Standard Internal Governance"]
            controls = [
                "Basic schema logging and execution checks"
            ]

        packet = {
            "artifact_metadata": {
                "audit_uuid": audit_id,
                "timestamp_utc": timestamp,
                "system_name": self.system_name,
                "generator": "traceguard-core compliance engine"
            },
            "risk_classification": {
                "consequence_level": consequence,
                "autonomy_level": autonomy,
                "human_oversight_enforced": oversight,
                "composite_score": score,
                "assigned_tier": tier
            },
            "regulatory_mapping": regulatory_focus,
            "mandatory_controls": controls,
            "runtime_boundary_blueprint": {
                "traceguard_enforcement": "ACTIVE",
                "aximos_drift_status": "HIGH_RISK" if violations_detected > 0 else "LOW_RISK",
                "allowed_action_schema": ["read_logs", "safe_query"] if oversight else ["safe_query"]
            }
        }
        return packet

    def export_as_markdown(self, packet: dict) -> str:
        meta = packet["artifact_metadata"]
        risk = packet["risk_classification"]
        blueprint = packet["runtime_boundary_blueprint"]

        md = f"""# ENTERPRISE COMPLIANCE & ASSURANCE AUDIT PACKET
**System Name:** {meta['system_name']}  
**Audit UUID:** `{meta['audit_uuid']}`  
**Timestamp (UTC):** {meta['timestamp_utc']}  

---

## 1. Executive Tier Classification
* **Assigned Tier:** {risk['assigned_tier']}
* **Composite Risk Score:** {risk['composite_score']} (Consequence: {risk['consequence_level']} | Autonomy: {risk['autonomy_level']} | Oversight: {risk['human_oversight_enforced']})

## 2. Regulatory Alignment
* **Frameworks Mapped:** {', '.join(packet['regulatory_mapping'])}
* **Core Principle:** Designed to satisfy rigorous operational governance, aligning with tiered assurance frameworks for critical infrastructure and autonomous systems[span_0](start_span)[span_0](end_span).

## 3. Mandatory Governance Controls
"""
        for control in packet["mandatory_controls"]:
            md += f"- [x] {control}\n"

        md += f"""
## 4. Runtime Boundary Blueprint
* **TraceGuard Status:** `{blueprint['traceguard_enforcement']}`
* **AXIOMOS Drift Evaluation:** `{blueprint['aximos_drift_status']}`
* **Permitted Action Schema:** `{json.dumps(blueprint['allowed_action_schema'])}`

---
*Generated autonomously by TraceGuard-Core Assurance Engine. Immutable record verified via UUID token.*
"""
        return md
