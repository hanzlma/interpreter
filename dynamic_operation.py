import re

from datatypes import String, Int, Float, Bool, Let

from errors import MHscr_ValueError, MHscr_TypeError, MHscr_OperatorError
from operators import operators
from helper import DynamicListContainsDatatype

class DynamicCalculator:
    """Dynamic Calculator static class"""

    def CalculateDynamicOperations(arguments: list[String | Int | Float | Bool | Let], ops: list[str], _recursive: bool = False) -> String | Int | Float | Bool:
        from datatypes import GetDatatypeDynamically
        for i in range(len(arguments)):
            arguments[i] = GetDatatypeDynamically(str(arguments[i])) if isinstance(arguments[i], Let) else arguments[i]
        if isinstance(arguments[0], String) and (ops.count(operators['minus']) > 0 or ops.count(operators['multiply']) > 0 or ops.count(operators['divide']) > 0 ):
            raise MHscr_TypeError("Strings can only be summed")
        if (not isinstance(arguments[0], (String, Let))) and DynamicListContainsDatatype(arguments, String):
            raise MHscr_TypeError('String can only be used with other datatypes if it is the first type in the operation')
        value: String | Int | Float | Bool
        (arguments, ops) = DynamicCalculator.ResolveNumericalOperatorPrecedences(arguments, ops)
        if not _recursive:
            (arguments, ops) = DynamicCalculator.ResolveLogicalOperatorPrecedences(arguments, ops)
            (arguments, ops) = DynamicCalculator.ResolveComparativeOperatorPrecedences(arguments, ops)
        
        for i in range(len(arguments)):
            if i == 0:
                value = arguments[0]
            else: 
                value = DynamicCalculator.Operation(value, arguments[i], ops[i-1])
        
        return value
    
    def ResolveNumericalOperatorPrecedences(arguments: list[String | Int | Float | Bool], ops: list[str]) -> tuple[list[String | Int | Float | Bool] , list[str]]:
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

    def ResolveLogicalOperatorPrecedences(arguments: list[String | Int | Float | Bool], ops: list[str]) -> tuple[list[String | Int | Float | Bool] , list[str]]:
        if len(re.findall('\|\||&&', str(ops))) < 1:
            return (arguments, ops)
        logicalOperators: list[tuple[int, str]] = []
        for i in range(0, len(arguments) - 1):
            if re.search('^\|\||&&$', ops[i]):
                logicalOperators.append((i, ops[i]))
        outputArguments: list[String | Int | Float | Bool] = []
        outputOperators: list[str] = []

        for i in range(len(logicalOperators)):
            if i == 0:
                outputArguments.append(DynamicCalculator.CalculateDynamicOperations(arguments[:logicalOperators[i][0] + 1], ops[:logicalOperators[i][0]], True))
            else:
                outputArguments.append(DynamicCalculator.CalculateDynamicOperations(arguments[logicalOperators[i-1][0] + 1:logicalOperators[i][0] + 1], ops[logicalOperators[i-1][0] + 1:logicalOperators[i][0]], True))
            outputOperators.append(logicalOperators[i][1])
            if i == len(logicalOperators) - 1:
                outputArguments.append(DynamicCalculator.CalculateDynamicOperations(arguments[logicalOperators[i][0] + 1:], ops[logicalOperators[i][0] + 1:], True))

        return(outputArguments, outputOperators)

    def ResolveComparativeOperatorPrecedences(arguments: list[String | Int | Float | Bool], ops: list[str]) -> tuple[list[String | Int | Float | Bool] , list[str]]:
        if len(re.findall(r'==|!=|>|<|>=|<=', str(ops))) < 1:
            return (arguments, ops)
        logicalOperators: list[tuple[int, str]] = []
        for i in range(0, len(arguments) - 1):
            if re.search(r'^==|!=|>|<|>=|<=$', ops[i]):
                logicalOperators.append((i, ops[i]))
        outputArguments: list[String | Int | Float | Bool] = []
        outputOperators: list[str] = []

        for i in range(len(logicalOperators)):
            if i == 0:
                outputArguments.append(DynamicCalculator.CalculateDynamicOperations(arguments[:logicalOperators[i][0] + 1], ops[:logicalOperators[i][0]], True))
            else:
                outputArguments.append(DynamicCalculator.CalculateDynamicOperations(arguments[logicalOperators[i-1][0] + 1:logicalOperators[i][0] + 1], ops[logicalOperators[i-1][0] + 1:logicalOperators[i][0]], True))
            outputOperators.append(logicalOperators[i][1])
            if i == len(logicalOperators) - 1:
                outputArguments.append(DynamicCalculator.CalculateDynamicOperations(arguments[logicalOperators[i][0] + 1:], ops[logicalOperators[i][0] + 1:], True))
        
        return(outputArguments, outputOperators)

    def Operation(left: String | Int | Float | Bool, right: String | Int | Float | Bool, operator: str) -> String | Int | Float | Bool:
        operations: dict[str, ] = {
            '+': DynamicCalculator.Sum,
            '-': DynamicCalculator.Substraction,
            '*': DynamicCalculator.Multiplication,
            '/': DynamicCalculator.Division,
            '&&': DynamicCalculator.LogicalAnd,
            '||': DynamicCalculator.LogicalOr,
            '==': DynamicCalculator.Equals,
            '!=': DynamicCalculator.NotEquals,
            '>': DynamicCalculator.GreaterThan,
            '<': DynamicCalculator.LowerThan,
            '>=': DynamicCalculator.GreaterOrEqual,
            '<=': DynamicCalculator.LowerOrEqual,
        }
        try:
            return operations[operator](left, right)
        except KeyError:
            raise MHscr_OperatorError(f"Unknown operator {operator}")

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
    
    def LogicalAnd(left: String | Int | Float | Bool, right: String | Int | Float | Bool) -> Bool:
        try:
            return Bool(bool(left.value and right.value))
        except:  # noqa: E722
            raise MHscr_ValueError(f"Unsupported operation: {left} {type(left)} && {right} {type(right)}")
    
    def LogicalOr(left: String | Int | Float | Bool, right: String | Int | Float | Bool) -> Bool:
        try:
            return Bool(bool(left.value or right.value))
        except:  # noqa: E722
            raise MHscr_ValueError(f"Unsupported operation: {left} {type(left)} || {right} {type(right)}")
        
    def Equals(left: String | Int | Float | Bool, right: String | Int | Float | Bool) -> Bool:
        try:
            return Bool(bool(left.value == right.value))
        except:  # noqa: E722
            raise MHscr_ValueError(f"Unsupported operation: {left} {type(left)} == {right} {type(right)}")
    
    def NotEquals(left: String | Int | Float | Bool, right: String | Int | Float | Bool) -> Bool:
        try:
            return Bool(bool(left.value != right.value))
        except:  # noqa: E722
            raise MHscr_ValueError(f"Unsupported operation: {left} {type(left)} != {right} {type(right)}")
    
    def GreaterThan(left: String | Int | Float | Bool, right: String | Int | Float | Bool) -> Bool:
        try:
            return Bool(bool(left.value > right.value))
        except:  # noqa: E722
            raise MHscr_ValueError(f"Unsupported operation: {left} {type(left)} > {right} {type(right)}")
        
    def LowerThan(left: String | Int | Float | Bool, right: String | Int | Float | Bool) -> Bool:
        try:
            return Bool(bool(left.value < right.value))
        except:  # noqa: E722
            raise MHscr_ValueError(f"Unsupported operation: {left} {type(left)} < {right} {type(right)}")
    
    def GreaterOrEqual(left: String | Int | Float | Bool, right: String | Int | Float | Bool) -> Bool:
        try:
            return Bool(bool(left.value >= right.value))
        except:  # noqa: E722
            raise MHscr_ValueError(f"Unsupported operation: {left} {type(left)} >= {right} {type(right)}")
        
    def LowerOrEqual(left: String | Int | Float | Bool, right: String | Int | Float | Bool) -> Bool:
        try:
            return Bool(bool(left.value <= right.value))
        except:  # noqa: E722
            raise MHscr_ValueError(f"Unsupported operation: {left} {type(left)} <= {right} {type(right)}")
    
    def PrintAllArgumentsAndOperators(arguments: list[String | Int | Float | Bool], ops: list[str]) -> None:
        a = []

        for x in arguments:
            a.append(x.value)
        
        print(a)
        print(ops)