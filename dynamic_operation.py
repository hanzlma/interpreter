from datatypes import String, Int, Float, Bool
from errors import MHscr_ValueError
from operators import operators
from helper import DynamicListContainsDatatype

class DynamicCalculator:
    """Dynamic Calculator."""
    value: String | Int | Float | Bool
    def CalculateDynamicOperations(self, arguments: list[String | Int | Float | Bool], ops: list[str]) -> String | Int | Float | Bool:
        if isinstance(arguments[0], String) and (ops.count(operators['minus']) > 0 or ops.count(operators['multiply']) > 0 or ops.count(operators['divide']) > 0 ):
            raise MHscr_ValueError("Strings can only be summed")
        if (not isinstance(arguments[0], String)) and DynamicListContainsDatatype(arguments, String):
            raise MHscr_ValueError('String can only be used with other datatypes if it is the first type in the operation')
    
        for i in range(len(arguments)):
            if i == 0:
                self.value = arguments[0]
            else: 
                match ops[i-1]:
                    case '+':
                        self.Sum(arguments[i])
                        pass
                    case '-':
                        pass
                    case '*':
                        pass
                    case '/':
                        pass
                    case '&&':
                        pass
                    case '||':
                        pass
                
                    case _:
                        raise MHscr_ValueError(f"Unsupported operator {ops[i-1]}")
        
        return self.value
    
    def Sum(self, argument: String | Int | Float):
        T: type = type(self.value)
        type_argument: type = type(argument)
        if type_argument is T:
            
            self.value = T(self.value.value + argument.value)
        elif T is String:
            self.value = T(f"'{self.value.value + str(argument.value)}'")
        elif (T is Int and type_argument is Float) or (T is Float and type_argument is Int):
            self.value = Float(self.value.value + argument.value)
        else:
            raise MHscr_ValueError(f"Unsupported operation: {self.value}<{T}> + {argument}<{type_argument}>")
            