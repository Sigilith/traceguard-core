
class TraceGuardBoundaryIntake:
    """
    Receives normalized SIGILITH telemetry and forwards it
    into TraceGuard's boundary kernel for enforcement mapping.
    """

    def __init__(self):
        pass

    def map_observations_to_boundary(self, normalized_packet):
        """
        Converts normalized structural observations into
        boundary-kernel-ready enforcement events.
        """
        events = []

        for obs in normalized_packet.get("normalized_observations", []):
            events.append({
                "file": obs["file"],
                "class_count": obs["structural_markers"]["class_count"],
                "function_count": obs["structural_markers"]["function_count"],
                "boundary_signal": "STRUCTURAL_OBSERVED",
                "status": obs["status"]
            })

        return {
            "source": normalized_packet.get("source"),
            "boundary_events": events
        }
