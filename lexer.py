class Lexer:
    """
    Lexer class of MHscript interpreter.
    """
    cli: bool
    lexFunction: str
    def __init__(self, parent) -> None:
        from runner_cli import CLIRunner
        self.cli = True if type(parent) == CLIRunner else False #doplnit WholeFile typem
        self.lexFunction = "Lex_CLI" if self.cli else "Lex_WholeFile"

    from expressions import PrintExp

    def Lex(self, script: str) -> PrintExp:
        return getattr(self, self.lexFunction)(script)
    
    def Lex_CLI(self, line: str) -> PrintExp:
        command = line.split(' ')[0]
        
        from keywords import KeywordsDict
        expression = KeywordsDict(self).GetExpression(command=command)
        return expression
    
