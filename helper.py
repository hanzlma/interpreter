def DynamicListContainsDatatype(arr: list, t: type):
    for x in arr:
        if isinstance(x, t):
            return True
    return False