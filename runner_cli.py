from lexer import Lexer
from errors import MHscr_ValueError, MHscr_TypeError, MHscr_OperatorError, MHscr_KeywordError
from variable import Variable
from keywords import KeywordsDict
class CLIRunner:
    """Runner for in-CLI interpreter."""
    variables: dict[str, Variable] = dict[str, Variable]()
    keywords: KeywordsDict = KeywordsDict()
    def __init__(self) -> None:
        self.lexer: Lexer = Lexer(self)
    def Run(self) -> None:
        print('MHscript version alpha 1')
        print('Input commands line by line')
        print('End by writing "exit" or by using Ctrl + C\n\n')

        try:
            inp = input('> ')
            while inp != 'exit':
                try:
                    expression = self.lexer.Lex(inp)(inp, True)
                    expression.execute()
                except MHscr_ValueError as err:
                    print(f'> Code "{inp}" could not have been executed because of a ValueError!\nError: {err}')
                except MHscr_TypeError as err:
                    print(f'> Code "{inp}" could not have been executed because of a TypeError!\nError: {err}')
                except MHscr_OperatorError as err:
                    print(f'> Code "{inp}" could not have been executed because of an OperatorError!\nError: {err}')
                except MHscr_KeywordError as err:
                    print(f'> Code "{inp}" could not have been executed because of a KeywordError!\nError: {err}')
                inp = input('> ')
        except KeyboardInterrupt:
            pass