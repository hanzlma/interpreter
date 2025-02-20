class MHscr_Error(Exception):
    def __init__(self, message:str = "Unknown Error", /, *, line:int = None, command:str=None) -> None:
        self.message = message
        self.line = line
        self.command = command
        super().__init__(message)
    def __str__(self) -> str:
        return self.message
    def get_name(self) -> str:
        return type(self).__name__.removeprefix("MHscr_")

class MHscr_ValueError(MHscr_Error):
    """Value error: Raised in situations when the value of the argument is the reason for the Exception."""
    pass

class MHscr_TypeError(MHscr_Error):
    """Type error: Raised in situations when the type of the argument is the reason for the Exception."""
    pass

class MHscr_OperatorError(MHscr_Error):
    """Operator error: Raised in situations when the operator is the reason for the Exception."""
    pass

class MHscr_KeywordError(MHscr_Error):
    """Keyword error: Raised in situations when the called keyword creates an Exception."""
    pass

class MHscr_SyntaxError(MHscr_Error):
    pass

class MHscr_RuntimeError(MHscr_Error):
    pass

def getErrorLine(runner, expression) -> int | None:
    try:
        return runner.source_expressions.index(expression)
    finally:
        return None
        