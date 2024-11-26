from .expressions import Expression, PrepareValue
from operators import SplitByOperators
from datatypes import Bool
from errors import MHscr_SyntaxError
from .variable import VariableExp, VariableAssignmentExp

class IfExpression(Expression):

    inp: str
    argument: str
    arguments: list[str]
    expressions: list

    def __init__(self, runner, inp: str, cli) -> None:
        super().__init__(runner, inp, cli)
        self.expressions = []
        self.firstCall = True
        self.prepareArguments()
    
    def execute(self) -> None:
        value = Bool(PrepareValue(self.runner, self.argument, self.arguments).value).value
        if self.firstCall:
            self.firstCall = False
            self.firstExec()
            self.remove(value)
        

        if value:
            for exp in self.expressions:
                exp.execute()
        

    def prepareArguments(self) -> None:
        self.argument = self.inp.replace('if ', '')
        self.arguments = SplitByOperators(self.argument)
        
    def firstExec(self) -> None:
        nested: int = 0
        
        index: int = self.runner.source_expressions.index(self)
        
        if not any(isinstance(expression, EndIfExpression) for expression in self.runner.source_expressions[index+1:]):
            raise MHscr_SyntaxError("Missing endif statement.", index)
        for expression in self.runner.source_expressions[index + 1:]:
            if isinstance(expression, (EndIfExpression, EndWhileExpression, EndForExpression)):
                    if nested == 0:
                        break
                    else: 
                        nested -= 1
                        continue
            elif isinstance(expression, (IfExpression, WhileExpression, ForExpression)):
                    if nested == 0:
                        self.expressions.append(expression)
                    nested += 1
                    continue
            elif nested == 0:
                    self.expressions.append(expression)

        
    def remove(self, value: bool) -> None:
        nested = 0
        if not value:
            for expression in self.runner.source_expressions[self.runner.source_expressions.index(self) + 1:]:
                if isinstance(expression, (EndIfExpression)):
                    if nested == 0:
                        break
                    else: 
                        nested -= 1
                        
                if isinstance(expression, (IfExpression)):
                    
                    nested += 1
                    
                
                self.runner.expressions.remove(expression)
            return
        for expression in self.runner.source_expressions[self.runner.source_expressions.index(self) + 1:]:
                if isinstance(expression, (EndIfExpression, EndWhileExpression, EndForExpression)):
                    if nested == 0:
                        break
                    else: 
                        nested -= 1
                        continue
                if isinstance(expression, (IfExpression, WhileExpression, ForExpression)):
                    if nested == 0:
                        self.runner.expressions.remove(expression)
                    nested += 1
                    continue
                if nested != 0:
                    continue
                self.runner.expressions.remove(expression)
class EndIfExpression(Expression):
    pass

class WhileExpression(Expression):

    inp: str
    argument: str
    arguments: list[str]
    expressions: list

    def __init__(self, runner, inp: str, cli: bool) -> None:
        super().__init__(runner, inp, cli)
        self.firstCall = True
        self.expressions = []
        self.prepareArguments()

    def execute(self) -> None:
        value = Bool(PrepareValue(self.runner, self.argument, self.arguments).value).value

        if self.firstCall:
            self.firstCall = False
            self.firstExec()

        while value:
            for expression in self.expressions:
                expression.execute()
            value = Bool(PrepareValue(self.runner, self.argument, self.arguments).value).value

    def prepareArguments(self) -> None:
        self.argument = self.inp.replace('while ', '')
        self.arguments = SplitByOperators(self.argument)

    def firstExec(self) -> None:
        nested: int = 0
        index: int = self.runner.source_expressions.index(self)
        if not any(isinstance(expression, EndWhileExpression) for expression in self.runner.source_expressions[index+1:]):
            raise MHscr_SyntaxError("Missing endwhile statement.", index)

        for expression in self.runner.source_expressions[index+1:]:
                if isinstance(expression, (EndIfExpression, EndWhileExpression, EndForExpression)):
                    if nested == 0:
                        break
                    else: 
                        nested -= 1
                        continue
                elif isinstance(expression, (IfExpression, WhileExpression, ForExpression)):
                    if nested == 0:
                        self.expressions.append(expression)
                    nested += 1
                    continue
                elif nested == 0:
                    self.expressions.append(expression)

        nested = 0

        for expression in self.runner.source_expressions[self.runner.source_expressions.index(self) + 1:]:
                if isinstance(expression, (EndIfExpression, EndWhileExpression, EndForExpression)):
                    if nested == 0:
                        break
                    else: 
                        nested -= 1
                        continue
                if isinstance(expression, (IfExpression, WhileExpression, ForExpression)):
                    if nested == 0:
                        self.runner.expressions.remove(expression)
                    nested += 1
                    continue
                if nested != 0:
                    continue
                self.runner.expressions.remove(expression)

class EndWhileExpression(Expression):
    pass


class ForExpression(Expression):

    inp: str
    argument: list[str] #0 - declaration; 1 logical statement; 2 iteration;
    expressions: list
    declaration: VariableExp
    arguments_if: list[str]
    iteration: VariableAssignmentExp
    declared_varname: str

    def __init__(self, runner, inp: str, cli: bool) -> None:
        super().__init__(runner, inp, cli)
        self.firstCall = True
        self.expressions = []
        self.prepareArguments()

    def prepareArguments(self) -> None:
        self.argument = [arg.strip() for arg in self.inp.replace('for ', '').split(';')]
        
        self.declaration = VariableExp(self.runner, self.argument[0], False)
        self.arguments_if = SplitByOperators(self.argument[1])
        self.iteration = VariableAssignmentExp(self.runner, self.argument[2], False)
        self.declared_varname = self.declaration.name
        
    def execute(self) -> None:
        if self.firstCall:
            self.firstCall = False
            self.firstExec()
        
        self.declaration.execute()
        
        value = Bool(PrepareValue(self.runner, self.argument[1], self.arguments_if).value).value
        
        while value:
            for expression in self.expressions:
                expression.execute()
            self.iteration.execute()
            value = Bool(PrepareValue(self.runner, self.argument[1], self.arguments_if).value).value

        self.runner.variables.pop(self.declared_varname)

    def firstExec(self) -> None:
        nested: int = 0
        index: int = self.runner.source_expressions.index(self)
        if not any(isinstance(expression, EndForExpression) for expression in self.runner.source_expressions[index+1:]):
            raise MHscr_SyntaxError("Missing endfor statement.", index)

        for expression in self.runner.source_expressions[index+1:]:
                if isinstance(expression, (EndIfExpression, EndWhileExpression, EndForExpression)):
                    if nested == 0:
                        break
                    else: 
                        nested -= 1
                        continue
                elif isinstance(expression, (IfExpression, WhileExpression, ForExpression)):
                    if nested == 0:
                        self.expressions.append(expression)
                    nested += 1
                    continue
                elif nested == 0:
                    self.expressions.append(expression)

        nested = 0

        for expression in self.runner.source_expressions[self.runner.source_expressions.index(self) + 1:]:
                if isinstance(expression, (EndIfExpression, EndWhileExpression, EndForExpression)):
                    if nested == 0:
                        break
                    else: 
                        nested -= 1
                        continue
                if isinstance(expression, (IfExpression, WhileExpression, ForExpression)):
                    if nested == 0:
                        self.runner.expressions.remove(expression)
                    nested += 1
                    continue
                if nested != 0:
                    continue
                self.runner.expressions.remove(expression)
                


class EndForExpression(Expression):
    pass