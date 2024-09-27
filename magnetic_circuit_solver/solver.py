from circuit import Circuit
import magnetic_utils as magutils

class Solver:

    def __init__(self, circuit: Circuit, logging: bool) -> None:
        self.__circuit = circuit
        self.__logging = logging # Imprime todos los pasos intermedios si es True
        self.__log_line_number = 1 

    def solve(self) -> float:
        
        # Calcular La Fmm de la columna central
        Bc = self.__find_flux(self.__circuit.OE, self.__circuit.SC, self.__circuit.SF, "Bc") # Densidad de flujo de la columna
        Hc = self.__find_mag_intensity(Bc,"Hc") # Intensidad magnetica de la columna
        Be = self.__find_flux_vacuum(self.__circuit.OE, "Be", self.__circuit.fringe) # B del entrehierro
        He = self.__find_mag_intensity(Be, name="He", vacuum=True) # H del entrehierro
        Fmm_ce = self.__find_fmm_column(Hc, He, "Fce") # FMM que "cae" en la columna central y entrehierro

        # Calcular Hx y Bx
        Hx = self.__find_Hx(Fmm_ce) # Calcula el H correspondiente (de la rama 1 o 2)

        bx_name = "B1" if self.__circuit.solve_for_I2 else "B2"
        Bx = self.__find_flux_curve(Hx, bx_name) # Calcula el B correspondiente (de la rama 1 o 2)

        # Calcular flujos en las ramas
        Oxtuple, Ox2tuple = self.__calc_branch_flux(Bx) # Calcula los flujos O1 y O2

        Ox2, _ = Ox2tuple

        # Calcular Corriente
        Ituple = self.__solve__current(Ox2, Fmm_ce) # Resuelve para la corriente faltante


        return (Oxtuple, Ox2tuple, Ituple) # Respuesta
    

    def __solve__current(self, Ox2: float, fmm_ce: float):

        Bx_name = "B1"
        Hx_name = "H1"

        if(self.__circuit.solve_for_I2):
            Bx_name = "B2"
            Hx_name = "H2"


        Bx2 = self.__find_flux(Ox2, self.__circuit.SL, self.__circuit.SF, Bx_name)
        Hx2 = self.__find_mag_intensity(Bx2, Hx_name)
        return self.__find_missing_current(Hx2, fmm_ce)


    def __calc_branch_flux(self, Bx: float) -> tuple:
        Ox = Bx * self.__circuit.SL * self.__circuit.SF
        Ox2 = self.__circuit.OE - Ox
        
        Ox_name = "O1" if self.__circuit.solve_for_I2 else "O2"
        Ox2_name = "O2" if self.__circuit.solve_for_I2 else "O1"

        if(self.__logging):
            self.__log(Ox_name, Ox, "Wb")
            self.__log(Ox2_name, Ox2, "Wb")

        return ((Ox, Ox_name), ((Ox2, Ox2_name)))

    def __find_missing_current(self, Hx2: float, fmm_ce: float) -> float:
        N = self.__circuit.N1
        L = self.__circuit.L1
        name = "I1"

        if(self.__circuit.solve_for_I2):
            N = self.__circuit.N2
            L = self.__circuit.L2
            name = "I2"

        I = (Hx2 * L + fmm_ce)/N
        
        if(self.__logging):
            self.__log(name, I, "A")
        return (I, name)


    def __find_Hx(self, fmm_ce: float) -> float:
        
        I = self.__circuit.I2
        N = self.__circuit.N2
        L = self.__circuit.L2
        name = "H2"

        if(self.__circuit.solve_for_I2):
            I = self.__circuit.I1
            N = self.__circuit.N1
            L = self.__circuit.L1
            name = "H1"
    
        H = (N*I-fmm_ce)/L

        if(self.__logging):
            self.__log(name, H, "A/M")

        return H
    
    def __find_flux_vacuum(self, flux: float, name: str, percent_inc: float = None):
        
        SC = self.__circuit.SC
        A = self.__circuit.A
        lg = self.__circuit.LE

        B = magutils.B_vacuum(flux, SC, A, lg, percent_inc)
        if(self.__logging):
            self.__log(name, B, "Teslas")
        return B

    def __find_flux(self, flux: float, cross: float, sf:float, name:str) -> float:
        B = magutils.B(flux, cross, sf)
        if(self.__logging):
            self.__log(name, B, "Teslas")
        return B
    
    def __find_flux_curve(self, H_field:float, name:str) -> float:
        B = magutils.B_curve(H_field, self.__circuit.a, self.__circuit.b)
        if(self.__logging):
             self.__log(name, B, "Teslas")
        return B

    def __find_mag_intensity(self, B_field: float, name:str = "", vacuum = False) -> float:
        H = magutils.H_vacuum(B_field) if vacuum else \
        magutils.H(B_field, self.__circuit.a, self.__circuit.b)

        if(self.__logging):
            self.__log(name, H, "A/M")   
        return H
    
    def __find_fmm_column(self, hc: float, he: float, name:str) -> float:
        Lc = self.__circuit.L3 - self.__circuit.LE # Longitud media de columna central
        Fce = hc*Lc + he*self.__circuit.LE
        if(self.__logging):
              self.__log("Fce", Fce, "A*t")
        return Fce

    def __log(self, name: str, value, units: str) -> None:
        print(f"[{self.__log_line_number}] {name} {value:.4f} {units}")
        self.__log_line_number += 1
    
        

if __name__ == "__main__":
    """Ejemplos de funcionalidad"""
    circuit = Circuit( 
        N1=100,
        N2=50,
        I1=0,
        I2=37.8,
        SC=0.02,
        SL=0.01,
        L1=1.10,
        L2=1.10,
        L3=0.30,
        LE=0.002,
        OE=0.02,
        SF=0.97,
        a=0.0123,
        b=0.00797,
        A=5e-2,
        fringe=None,
        solve_for_I2=False
    )


    circuit2 = Circuit( 
        N1=360,
        N2=360,
        I1=11.32,
        I2=0,
        SC=50e-4,
        SL=25e-4,
        L1=0.65,
        L2=0.65,
        L3=0.30,
        LE=0.005,
        OE=5e-3,
        SF=1,
        a=0.03,
        b=0.02,
        solve_for_I2=True,
        fringe=10,
        A=5e-2
    )


    solver = Solver(circuit2, logging=True)
    print(solver.solve())