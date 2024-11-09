class MHscr_Error(Exception):
    def __init__(self, message:str = "Unknown Error") -> None:
        self.message = message
        super().__init__(message)
    def __str__(self) -> str:
        return self.message

class MHscr_ValueError(MHscr_Error):
    """Value error: Raised in situations when the value of the argument is the reason for the Exception."""
    pass

class MHscr_TypeError(MHscr_Error):
    """Type error: Raised in situations when the type of the argument is the reason for the Exception."""
    pass

class MHscr_OperatorError(MHscr_Error):
    """Operator error: Raised in situations when the operator is the reason for the Exception."""
    pass