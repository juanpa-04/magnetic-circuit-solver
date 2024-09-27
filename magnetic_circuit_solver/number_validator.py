class NumberValidator:
    def __init__(self, range:tuple) -> None:
        self.__range = range


    @property 
    def range(self) -> tuple:
        return self.__range

    def validate(self, userinput: str) -> bool:
        
        userinput = self.convert(userinput)
        if userinput == None:
            return False
       
        if self.__is_in_range(userinput) and self.__is_valid_type(userinput):
            return True
        
        return False
    
    def convert(self, userinput):
        try:
            return int(userinput)
        except:
            try:
                return float(userinput)
            except:
                return None
    
    def __is_in_range(self, userinput) -> bool:
        min, max = self.__range

        valid = False
        if min == None and max == None:
            valid = True
        elif min == None:
            if userinput <= max:
                valid = True
        elif max == None:
            if userinput >= min:
                valid = True
        else:
            if userinput <= max and userinput >= min:
                valid = True
        
        return valid

    def __is_valid_type(self, userinput) -> bool:

        min, max = self.__range

        minmax = min if min != None else max
        if not minmax:
            return True

        isint = isinstance(minmax, int)
        if isint and isinstance(userinput, int):
           return True
        elif not isint and isinstance(userinput, float):
           return True

        return False