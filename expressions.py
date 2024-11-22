import re

from operators import GetOperatorsFromText, SplitByOperators
from datatypes import GetDatatypeDynamically, String, Float, Int, Let, Bool
from variable import Variable
from dynamic_operation import DynamicCalculator
from errors import MHscr_OperatorError, MHscr_ValueError, MHscr_TypeError, MHscr_KeywordError, MHscr_SyntaxError

def PrepareValue(runner, argument: str, arguments: list[str]):
    if len(arguments) == 1:
        return GetDatatypeDynamically(runner, argument)
    else:
        operators = GetOperatorsFromText(argument)
        args = []
        for x in arguments:
            args.append(GetDatatypeDynamically(runner, x))
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
    def __init__(self, runner, inp: str, cli: bool) -> None:
        self.runner = runner
        self.inp = inp
        self.cli = cli
        
        self.prepareArguments()
    
    def prepareArguments(self) -> None:
        self.argument = self.inp.replace('print ', '')
        self.arguments = SplitByOperators(self.argument)
            
    def execute(self) -> None:
        self.printvalue = str(PrepareValue(self.runner, self.argument, self.arguments))
        print(f"{'> ' if self.cli else ''}{self.printvalue}")

        
class InputExp:
    """
    Input expression.
    Structure:
        input <variable to assign input to>
    Example:
        input test //assigns input to variable 'test'

    """
    cli: bool
    inp: str
    name: str | None
    msg: str | None
    
    def __init__(self, runner, inp: str, cli:bool) -> None:
        self.runner = runner
        self.inp = inp
        self.cli = cli
        self.name = None
        self.msg = None
        
        self.prepareArguments()

    def prepareArguments(self) -> None:
        args: list[str] = [match[0] or match[1] for match in re.findall(r"(\b[a-zA-Z]*\b)|(['|\"][^'\"]*['|\"])", self.inp.replace('input ', ''))]
        while args.count('') > 0:
            args.remove('')
        if len(args) == 0:
            return
        if len(args) == 1:
            try:
                self.msg = String(self.inp.replace('input ','')).value
                return
            except MHscr_ValueError:
                pass
            if args[0] in self.runner.keywords.dictionary.keys():
                self.name = args[0]
            else:
                raise MHscr_ValueError("Variable not initialized", self.runner.expressions.index(self) if not self.cli else None)
        elif len(args) == 2:
            if args[0] in self.runner.keywords.dictionary.keys():
                self.name = args[0]
                self.msg = String(args[1]).value
            elif args[1] in self.runner.keywords.dictionary.keys():
                self.name = args[1]
                self.msg = String(args[0]).value
            else:
                raise MHscr_ValueError("Variable not initialized", self.runner.expressions.index(self) if not self.cli else None)
        else:
            raise MHscr_ValueError("Unexpected argument count", self.runner.expressions.index(self) if not self.cli else None)

    def execute(self) -> None:
        
        value = input(f"{'[input]> ' if self.cli else ''}{self.msg if self.msg is not None else ''}")
        if self.name:
            value = GetDatatypeDynamically(self.runner, value)
            if not isinstance(value, self.runner.variables[self.name].datatype) and self.runner.variables[self.name].datatype is not Let:
                raise MHscr_TypeError(f"Variable of type {self.runner.variables[self.name].datatype} cannot be assigned value of type {type(value)}.", self.runner.expressions.index(self) if not self.cli else None)
            self.runner.variables[self.name] = Variable(self.name, type(value), value)
            
        
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
    
    def __init__(self, runner, inp: str, cli: bool, const: bool = False) -> None:
        self.runner = runner
        self.inp = inp
        self.cli = cli
        self.const = const
        
        self.prepareArguments()

    def prepareArguments(self)->None:
        parts: list[str] = self.inp.split(' ')
        self.__getDatatype(parts[0])
        
        self.name = parts[1]
        if parts[2] != '=':
            raise MHscr_OperatorError(f"Unexpected value {parts[2]}", self.runner.expressions.index(self) if not self.cli else None)
        self.argument = self.inp.replace(f"{parts[0]} {parts[1]} {parts[2]} ", "")
        self.arguments = SplitByOperators(self.argument)          

    def execute(self)->None:
        self.var = PrepareValue(self.runner, self.argument, self.arguments)
        if self.name in self.runner.variables:
            raise MHscr_ValueError(f"Variable '{self.name}' already initialized.", self.runner.expressions.index(self) if not self.cli else None)
        self.runner.variables[self.name] = Variable(self.name, self.datatype, self.var, self.const)
        if not self.const:
            self.runner.keywords.dictionary[self.name] = VariableAssignmentExp
        
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
            raise MHscr_KeywordError(f"Datatype {datatypeName} is not a valid datatype for a {'constant ' if self.const else ''}variable.", self.runner.expressions.index(self) if not self.cli else None)
        
