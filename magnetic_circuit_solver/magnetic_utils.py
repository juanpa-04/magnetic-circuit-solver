import constants as cons

def H(B_field: float, a: float, b: float) -> float:
    """Calcula H apartir de B, a, b"""
    H = B_field/(a-b*B_field)
    return H

def H_vacuum(B_field: float, fringing: float = False) -> float:
    """Calcula H en el vacio"""
    H = B_field/cons.PERMEABILITY_VACUUM
    return H

def B(flux: float, cross_section: float, sf: float = 1) -> float:
    """Calcula B"""
    B = flux/(cross_section*sf)
    return B
