from datatypes import String, Int, Float, Bool
from errors import MHscr_ValueError, MHscr_TypeError, MHscr_OperatorError
from operators import operators
from helper import DynamicListContainsDatatype

class DynamicCalculator:
    """Dynamic Calculator static class"""

    def CalculateDynamicOperations(arguments: list[String | Int | Float | Bool], ops: list[str]) -> String | Int | Float | Bool:
        if isinstance(arguments[0], String) and (ops.count(operators['minus']) > 0 or ops.count(operators['multiply']) > 0 or ops.count(operators['divide']) > 0 ):
            raise MHscr_TypeError("Strings can only be summed")
        if (not isinstance(arguments[0], String)) and DynamicListContainsDatatype(arguments, String):
            raise MHscr_TypeError('String can only be used with other datatypes if it is the first type in the operation')
        value: String | Int | Float | Bool
        (arguments, ops) = DynamicCalculator.ResolveOperatorPrecedences(arguments, ops)
        for i in range(len(arguments)):
            if i == 0:
                value = arguments[0]
            else: 
                value = DynamicCalculator.Operation(value, arguments[i], ops[i-1])
        
        return value
    
    def ResolveOperatorPrecedences(arguments: list[String | Int | Float | Bool], ops: list[str]) -> tuple[list[String | Int | Float | Bool] , list[str]]:
        args: list[String | Int | Float | Bool] = arguments
        op: list[str] = ops
        
        while op.count('*') > 0:
            index: int = op.index('*')
            args[index] = DynamicCalculator.Multiplication(args[index], args[index+1])
            args.pop(index+1)
            op.pop(index)

        while op.count('/') > 0:
            index: int = op.index('/')
            args[index] = DynamicCalculator.Division(args[index], args[index+1])
            args.pop(index+1)
            op.pop(index)

        return (args, op)
        
    def Operation(left: String | Int | Float | Bool, right: String | Int | Float | Bool, operator: str) -> String | Int | Float | Bool:
        match operator:
                    case '+':
                        return DynamicCalculator.Sum(left, right)
                    case '-':
                        return DynamicCalculator.Substraction(left, right)
                    case '*':
                        return DynamicCalculator.Multiplication(left, right)
                    case '/':
                        return DynamicCalculator.Division(left, right)
                    case '&&':
                        pass
                    case '||':
                        pass
                
                    case _:
                        raise MHscr_OperatorError(f"Unsupported operator {operator}")
    
    def Sum(left: String | Int | Float | Bool, right: String | Int | Float | Bool) -> String | Int | Float | Bool:
        T: type = type(left)
        type_argument: type = type(right)
        if type_argument is T and T is not Bool and T is not String:
            
            return T(left.value + right.value)
        elif T is String:
            return T(f"'{str(left.value) + str(right.value)}'")
        elif (T is Int and type_argument is Float) or (T is Float and type_argument is Int):
            return Float(left.value + right.value)
        else:
            raise MHscr_ValueError(f"Unsupported operation: {left} {T} + {right} {type_argument}")
            
    def Substraction(left: String | Int | Float | Bool, right: String | Int | Float | Bool) -> String | Int | Float | Bool:
        T: type = type(left)
        type_argument: type = type(right)
        
        if T is Bool or T is String:
            raise MHscr_TypeError(f"Type {T} cannot be used in a substracting operation.")
        elif type_argument is Bool or type_argument is String:
            raise MHscr_TypeError(f"Type {type_argument} cannot be used in a substracting operation.")
        elif T is Float or type_argument is Float:
            return Float(left.value - right.value)
        elif T is Int and T is type_argument:
            return Int(left.value - right.value)
        else:
            raise MHscr_ValueError(f"Unsupported operation: {left} {T} - {right} {type_argument}")
        
    def Multiplication(left: String | Int | Float | Bool, right: String | Int | Float | Bool) -> String | Int | Float | Bool:
        T: type = type(left)
        type_argument: type = type(right)
        
        if T is Bool or T is String:
            raise MHscr_TypeError(f"Type {T} cannot be used in a multiplicating operation.")
        elif type_argument is Bool or type_argument is String:
            raise MHscr_TypeError(f"Type {type_argument} cannot be used in a multiplicating operation.")
        elif T is Float or type_argument is Float:
            return Float(left.value * right.value)
        elif T is Int and T is type_argument:
            return Int(left.value * right.value)
        else:
            raise MHscr_ValueError(f"Unsupported operation: {left} {T} * {right} {type_argument}")
        
    def Division(left: String | Int | Float | Bool, right: String | Int | Float | Bool) -> String | Int | Float | Bool:
        T: type = type(left)
        type_argument: type = type(right)
        
        if T is Bool or T is String:
            raise MHscr_TypeError(f"Type {T} cannot be used in a divising operation.")
        elif type_argument is Bool or type_argument is String:
            raise MHscr_TypeError(f"Type {type_argument} cannot be used in a divising operation.")
        elif T is Float or type_argument is Float:
            return Float(left.value / right.value)
        elif T is Int and T is type_argument:
            return Int(left.value / right.value)
        else:
            raise MHscr_ValueError(f"Unsupported operation: {left} {T} / {right} {type_argument}")