from mhscr_interpreter.errors import MHscr_KeywordError


class Lexer:
    """
    Lexer class of MHscript interpreter.
    """

    cli: bool
    lexFunction: str

    def __init__(self, runner) -> None:
        from .runner_cli import CLIRunner

        self.cli = True if isinstance(runner, CLIRunner) else False
        self.lexFunction = "Lex_CLI" if self.cli else "Lex_Wholefile"
        self.runner = runner

    from mhscr_interpreter.Expressions.expressions import Expression

    def Lex(self, script: str | list[str]) -> Expression | list[Expression]:
        return getattr(self, self.lexFunction)(script)

    def Lex_CLI(self, line: str) -> Expression:
        command = line.split(" ")[0]
        expression = self.runner.keywords.GetExpression(command=command)
        return expression

    def Lex_Wholefile(self, lines: list[str]) -> list[Expression]:
        expressions = []
        for line in lines:
            try:
                expressions.append(
                    self.runner.keywords.GetExpression(command=line.split(" ")[0])
                )
            except MHscr_KeywordError as err:
                raise MHscr_KeywordError(err.message, command=line)
            from .Expressions.variable import VariableExp, VariableAssignmentExp
            from .Expressions.function import (
                FunctionDefinitionExpression,
                FunctionCallExpression,
            )

            if expressions[-1] is VariableExp:
                self.runner.keywords.dictionary[line.split(" ")[1]] = (
                    VariableAssignmentExp
                )
            elif expressions[-1] is FunctionDefinitionExpression:
                self.runner.keywords.dictionary[line.split(" ")[1]] = (
                    FunctionCallExpression
                )
        return expressions
