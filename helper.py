import inspect

def DynamicListContainsDatatype(arr: list, t: type):
    for x in arr:
        if isinstance(x, t):
            return True
    return False

def get_class_from_frame(fr):

    args, _, _, value_dict = inspect.getargvalues(fr)
  # we check the first parameter for the frame function is
  # named 'self'
    if len(args) and args[0] == 'self':
        instance = value_dict.get('self', None)
        if instance:
            return getattr(instance, '__class__', None)
    return None

def getRunnerInstance():
    instance = None
    stack = inspect.stack()
    for x in range(len(stack)):
        instance = get_class_from_frame(stack[x][0])
        #print(instance)
        if str(instance).find('Runner') != -1:
            return instance
    raise