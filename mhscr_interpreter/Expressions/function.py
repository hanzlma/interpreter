from .expressions import Expression
from mhscr_interpreter.errors import MHscr_RuntimeError, MHscr_SyntaxError
from mhscr_interpreter.function import Function
from mhscr_interpreter.variable import Variable
from mhscr_interpreter.datatypes import GetDatatypeDynamically
class FunctionDefinitionExpression(Expression):
    """
    Implementation of a function definition expression.
    This expression starts a function block, meaning all following expressions until
    EndFunctionDefinitionExpression belong to this function.
    
    ALL FUNCTION PARAMETRES ARE READ-ONLY!
    """
    arguments: list[str]
    defined_arguments: list[tuple] = []
    expressions: list = []
    name: str
    
    def __init__(self, runner, inp: str, cli: bool) -> None:
        super().__init__(runner, inp, cli)
        self.prepareArguments()
    
    def prepareArguments(self) -> None:
        self.name = self.inp.replace('fn ', '').split(' ')[0]
        self.arguments = [arg.strip() for arg in self.inp.replace(f"fn {self.name}", '').split(',')]

        from .variable import VariableExp, VariableAssignmentExp
        
        for argument in self.arguments:
            datatype = VariableExp.GetDatatype(self.runner, self, argument.split(' ')[0])
            name = argument.split(' ')[1]
            self.defined_arguments.append((datatype, name))
            self.runner.keywords.dictionary[name] = VariableAssignmentExp

        
    def getExpressions(self) -> None:
        index = self.runner.source_expressions.index(self)

        if not any([isinstance(expression, EndFunctionDefinitionExpression) for expression in self.runner.source_expressions[index + 1:]]):
            raise MHscr_SyntaxError("Missing endfn statement.", line=index)

        for expression in self.runner.source_expressions[index + 1:]:
            if isinstance(expression, EndFunctionDefinitionExpression):
                break
            self.expressions.append(expression)
            self.runner.expressions.remove(expression)
        
    
    def execute(self, /, *, functionCall=False) -> None:
        super().execute(functionCall=functionCall)
        if functionCall:
            raise MHscr_RuntimeError("Cannot define a function inside a function", line=self.runner.source_expressions.index(self))
        self.getExpressions()
        
        if any([fn.name == self.name for fn in self.runner.functions]):
            raise MHscr_RuntimeError(f"Function '{self.name}' is already defined.", line=self.runner.source_expressions.index(self))
        
        self.runner.functions.append(Function(self.name, self.defined_arguments, self.expressions))
        
        
        

class EndFunctionDefinitionExpression(Expression):
    """Expression symbolizing the end of the function definition block."""
    pass
class FunctionCallExpression(Expression):
    """Expression which calls a previously defined function."""
    
    name: str
    arguments: list[str]
    function: Function = None
    
    def __init__(self, runner, inp: str, cli: bool) -> None:
        super().__init__(runner, inp, cli)
        self.name = self.inp.split(' ')[0]
        self.arguments = [arg.strip() for arg in self.inp.replace(self.name, '').split(',')]
    
    def execute(self, /, *, functionCall=False) -> None:
        super().execute(functionCall=functionCall)
        for fn in self.runner.functions:
            if fn.name == self.name:
                self.function = fn
                break
        if not self.function:
            raise MHscr_RuntimeError("Function does not exist.", line=self.runner.source_expressions.index(self))
        for i in range(len(self.function.arguments)):
            (datatype, name) = self.function.arguments[i]
            if name in self.runner.variables.keys():
                raise MHscr_RuntimeError(f"Variable {name} already initialized.", line=self.runner.source_expressions.index(self))
            self.runner.variables[name] = Variable(name, datatype, GetDatatypeDynamically(self.runner,self.arguments[i]), local=True)
        
        for expression in self.function.expressions:
            expression.execute(functionCall=next(f for f in self.runner.functions if f == self.function))
            
        for (datatype, name) in self.function.arguments:
            self.runner.variables.pop(name)
            
        names = []
        for (name,var) in self.runner.variables.items():
            if var.local:
                names.append(name)
                self.runner.keywords.dictionary.pop(name)
        for name in names:
            self.runner.variables.pop(name)
        
        