from operators import GetOperatorsFromText, SplitByOperators
from datatypes import GetDatatypeDynamically
from dynamic_operation import DynamicCalculator
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
        
        if len(self.arguments) == 1:
            self.printvalue = str(GetDatatypeDynamically(self.argument).value)
        else:
            operators = GetOperatorsFromText(self.argument)
            args = []
            for x in self.arguments:
                args.append(GetDatatypeDynamically(x))
            self.arguments = args
            self.printvalue = str(DynamicCalculator.CalculateDynamicOperations(self.arguments, operators).value)
        """ if argument.count('"') == 0:
            pass
        elif argument.count('"') == 2:
            self.argument = argument.replace('"', '')
        elif argument.count('"') % 2 != 0:
            raise
        elif argument.count('"') / 2 != argument.count('+') + 1:
            raise
        else:
            phrases = argument.split('+')
            self.argument = ''
            for phrase in phrases:
                self.argument += phrase.strip().replace('"','') """
            
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