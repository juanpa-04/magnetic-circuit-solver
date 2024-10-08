from number_validator import NumberValidator


def prompt(message:str, validator: NumberValidator):
    """
    Espera datos del usuaria y validan que sean números.
    En el caso de ser invalidos el programa sigue preguntando
    hasta que sean validos.
    """
    loop = True
    while(loop):
        userinput = input(message)
        if validator.validate(userinput):
            loop = False
        else:
            print("Error: Rango o dato inválido")

    return validator.convert(userinput)

def multiple_choice(choices: list, choose_msg: str):
    """
    Imprime todas las opciones de choices y solo deja escoger alguna de ellas.
    """
    print("Opciones (ingresar número de opción):")
    max = len(choices)
    for i, choice in enumerate(choices):
        print(f"[{i + 1}] {choice}")
    
    return prompt(choose_msg, NumberValidator((1, max)))
   


    

    
