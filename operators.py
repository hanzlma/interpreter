import re
operators = {
    "plus" : '+',
    "minus": '-',
    "multiply": '*',
    "divide": '/',
    "and": '&&',
    "or": '||'
}

def SplitByOperators(string: str) -> list[str]:
    split1: list[str] = re.split('\+|-|\*|/|&&|\|\|', string)
    output: list[str] = []
    for x in split1:
        output.append(x.strip())
    return output

def GetOperatorsFromText(string: str) -> list[str]:
    operatorOccurencies: dict[int, str] = {}
    for operator in re.finditer('\+|-|\*|/|&&|\|\|', string):
        operatorOccurencies[operator.start()] = operator[0]
    operatorOccurencies = {key: operatorOccurencies[key] for key in sorted(operatorOccurencies)}
    output: list[str] = []
    for occurency in list(operatorOccurencies.values()):
        output.append(occurency)
    print(operatorOccurencies)
    return output
