import constants as cons

def H(B_field: float, a: float, b: float) -> float:
    """Calcula H apartir de B, a, b"""
    H = B_field/(a-b*B_field)
    return H

def B_curve(H_field: float, a:float, b:float) -> float:
    B = (a*H_field)/(1+b*H_field)
    return B

def H_vacuum(B_field: float) -> float:
    """Calcula H en el vacio"""
    H = B_field/cons.PERMEABILITY_VACUUM
    return H

def B_vacuum(flux: float, w: float, d:float, lg: float, percent_inc: float = None) -> float:
    """Calcula B tomando en cuenta el area efectiva"""

    effective_area = (w + lg)*(d + lg)
    if(percent_inc):
        effective_area = (w*d*(1 + percent_inc/100))
    
    
    return flux/effective_area


def B(flux: float, cross_section: float, sf: float = 1) -> float:
    """Calcula B"""
    B = flux/(cross_section*sf)
    return B

def approx_froelich_constants(hb25: tuple, hb90: tuple) -> tuple:
    """Aproxima la curva de un material con dos puntos, 
       uno al 25% y el otro al 90% del valor maximo de B 
    """
    h25, b25 = hb25
    h90, b90 = hb90

    x = (b25*h25)/(h90*b90)

    a = (b25-x*b90)/(h25 - x*h90)
    b = (a*h90 - b90)/(h90*b90)

    return (a, b)


