from mhscr_interpreter.errors import MHscr_KeywordError
class KeywordsDict:
    """
    Translates keyword into class reference.
    """
    from .Expressions.branchingAndCycles import IfExpression, EndIfExpression, WhileExpression, EndWhileExpression, ForExpression, EndForExpression
    from .Expressions.variable import VariableExp, VariableAssignmentExp, ConstantVariableExp
    from .Expressions.print import PrintExp
    from .Expressions.input import InputExp
    from .Expressions.function import FunctionDefinitionExpression, EndFunctionDefinitionExpression
    dictionary: dict[str, ] = {
    
        'print': PrintExp,
        'input': InputExp,
        'string': VariableExp,
        'int': VariableExp,
        'float': VariableExp,
        'bool': VariableExp,
        'let': VariableExp,
        'const': ConstantVariableExp,
    }
    wholefileOnlyDictionary: dict[str, ] = {
        'if': IfExpression,
        'endif': EndIfExpression,
        'while': WhileExpression,
        'endwhile': EndWhileExpression,
        'for': ForExpression,
        'endfor': EndForExpression,
        'fn': FunctionDefinitionExpression,
        'endfn': EndFunctionDefinitionExpression,
    }
    def __init__(self, runner, cli = True) -> None:
        self.runner = runner
        if not cli:
            self.dictionary.update(self.wholefileOnlyDictionary)
       
    def GetExpression(self, command):
        try:
            return self.dictionary[command]
        except KeyError as err:
            raise MHscr_KeywordError(f"Unknown keyword {err}" if command not in self.runner.variables.keys() else f"Cannot change value of an initialized constant {command}", command=command)