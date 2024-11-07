from lexer import Lexer
from errors import MHscr_ValueError
class CLIRunner:
    """
    Runner for in-CLI interpreter
    """
    def Run(self) -> None:
        print('MHscript version alpha 1')
        print('Input commands line by line')
        print('End by writing "exit" or by using Ctrl + C\n\n')
        lexer: Lexer = Lexer(self)
        try:
            inp = input('> ')
            while inp != 'exit':
                try:
                    expression = lexer.Lex(inp)(inp, True)
                    expression.execute()
                except MHscr_ValueError as err:
                    print(f'> Code "{inp}" could not have been executed because of a ValueError!\nError:{err}')
                inp = input('> ')
        except KeyboardInterrupt:
            pass