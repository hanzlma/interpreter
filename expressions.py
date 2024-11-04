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
    arguments: list#[] TBD
    def __init__(self, inp: str, cli: bool) -> None:
        self.inp = inp
        self.cli = cli
    
    def prepareArguments(self) -> None:
        argument: str = self.inp.replace('print ', '')
        if argument.count('"') == 0:
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
                self.argument += phrase.strip().replace('"','')
            
    def execute(self) -> None:
        self.prepareArguments()
        print(f"{'> ' if self.cli else ''}{self.argument}")
    
        
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