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
    SF: float
    a: float
    b: float
    solve_I1: bool = True
    fringing: bool = False
    fringe: int = 0
