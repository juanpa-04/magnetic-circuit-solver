from dataclasses import dataclass

@dataclass()
class Circuit():
    """Conjunto de datos y opciones que representan el circuito"""
    N1: int
    N2: int
    I1: float
    I2: float
    SC: float
    SL: float
    L1: float # Es la longitud media de todo la parte izquierda del circuito (igual que ejemplo)
    L2: float # Es la longitud media de todo la parte derecha del circuito
    L3: float
    LE: float
    OE: float
    A: float # Es el grosor del circuito no la altura (SC=A*W donde)
    SF: float # Factor de apilado
    a: float
    b: float
    solve_for_I2: bool = True # Opción para resolver I1 o I2
    fringe: int = None # Si la opcion queda en None el circuito la calcula auto
