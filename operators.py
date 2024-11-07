operators = {
    "plus" : '+',
    "minus": '-',
    "multiply": '*',
    "divide": '/',
    "and": '&&',
    "or": '||'
}

def SplitByOperators(string: str) -> list[str]:
    split1 = string.split(operators['plus'])
    split2: list[str] = []
    for x in split1:
        split2.extend(x.split(operators['minus']))
    split3: list[str] = []
    for x in split2:
        split3.extend(x.split(operators['multiply']))
    split4: list[str] = []
    for x in split3:
        split4.extend(x.split(operators['divide']))
    output: list[str] = []
    for x in split4:
        output.append(x.strip())
    return output

def GetOperatorsFromText(string: str) -> list[str]:
    operatorOccurencies: dict[int, str] = {}
    previousIndex: int = 0
    for i in range(string.count(operators['plus'])):
        index = string.index(operators['plus'], previousIndex)
        operatorOccurencies[index] = operators['plus']
        previousIndex = index + 1
    previousIndex = 0
    for i in range(string.count(operators['minus'])):
        index = string.index(operators['minus'], previousIndex)
        operatorOccurencies[index] = operators['minus']
        previousIndex = index + 1
    previousIndex = 0
    for i in range(string.count(operators['multiply'])):
        index = string.index(operators['multiply'], previousIndex)
        operatorOccurencies[index] = operators['multiply']
        previousIndex = index + 1
    previousIndex = 0
    for i in range(string.count(operators['divide'])):
        index = string.index(operators['divide'], previousIndex)
        operatorOccurencies[index] = operators['divide']
        previousIndex = index + 1
    previousIndex = 0
    operatorOccurencies = {key: operatorOccurencies[key] for key in sorted(operatorOccurencies)}
    output: list[str] = []
    for occurency in list(operatorOccurencies.values()):
        output.append(occurency)
    print(operatorOccurencies)
    return output
