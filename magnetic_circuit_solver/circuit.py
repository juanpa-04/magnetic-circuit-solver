from dataclasses import dataclass

@dataclass()
class Circuit():
    N1: int
    N2: int
    I1: float
    I2: float
    SC: float
    SL: float
    L1: float
    L2: float
    L3: float
    LE: float
    OE: float
    A: float
    SF: float
    a: float
    b: float
    solve_for_I2: bool = True
    fringe: int = None
