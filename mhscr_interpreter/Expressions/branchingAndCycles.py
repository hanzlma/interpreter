from .expressions import Expression, PrepareValue
from mhscr_interpreter.operators import SplitByOperators
from mhscr_interpreter.datatypes import Bool
from mhscr_interpreter.errors import MHscr_SyntaxError
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

    def execute(self, functionCall=False) -> None:
        
        value = Bool(PrepareValue(self.runner, self.argument, self.arguments).value).value
        runner = functionCall if functionCall else self.runner
        if self.firstCall:
            self.firstCall = False
            self.firstExec(runner)
            self.remove(value, runner)
        

        if value:
            for exp in self.expressions:
                exp.execute(functionCall)
        

    def prepareArguments(self) -> None:
        self.argument = self.inp.replace('if ', '')
        self.arguments = SplitByOperators(self.argument)
        
    def firstExec(self, runner) -> None:
        nested: int = 0
        
        index: int = runner.source_expressions.index(self)
        
        if not any(isinstance(expression, EndIfExpression) for expression in runner.source_expressions[index+1:]):
            raise MHscr_SyntaxError("Missing endif statement.", line=index)
        for expression in runner.source_expressions[index + 1:]:
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

        
    def remove(self, value: bool, runner) -> None:
        nested = 0
        if not value:
            for expression in runner.source_expressions[runner.source_expressions.index(self) + 1:]:
                if isinstance(expression, (EndIfExpression)):
                    if nested == 0:
                        break
                    else: 
                        nested -= 1
                        
                if isinstance(expression, (IfExpression)):
                    
                    nested += 1
                    
                
                runner.expressions.remove(expression)
            return
        for expression in runner.source_expressions[runner.source_expressions.index(self) + 1:]:
                if isinstance(expression, (EndIfExpression, EndWhileExpression, EndForExpression)):
                    if nested == 0:
                        break
                    else: 
                        nested -= 1
                        continue
                if isinstance(expression, (IfExpression, WhileExpression, ForExpression)):
                    if nested == 0:
                        runner.expressions.remove(expression)
                    nested += 1
                    continue
                if nested != 0:
                    continue
                runner.expressions.remove(expression)
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

    def execute(self, functionCall=False) -> None:
        value = Bool(PrepareValue(self.runner, self.argument, self.arguments).value).value
        runner = functionCall if functionCall else self.runner
        if self.firstCall:
            self.firstCall = False
            self.firstExec(runner)

        while value:
            for expression in self.expressions:
                expression.execute()
            value = Bool(PrepareValue(self.runner, self.argument, self.arguments).value).value

    def prepareArguments(self) -> None:
        self.argument = self.inp.replace('while ', '')
        self.arguments = SplitByOperators(self.argument)

    def firstExec(self, runner) -> None:
        nested: int = 0
        index: int = runner.source_expressions.index(self)
        if not any(isinstance(expression, EndWhileExpression) for expression in runner.source_expressions[index+1:]):
            raise MHscr_SyntaxError("Missing endwhile statement.", line=index)

        for expression in runner.source_expressions[index+1:]:
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
        
        for expression in runner.source_expressions[runner.source_expressions.index(self) + 1:]:
                if isinstance(expression, (EndIfExpression, EndWhileExpression, EndForExpression)):
                    if nested == 0:
                        break
                    else: 
                        nested -= 1
                        continue
                if isinstance(expression, (IfExpression, WhileExpression, ForExpression)):
                    if nested == 0:
                        runner.expressions.remove(expression)
                    nested += 1
                    continue
                if nested != 0:
                    continue
                runner.expressions.remove(expression)

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
        
    def execute(self, functionCall=False) -> None:
        runner = functionCall if functionCall else self.runner
        if self.firstCall:
            self.firstCall = False
            self.firstExec(runner)
        
        self.declaration.execute()
        
        value = Bool(PrepareValue(self.runner, self.argument[1], self.arguments_if).value).value
        
        while value:
            for expression in self.expressions:
                expression.execute()
            self.iteration.execute()
            value = Bool(PrepareValue(self.runner, self.argument[1], self.arguments_if).value).value

        self.runner.variables.pop(self.declared_varname)

    def firstExec(self, runner) -> None:
        nested: int = 0
        index: int = runner.source_expressions.index(self)
        if not any(isinstance(expression, EndForExpression) for expression in runner.source_expressions[index+1:]):
            raise MHscr_SyntaxError("Missing endfor statement.", line=index)

        for expression in runner.source_expressions[index+1:]:
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
        
        for expression in runner.source_expressions[runner.source_expressions.index(self) + 1:]:
                if isinstance(expression, (EndIfExpression, EndWhileExpression, EndForExpression)):
                    if nested == 0:
                        break
                    else: 
                        nested -= 1
                        continue
                if isinstance(expression, (IfExpression, WhileExpression, ForExpression)):
                    if nested == 0:
                        runner.expressions.remove(expression)
                    nested += 1
                    continue
                if nested != 0:
                    continue
                runner.expressions.remove(expression)
                


class EndForExpression(Expression):
    pass