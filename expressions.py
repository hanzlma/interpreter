
from operators import GetOperatorsFromText, SplitByOperators
from datatypes import GetDatatypeDynamically, String, Float, Int, Let, Bool
from variable import Variable
from dynamic_operation import DynamicCalculator
from helper import getRunnerInstance
from errors import MHscr_OperatorError, MHscr_ValueError, MHscr_TypeError, MHscr_KeywordError

def PrepareValue(argument: str, arguments: list[str]):
    if len(arguments) == 1:
        return GetDatatypeDynamically(argument)
    else:
        operators = GetOperatorsFromText(argument)
        args = []
        for x in arguments:
            args.append(GetDatatypeDynamically(x))
        return DynamicCalculator.CalculateDynamicOperations(args, operators)

class PrintExp:
    """
    Print expression.
    Structure:
        print <what to print>
    Example:
        print "Hello world"

    """
    cli: bool
    inp: str
    argument: str
    arguments: list
    printvalue: str
    def __init__(self, inp: str, cli: bool) -> None:
        self.inp = inp
        self.cli = cli
    
    def prepareArguments(self) -> None:
        self.argument = self.inp.replace('print ', '')
        self.arguments = SplitByOperators(self.argument)
        
        self.printvalue = str(PrepareValue(self.argument, self.arguments))
            
    def execute(self) -> None:
        self.prepareArguments()
        print(f"{'> ' if self.cli else ''}{self.printvalue}")

        
class InputExp:
    """
    Input expression.
    Structure:
        input <variable to assign input to>
    Example:
        input test //assigns input to variable 'test'

    """
    cmd = 'input'
    #variable: TBD
    
class VariableExp:
    """
    
    """
    cli: bool
    inp: str
    name: str
    argument: str
    arguments: list
    datatype: type
    var: String | Int | Float | Bool
    const: bool
    
    def __init__(self, inp: str, cli: bool, const: bool = False) -> None:
        self.inp = inp
        self.cli = cli
        self.const = const
    def prepareArguments(self)->None:
        parts: list[str] = self.inp.split(' ')
        self.__getDatatype(parts[0])
        
        self.name = parts[1]
        if parts[2] != '=':
            raise MHscr_OperatorError(f"Unexpected value {parts[2]}")
        self.argument = self.inp.replace(f"{parts[0]} {parts[1]} {parts[2]} ", "")
        self.arguments = SplitByOperators(self.argument)
        
        """ if len(self.arguments) == 1:
            self.var = GetDatatypeDynamically(self.argument)
        else:
            operators = GetOperatorsFromText(self.argument)
            args = []
            for x in self.arguments:
                args.append(GetDatatypeDynamically(x))
            self.arguments = args
            self.var = DynamicCalculator.CalculateDynamicOperations(self.arguments, operators) """
            
        self.var = PrepareValue(self.argument, self.arguments)
    def execute(self)->None:
        self.prepareArguments()
        runner = getRunnerInstance()
        if self.name in runner.variables:
            raise MHscr_ValueError(f"Variable '{self.name}' already initialized.")
        runner.variables[self.name] = Variable(self.name, self.datatype, self.var, self.const)
        if not self.const:
            runner.keywords.dictionary[self.name] = VariableAssignmentExp
        
    def __getDatatype(self, datatypeName:str)->None:
        dictionary: dict[str, ] = {
            'string': String,
            'int': Int,
            'float': Float,
            'bool': Bool,
            'let': Let
        }
        if self.const:
            dictionary.pop('let')
        try:
            self.datatype = dictionary[datatypeName]
        except KeyError:
            raise MHscr_KeywordError(f"Datatype {datatypeName} is not a valid datatype for a {'constant ' if self.const else ''}variable.")
        
class ConstantVariableExp:
    
    cli: bool
    inp: str
    
    def __init__(self, inp: str, cli: bool) -> None:
        self.inp = inp.replace('const ', '')
        self.cli = cli
    def execute(self) -> None:
        VariableExp(self.inp, self.cli, True).execute()

class VariableAssignmentExp:
    cli: bool
    inp: str
    name: str
    argument: str
    arguments: list[str]
    var: String | Int | Float | Bool | Let
    
    def __init__(self, inp: str, cli: bool) -> None:
        self.inp = inp
        self.cli = cli
        
    def execute(self) -> None:
        self.prepareArguments()
        
        runner = getRunnerInstance()
        if self.name not in runner.variables:
            raise MHscr_ValueError(f"Variable {self.name} not initialized")
        if type(self.var) is not type(runner.variables[self.name].var) and not isinstance(runner.variables[self.name].var, Let):
            raise MHscr_TypeError(f"Type {runner.variables[self.name].var} cannot hold value {self.var.value}")
        if runner.variables[self.name].const:
            raise MHscr_TypeError("Cannot assign value to constant.")
        if isinstance(runner.variables[self.name].var, Let):
            self.var = Let(self.var)
        
        runner.variables[self.name] = Variable(self.name, runner.variables[self.name].datatype, self.var, False)


    def prepareArguments(self) -> None:
        parts = self.inp.split(' ')
        self.name = parts[0]
        if parts[1] != '=':
            raise MHscr_OperatorError(f"Unexpected value {parts[2]}")
        self.argument = self.inp.replace(f"{parts[0]} {parts[1]} ", "")
        self.arguments = SplitByOperators(self.argument)
        self.var = PrepareValue(self.argument, self.arguments)
        