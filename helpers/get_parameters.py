import inspect

def get_parameters(fn):
    signature = str(inspect.signature(fn))
    raw = signature[1:-1].split(', ')
    args = []
    kwargs = []
    for arg in raw:
        if '*' in arg:
            continue
        if '=' in arg:
            kwargs.append(arg.split('=')[0])
        else:
            args.append(arg)

    return [args, kwargs]
