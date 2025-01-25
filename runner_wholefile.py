from lexer import Lexer
from errors import MHscr_Error
from variable import Variable
from keywords import KeywordsDict
from function import Function

class WholefileRunner:
    """Runner class for wholefile interpreter."""
    
    variables: dict[str, Variable] = dict[str, Variable]()

    lexer: Lexer
    filepath: str
    expressions: list = []
    functions: list[Function] = []
    
    def __init__(self, filepath:str) -> None:
        self.filepath = filepath
        self.keywords = None
        self.lexer: Lexer = None
        
        self._initialize_subcomponents()
    def _initialize_subcomponents(self):
        self.keywords = KeywordsDict(runner=self, cli=False)
        self.lexer = Lexer(runner=self)
        
    def Run(self) -> None:
        try:
            file = open(self.filepath)
            lines = file.readlines()
        except Exception as Err:
            print(Err)
        finally:
            file.close()
        
        for i in range(len(lines)):
            lines[i] = lines[i].replace('\n', '')
        try:
            commands = self.lexer.Lex(lines)
        except MHscr_Error as err:
            print(f"Program encountered an exception: line {lines.index(err.command)}, {err.get_name()}: {err.message}")
            exit()
            
        try:
            self.expressions = [commands[i](runner=self, inp=lines[i], cli=False) for i in range(len(commands))]

        except MHscr_Error as err:
            print(f"Program encountered an exception: line {err.line if err.line else lines.index(err.command)}, {err.get_name()}: {err.message}")
            exit()

        self.source_expressions = self.expressions.copy()
            

        for expression in self.expressions:
            try: 
                expression.execute()
            except MHscr_Error as err:
                print(f"Program encountered an exception: line {err.line if err.line else self.expressions.index(expression)}, {err.get_name()}: {err.message}")
                exit()
        
    