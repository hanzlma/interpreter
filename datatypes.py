from errors import MHscr_ValueError
class String:
    """
    String class for MHscript.
    Strings in MHscript can have either simple or double quotes.
    
    Constructor:
    -----------
        val: str - block of code to be converted to String. Raises ValueError if the conversion fails.
    """
    value: str
    
    def __init__(self, val: str) -> None:
        if val[0] == val[-1] and (val[0] == '"' or val[0] == "'"):
            self.value = val.replace(val[0], '')
        else:
            raise ValueError(f"Value {val} cannot be converted to string")

    def __str__(self) -> str:
        return self.value
class Int:
    """
    Integer class for MHscript.
    
    Constructor:
    -----------
        val: str - block of code to be converted to Int. Raises ValueError if the conversion fails.
    """
    value: int
    
    def __init__(self, val: str) -> None:
        self.value = int(val) # error handling in managing functions (if this function throws, the value is not an integer)
    
    def __str__(self) -> str:
        return str(self.value)
        
class Float:
    """
    Floating point number class for MHscript.
    
    Constructor:
    -----------
        val: str - block of code to be converted to Float. Raises ValueError if the conversion fails.
    """
    value: float
    
    def __init__(self, val:str|float) -> None:
        if isinstance(val, float):
            self.value = val
            pass
        else:
            self.value = float(val)
            if self.value.is_integer() and val.count('.') != 1:
                raise ValueError

    def __str__(self) -> str:
        return str(self.value)
class Bool:
    """
    Boolean class for MHscript.
    
    Constructor:
    -----------
        val: str - block of code to be converted to Bool. Raises ValueError if the conversion fails.
    """
    value: bool
    
    def __init__(self, val:str, _dynamically_called: bool = False) -> None:
        if _dynamically_called and val != 'True' and val!= 'False': 
            raise MHscr_ValueError("Dynamically typed value can only be turned to Bool if it is True or False")
        self.value = bool(val)
    
    def __str__(self) -> str:
        return str(self.value)
class Let:
    """
    Dynamic type class for MHscript.
    
    Constructor:
    -----------
        val: str - block of code to be stored. Raises ValueError if the value cannot be converted to any of the data types.
    """
    def __init__(self, val:str) -> None:
        self.value = GetDatatypeDynamically(val)
    
    def __str__(self) -> str:
        return str(self.value)


def GetDatatypeDynamically(val:str) -> String | Int | Bool | Float:
    try:
        return String(val)
    except ValueError:
        pass
    try:
        return Float(val)
    except ValueError:
        pass
    try:
        return Int(val)
    except ValueError:
        pass
    return Bool(val, _dynamically_called=True)
