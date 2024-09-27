from prompt_utils import prompt
from prompt_utils import multiple_choice
from number_validator import NumberValidator
import magnetic_utils as magutils
from circuit import Circuit
from solver import Solver

class TUI:
    def __init__(self):
        self.__circuit = None

    def start(self):
       
        self.__init__circuit()
        solver = Solver(circuit=self.__circuit, logging=True)
        print("\n *******Calculo*******\n")
        Oxtuple, Ox2tuple, Ituple = solver.solve()
        print("\n *******Resultados****\n")
        Ox, Ox_name = Oxtuple
        Ox2, Ox2_name = Ox2tuple
        I, I_name = Ituple

        print(f"{Ox_name}: {Ox} Wb")
        print(f"{Ox2_name}: {Ox2} Wb")
        print(f"{I_name}: {I} A")


    def __init__circuit(self):
        
        N1 = prompt("Ingresar N1$ ", NumberValidator((0, None)))
        N2 = prompt("Ingresar N2$ ", NumberValidator((0, None)))
        SL = prompt("Ingresar SL$ ", NumberValidator((0.0, None)))
        SC = prompt("Ingresar SC$ ", NumberValidator((0.0, None)))
        A  = prompt("Ingresar A (ancho/grosor)$ ", NumberValidator((0.0, None)))
        L1 = prompt("Ingresar L1$ ", NumberValidator((0.0, None)))
        L2 = prompt("Ingresar L2$ ", NumberValidator((0.0, None)))
        L3 = prompt("Ingresar L3$ ", NumberValidator((0.0, None)))
        LE = prompt("Ingresar LE$ ", NumberValidator((0.0, None)))
        OE = prompt("Ingresar OE$ ", NumberValidator((None, None)))
        SF = prompt("Ingresar factor de apilado$ ", NumberValidator((0.0,1)))
        I, solve_for_I2 =  self.__ask_current()
        I1 = I if solve_for_I2 else 0
        I2 = 0 if solve_for_I2 else I
        a, b = self.__ask_hb_curve()
        fringe = self.__ask_fringe()

        self.__circuit = Circuit( 
                N1=N1,
                N2=N2,
                I1=I1,
                I2=I2,
                SC=SC,
                SL=SL,
                L1=L1,
                L2=L2,
                L3=L3,
                LE=LE,
                OE=OE,
                SF=SF,
                A=A,
                a=a,
                b=b,
                solve_for_I2=solve_for_I2,
                fringe=fringe
            )
        
    def __ask_fringe(self):
        choice_fringe = ["Ingresar porcentaje de aumento", "Calcular automatico"]
        choice_msg = "Elegir metodo de calculo de dispersión$ "

        choice = multiple_choice(choice_fringe, choice_msg)
        if choice == 1:
            return prompt("Ingresar aumento (%)$ ", NumberValidator((None, None)))
        elif choice == 2:
            return None
        else:
            return None

    def __ask_current(self) -> tuple:
        choice_current = ["I1","I2"]
        choice_msg = "Cual corriente desea ingresar (hacia la bobina es postiva la corriente)$ "
        choice = multiple_choice(choice_current, choice_msg)

        current = None
        solve_for_I2 = True
        if choice == 1:
            current = prompt("Ingresar I1$ ", NumberValidator((None, None)))
        elif choice == 2:
            solve_for_I2 = False
            current = prompt("Ingresar I2$ ", NumberValidator((None, None)))
        else:
            return (None, None)

        return (current, solve_for_I2)

    def __ask_hb_curve(self) -> tuple:
        choices_hb = [
            "Calcular con dos puntos en 25% y 90%",
            "Ingresar directamente a y b"
        ]
        choice_msg = "Como desea calcular curva H-B$ "

        choice = multiple_choice(choices_hb, choice_msg)

        if choice == 1:
            b25 = prompt("Ingresar 25% de valor Bmax$ ", NumberValidator((None, None)))
            h25 = prompt("Ingresar H cuando B = 0.25Bmax$ ", NumberValidator((None, None)))
            b90 = prompt("Ingresar 90% de valor Bmax$ ", NumberValidator((None, None)))
            h90 = prompt("Ingresar H cuando B = 0.90Bmax$ ", NumberValidator((None, None)))
            a, b = magutils.approx_froelich_constants((h25, b25), (h90, b90))
            return (a, b)
        elif choice == 2:
            a = prompt("Ingresar a$ ", NumberValidator((None, None)))
            b = prompt("Ingresar b$ ", NumberValidator((None, None)))
            return (a, b)
        else:
            return (None, None)


if __name__ == "__main__":
    tui = TUI()
    tui.start()