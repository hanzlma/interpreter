class KeywordsDict:
    """
    Translates keyword into class reference.
    """
    from expressions import PrintExp
    dictionary: dict[str, ] = {
    
        'print': PrintExp,
    }
    def __init__(self, parent) -> None:
        self.cli = parent.cli
    def GetExpression(self, command) -> PrintExp:
        return self.dictionary[command]