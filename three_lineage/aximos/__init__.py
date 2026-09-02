"""ThreeLineage AXIOMOS integration boundary."""

try:
    import axiomos as external_axiomos
except ImportError:
    external_axiomos = None

__all__ = ["external_axiomos"]
