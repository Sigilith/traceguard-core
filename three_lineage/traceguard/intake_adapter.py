
class TraceGuardIntakeAdapter:
    """
    Intake adapter between SIGILITH Observer and TraceGuard Boundary Kernel.
    Converts structural telemetry into enforcement-ready observation packets.
    """

    def __init__(self):
        pass

    def ingest_sigilith_telemetry(self, telemetry_packet):
        """
        Normalizes SIGILITH telemetry into TraceGuard's expected intake format.
        """
        normalized = []

        for entry in telemetry_packet.get("telemetry", []):
            normalized.append({
                "file": entry.get("file"),
                "structural_markers": {
                    "class_count": entry.get("classes", 0),
                    "function_count": entry.get("functions", 0),
                },
                "status": "OBSERVED"
            })

        return {
            "source": telemetry_packet.get("source"),
            "normalized_observations": normalized
        }
