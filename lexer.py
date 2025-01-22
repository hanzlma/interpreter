class Lexer:
    """
    Lexer class of MHscript interpreter.
    """
    cli: bool
    lexFunction: str
    def __init__(self, runner) -> None:
        from runner_cli import CLIRunner
        self.cli = True if isinstance(runner, CLIRunner) else False #doplnit WholeFile typem
        self.lexFunction = "Lex_CLI" if self.cli else "Lex_Wholefile"
        self.runner = runner

    from Expressions.variable import VariableExp, VariableAssignmentExp, ConstantVariableExp
    from Expressions.print import PrintExp
    from Expressions.input import InputExp

    def Lex(self, script: str | list[str]) -> PrintExp | VariableExp | ConstantVariableExp | VariableAssignmentExp | InputExp | list[PrintExp | VariableExp | ConstantVariableExp | VariableAssignmentExp | InputExp]:
        return getattr(self, self.lexFunction)(script)
    
    def Lex_CLI(self, line: str) -> PrintExp | VariableExp | ConstantVariableExp | VariableAssignmentExp | InputExp:
        command = line.split(' ')[0]
        
        expression = self.runner.keywords.GetExpression(command=command)
        return expression
    
    def Lex_Wholefile(self, lines: list[str]) -> list[PrintExp | VariableExp | ConstantVariableExp | VariableAssignmentExp | InputExp]:
        expressions = []
        for line in lines:
            expressions.append(self.runner.keywords.GetExpression(command=line.split(' ')[0]))
            from Expressions.variable import VariableExp, VariableAssignmentExp
            from Expressions.function import FunctionDefinitionExpression, FunctionCallExpression
            
            if expressions[-1] is VariableExp:
                self.runner.keywords.dictionary[line.split(' ')[1]] = VariableAssignmentExp
            elif expressions[-1] is FunctionDefinitionExpression:
                self.runner.keywords.dictionary[line.split(' ')[1]] = FunctionCallExpression
        return expressions

