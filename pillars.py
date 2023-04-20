
from cabmap import cabmap
UNIT = 'pt'
dirs = [
    "top",
    "right",
    "bottom",
    "left",
]
from base import *


def foo(*args, **kwargs):
    print(args, kwargs)
    return 'hi'


def default(*args):
    return 'asdfadf'


s = """
    margin: 6, 12, 18, 24
    padding: 6, 12, 18, 24
    colors: background color outline border-color
    rel
    abs
    center
    reset
    directions: 6, 12, 18, 24, -6, -12, -18, -24
"""


def css_entry(*args):
    size = len(args)

    if size == 4:
        attr, dir, n, unit = args
        return f"{attr}-{dir}: {n}{unit};"

    if size == 2:
        attr, n = args
        return f"{attr}: {n};"

def indent(s):
    return re.sub('^', '    ', s, flags=re.M)

def brackify(s):
    return f"{{\n{indent(s)}\n}}"

def css_name(s):
    return '.' + s
def css_string(name, s):
    return f"{css_name(name)} {brackify(s)}"

def margin(s):
    return pooler(s, 'margin')

def add_unit(v, k=0):
    ignore = [
        "z-index",
        "line-height",
    ]

    if k in ignore:
        return v
    if test('\d$', v):
        return v + UNIT
    return v

def css_group(name, *args):
    f = lambda k,v: css_entry(k, add_unit(v, k))
        
    s = [f(*arg) for arg in args]
    s = join(s)
    return css_string(name, s)

def css(name, k, v):
    return css_string(name, css_entry(k, add_unit(v, k)))

def pooler(s, attr):
    numbers = fa(s, 'integers')

    def fn(dir, n):
        name = attr[0] + dir[0] + str(n)
        attrKey = attr + '-' + dir
        unit = str(n) + '-' + UNIT
        s = css_entry(attrKey, unit)
        return css_string(name, s)

    return cross(dirs, numbers, fn)

def args_and_func(args):
    if args and isinstance(args[-1], type(lambda: None)):
        func = args[-1]
        args = list(args[:-1])
        return args, func
    else:
        return args, None


def cross(*args):
    import itertools
    args, func = args_and_func(args)
    items = list(itertools.product(*args))
    return map(items, func)

def padding(s):
    return pooler(s, 'padding')

def colors(s):
    items = fa(s, '[\w-]+')
    def fn(attr, color):
        alias = get_alias(attr)
        index = ''
        name = alias + color[0] + index
        return css(name, attr, color)
    return cross(items, roygbiv, fn)

def getIntegers(s):
    return re.findall('-?\d+(?=[\'\",])')

aliases = {
    'background': 'bg',
    'color': 'c',
    'outline': 'o',
}
def get_alias(s):
    return aliases[s]

#pprint(padding('23 45'))
roygbiv = [
    "red",
    "orange",
    "yellow",
    "green",
    "blue",
    "indigo",
    "violet",
    "white",
    "black",
    "purple",
    "pink",
]
def directions(s):
    items = fa(s, 'integers')
    def fn(dir, item):
        return css_group(
            dir[0] + str(item), 
            (dir, item),
            ('position', 'absolute')
        )
    return cross(dirs, items, fn)

def default(k):
    return css_group(k, *cabmap.get(k))

#pprint(directions('24'))
#pprint(colors('background outline'))
#import sympy

def fn(k, v):
    if isString(v):
        return partition(split(v, ' *[:;] *'))
    if isObject(v):
        return list(v.items())
    if not isNestedArray(v):
        return [v]
    return [k, v]
#x = eval(read('clip.js'))
#x = reduce(x, fn)
#appendVariable(x, name='cabmap')

pprint(default('reset'))
