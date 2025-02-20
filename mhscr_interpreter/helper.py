
def DynamicListContainsDatatype(arr: list, t: type):
    for x in arr:
        if isinstance(x, t):
            return True
    return False

def getLineNumberFromExpression(expression, runner):
    return runner.source_expressions.index(expression)