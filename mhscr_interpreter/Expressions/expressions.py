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
    
    def __init__(self, runner, inp:str, cli: bool) -> None:
        self.runner = runner
        self.inp = inp
        self.cli = cli
    
    def execute(self, functionCall=False) -> None:
        pass


        
            
        

        
