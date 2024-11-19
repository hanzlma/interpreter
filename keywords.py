from errors import MHscr_KeywordError
from helper import getRunnerInstance
class KeywordsDict:
    """
    Translates keyword into class reference.
    """
    from expressions import PrintExp, VariableExp, ConstantVariableExp
    dictionary: dict[str, ] = {
    
        'print': PrintExp,
        'string': VariableExp,
        'int': VariableExp,
        'float': VariableExp,
        'bool': VariableExp,
        'let': VariableExp,
        'const': ConstantVariableExp,
    }
    def GetExpression(self, command) -> PrintExp:
        try:
            return self.dictionary[command]
        except KeyError as err:
            raise MHscr_KeywordError(f"Unknown keyword {err}" if command not in getRunnerInstance().variables.keys() else f"Cannot change value of an initialized constant {command}")