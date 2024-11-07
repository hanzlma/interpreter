

class MHscr_ValueError(Exception):
    def __init__(self, message:str = "Value Error") -> None:
        self.message = message
        super().__init__(message)
    def __str__(self) -> str:
        return self.message