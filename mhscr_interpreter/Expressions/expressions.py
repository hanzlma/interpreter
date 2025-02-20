from mhscr_interpreter.operators import GetOperatorsFromText
from mhscr_interpreter.datatypes import GetDatatypeDynamically
from mhscr_interpreter.dynamic_operation import DynamicCalculator

def PrepareValue(runner, argument: str, arguments: list[str]):
    if len(arguments) == 1:
        return GetDatatypeDynamically(runner, argument)
    else:
        operators = GetOperatorsFromText(argument)
        args = []
        for x in arguments:
            args.append(GetDatatypeDynamically(runner, x))
        return DynamicCalculator.CalculateDynamicOperations(args, operators)

class Expression:
    """
    Parent class for all expression classes.
    
    __init__ : reads input values
    
    
    execute : executes the expression
    """
    def __init__(self, runner, inp:str, cli: bool) -> None:
        """

        Args:
            runner : current runner instance
            inp (str): input code
            cli (bool): 
        """
        self.runner = runner
        self.inp = inp
        self.cli = cli
    
    def execute(self, /, *, functionCall=False) -> None:
        self.functionCall=functionCall


        
            
        

        
