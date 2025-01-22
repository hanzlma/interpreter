class Function:
    
    name: str
    arguments: list[tuple] | None
    expressions: list | None
    
    def __init__(self, name, arguments = None, expressions = None) -> None:
        self.name = name
        self.arguments = arguments
        self.expressions = expressions
        self.source_expressions = expressions