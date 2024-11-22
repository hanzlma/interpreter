import re
operators = {
    "plus" : '+',
    "minus": '-',
    "multiply": '*',
    "divide": '/',
    "and": '&&',
    "or": '||',
    "equal": '==',
    "not_equal": '!=',
    "greater_than": '>',
    "lower_than": '<',
    "greater_equal": '>=',
    "lower_equal": '<='
}

def SplitByOperators(string: str) -> list[str]:
    split1: list[str] = re.split(r'(?<=\s)(\+|\-|\*|\/|&&|\|\||==|!=|>|<|>=|<=)(?=\s)', string)
    return [part.strip() for part in split1 if not re.match(r'^(\+|\-|\*|\/|&&|\|\||==|!=|>|<|>=|<=)$', part.strip())]

def GetOperatorsFromText(string: str) -> list[str]:
    operatorOccurencies: dict[int, str] = {}
    for operator in re.finditer(r'(?<=\s)(\+|\-|\*|\/|&&|\|\||==|!=|>|<|>=|<=)(?=\s)', string):
        operatorOccurencies[operator.start()] = operator[0]
    operatorOccurencies = {key: operatorOccurencies[key] for key in sorted(operatorOccurencies)}
    output: list[str] = []
    for occurency in list(operatorOccurencies.values()):
        output.append(occurency.strip())
    return output
