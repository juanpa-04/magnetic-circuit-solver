"""
Funciones para resolver B, H y calculo de la curva BH
"""
import constants as cons

def H(B_field: float, a: float, b: float) -> float:
    """Calcula H apartir de B, a, b"""
    try:
        return B_field/(a-b*B_field)
    except:
        return 0

def B_curve(H_field: float, a:float, b:float) -> float:
    try:
       return (a*H_field)/(1+b*H_field)
    except:
        return 0


def H_vacuum(B_field: float) -> float:
    """Calcula H en el vacio"""
    try:  
        return B_field/cons.PERMEABILITY_VACUUM
    except:
        return 0

def B_vacuum(flux: float, SC: float, A:float, lg: float, percent_inc: float = None) -> float:
    """Calcula B tomando en cuenta el area efectiva"""

    try:
        w = SC/A # A es el grosor
        effective_area = (w + lg)*(A + lg)
        if percent_inc != None :
            effective_area = (w*A*(1 + percent_inc/100))
        return flux/effective_area
    
    except:
        return 0


def B(flux: float, cross_section: float, sf: float = 1) -> float:
    """Calcula B con el factor de apilado"""
    B = flux/(cross_section*sf)
    return B

def approx_froelich_constants(hb25: tuple, hb90: tuple) -> tuple:
    """Aproxima la curva de un material con dos puntos, 
       uno al 25% y el otro al 90% del valor maximo de B 
    """
    h25, b25 = hb25
    h90, b90 = hb90

    # Resuelve las ecuaciones simultaneas de los dos puntos
    try:
        x = (b25*h25)/(h90*b90)

        a = (b25-x*b90)/(h25 - x*h90)
        b = (a*h90 - b90)/(h90*b90)
    except:
        return (0,0)

    return (a, b)


