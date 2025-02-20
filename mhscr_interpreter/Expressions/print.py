from .expressions import Expression, PrepareValue
from mhscr_interpreter.operators import SplitByOperators


class PrintExp(Expression):
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
        super().__init__(runner, inp, cli)
        
        self.prepareArguments()
    
    def prepareArguments(self) -> None:
        self.argument = self.inp.replace('print ', '')
        self.arguments = SplitByOperators(self.argument)
            
    def execute(self, /, *, functionCall=False) -> None:
        super().execute(functionCall=functionCall)
        self.printvalue = str(PrepareValue(self.runner, self.argument, self.arguments))
        print(f"{'> ' if self.cli else ''}{self.printvalue}")