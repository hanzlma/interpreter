from lexer import Lexer
from errors import MHscr_ValueError, MHscr_TypeError, MHscr_OperatorError, MHscr_KeywordError, MHscr_SyntaxError
from variable import Variable
from keywords import KeywordsDict

class WholefileRunner:
    """Runner class for wholefile interpreter."""
    
    variables: dict[str, Variable] = dict[str, Variable]()

    lexer: Lexer
    filepath: str
    expressions: list = []
    
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
            for i in range(len(lines)):
                lines[i] = lines[i].replace('\n', '')
            commands = self.lexer.Lex(lines)
            self.expressions = [commands[i](runner=self, inp=lines[i], cli=False) for i in range(len(commands))]
            for expression in self.expressions:
                expression.execute()
        except (MHscr_KeywordError, MHscr_OperatorError, MHscr_TypeError, MHscr_ValueError, MHscr_TypeError, MHscr_SyntaxError) as err:
            print(f"Program encountered an exception: line {err.line}, {err.get_name()}: {err.message}")
        finally:
            file.close()
        
    