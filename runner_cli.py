from lexer import Lexer
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
                expression = lexer.Lex(inp)(inp, True)
                expression.execute()
                inp = input('> ')
        except KeyboardInterrupt:
            pass