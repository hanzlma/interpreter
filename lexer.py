from helper import getRunnerInstance
class Lexer:
    """
    Lexer class of MHscript interpreter.
    """
    cli: bool
    lexFunction: str
    def __init__(self, parent) -> None:
        from runner_cli import CLIRunner
        self.cli = True if isinstance(parent, CLIRunner) else False #doplnit WholeFile typem
        self.lexFunction = "Lex_CLI" if self.cli else "Lex_WholeFile"

    from expressions import PrintExp, VariableAssignmentExp, VariableExp, ConstantVariableExp

    def Lex(self, script: str) -> PrintExp | VariableExp | ConstantVariableExp | VariableAssignmentExp:
        return getattr(self, self.lexFunction)(script)
    
    def Lex_CLI(self, line: str) -> PrintExp | VariableExp | ConstantVariableExp | VariableAssignmentExp:
        command = line.split(' ')[0]
        

        expression = getRunnerInstance().keywords.GetExpression(command=command)
        return expression