class ConstantVariableExp:
    
    cli: bool
    inp: str
    
    def __init__(self, runner, inp: str, cli: bool) -> None:
        self.runner = runner
        self.inp = inp.replace('const ', '')
        self.cli = cli

    def execute(self) -> None:
        VariableExp(self.runner,self.inp, self.cli, True).execute()

class VariableAssignmentExp:
    cli: bool
    inp: str
    name: str
    argument: str
    arguments: list[str]
    var: String | Int | Float | Bool | Let
    
    def __init__(self, runner, inp: str, cli: bool) -> None:
        self.runner = runner
        self.inp = inp
        self.cli = cli
        
        self.prepareArguments()
        
    def execute(self) -> None:
        self.var = PrepareValue(self.runner, self.argument, self.arguments)
        if self.name not in self.runner.variables:
            raise MHscr_ValueError(f"Variable {self.name} not initialized", self.runner.expressions.index(self) if not self.cli else None)
        if type(self.var) is not type(self.runner.variables[self.name].var) and not isinstance(self.runner.variables[self.name].var, Let):
            val = f'"{self.var.value}"' if isinstance(self.var.value, str) else self.var.value
            raise MHscr_TypeError(f"Type {self.runner.variables[self.name].datatype.__name__} cannot hold value {val}", self.runner.expressions.index(self) if not self.cli else None)
        if self.runner.variables[self.name].const:
            raise MHscr_TypeError("Cannot assign value to constant.", self.runner.expressions.index(self) if not self.cli else None)
        if isinstance(self.runner.variables[self.name].var, Let):
            self.var = Let(self.var)
        
        self.runner.variables[self.name] = Variable(self.name, self.runner.variables[self.name].datatype, self.var, False)

    def prepareArguments(self) -> None:
        parts = self.inp.split(' ')
        self.name = parts[0]
        if parts[1] != '=':
            raise MHscr_OperatorError(f"Unexpected value {parts[2]}", self.runner.expressions.index(self) if not self.cli else None)
        self.argument = self.inp.replace(f"{parts[0]} {parts[1]} ", "")
        self.arguments = SplitByOperators(self.argument)

        
class IfExpression:
    
    inp: str
    argument: str
    arguments: list[str]
    
    def __init__(self, runner, inp: str, cli) -> None:
        self.runner = runner
        self.inp = inp
        
        self.prepareArguments()
    
    def execute(self) -> None:
        value = Bool(PrepareValue(self.runner, self.argument, self.arguments).value).value
        nested: int = 0
        
        index: int = self.runner.expressions.index(self)
        for exp in self.runner.expressions[index + 1:]:
            if isinstance(exp, IfExpression):
                nested += 1
            if isinstance(exp, EndIfExpression):
                if nested == 0:
                    return
                nested -= 1
            if not value: 
                self.runner.expressions.remove(exp)
        raise MHscr_SyntaxError("Missing endif expression.", index)

    def prepareArguments(self) -> None:
        self.argument = self.inp.replace('if ', '')
        self.arguments = SplitByOperators(self.argument)
    
class EndIfExpression:
    
    def __init__(self, runner, inp, cli) -> None:
        pass
    
    def execute(self):
        pass