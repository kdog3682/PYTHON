import env
import inspect
from base import *

def is_empty(x):
    if x == 0:
        return False

    if not x:
        return True

    if isinstance(x, (list, tuple, set, frozenset, dict)):
        return not bool(x)

    return len(x) == 0

def early_return(fn):
    def wrapper(*args, **kwargs):
        if is_empty(args[0]):
            print("early return @ empty result")
            return
        result = fn(*args, **kwargs)
        return result
    return wrapper

@early_return
def clipsave(s):
    appendjson('clip.json', [s])


class FileState:
    def __init__(self, file):
        self.file = file
        self.tail = tail(file)
        self.name = removeExtension(self.tail)
        self.extension = getExtension(file)
        self.is_zip = self.extension == 'zip'
        self.is_js = self.extension == 'js'
        self.is_py = self.extension == 'py'
        self.is_html = self.extension == 'html'
        pprint(self.file)

    def unzip(self):
        if self.is_zip:
            from zipscript import unzip
            unzip(self.file, )
    

    @property
    def data(self):
        try:
            return read(self.file)
        except Exception as e:
            print(str(e))
            return 



def smart_manager():
    
    file = glf()
    ifiz 
    return

    def runner(item, key):
        q = item.get(key)
        if q and test('^' + q, getattr(state, key)):
            return True

    keys = ['name', 'extension', 'tail', 'file']
    for item in smartItems:
        for key in keys:
            if runner(item, key):
                return item['fn'](state)

def appendVim(value, name='temp'):
    value = dumpJson(value)
    s = f"let g:{name} = {value}"
    append("/home/kdog3682/.vimrc", s)


def antichoose(items):
    assert(items)

    a = prompt2(items)
    if not a:
        return items
    indexes = [int(n) - 1 for n in a.strip().split(" ")]

    store = []
    for i, item in enumerate(items):
        if i not in indexes:
            store.append(item)
    return store

def pyargs(file='base.py'):
    name = getExtension(file) + 'args'
    items = antichoose(fa(file, '\(([a-z]\w*)\)', filter='<9'))
    appendVim(items, name=name)

def toString(s):
    if isFunction(s):
        return inspect.getsource(s)
    return str(s)

def fa(s, r, flags=0, **kwargs):
    s = s if isArray(s) else textgetter(s)
    m = re.findall(r, s, flags=flags)
    if kwargs.get('filter'):
        m = filter(m, kwargs.get('filter'))
    m = unique(m)

    if kwargs.get('choose'):
        m = antichoose(m)

    if kwargs.get('fn'):
        m = map(m, kwargs.get('fn'))

    if kwargs.get('map'):
        m = map(m, kwargs.get('map'))

    if kwargs.get('filter'):
        m = filter(m, kwargs.get('filter'))

    if kwargs.get('append'):
        if kwargs.get('append') == 'self':
            appendVariable(dumpJson(m))

    if kwargs.get('save'):
        prompt(m)
        append(currentFile(), join(m))
    return m


def map(items, x):
    f = x
    if isString(x):
        x = x.strip()
        f = lambda arg: templater(x, [arg])

    return [f(el) for el in items]


def filter(items, x):
    f = x
    if isString(x):
        if test('^[<>=]', x):
            f = eval(f"lambda x: len(x) {x}")
        else:
            f = eval(f"lambda x: {x}")

    return [el for el in items if f(el)]

#pyargs()

s = """
zip
javascript
python
html
css
"""
t = """
# This is a map Target
def is_$1(s):
    return getExtension(s) == "$1"
"""

t = """
let g:wpsnippets["$1"]["$2"] = "$3"
"""



def is_javascript(s):
    return getExtension(s) == "js"

def is_zip(s):
    return getExtension(s) == "zip"

def is_css(s):
    return getExtension(s) == "css"

def is_python(s):
    return getExtension(s) == "py"

def is_html(s):
    return getExtension(s) == "html"


class Cache:
    def __init__(self, fallback):
        self.store = {}
        self.fallback = fallback

    def get(self, k):
        m = self.store.get(k)
        if m == None:
            value = self.fallback(k)
            self.store[k] = value
            return value
        print ('returning cache')
        return m
    
        
def dictf(ref):
    def f(k):
        fn = getattr(ref, k, getattr(ref, 'default', None))
        params = count_params(fn)
        return fn, params
    cache = Cache(f)
    def runner(k, v):
        try:
            fn, params = cache.get(k)
            return fn(k) if params == 1 else fn(v, k)
        except Exception as e:
            prompt(error=str(e))
            print("---------------")
            print(str(e))
            print('error')
            dprint(k, v)
            input('throw please')
            input('throw please')
            input('throw please')
            print("---------------")
        
    return runner

def lines(s, ref=0):
    s = s.strip()
    lines = map(s.split('\n'), trim)
    if test('^ *\w+:', s, flags=re.M):
        lines = map(lines, lambda x: splitonce(x, ' *: *'))

    if ref:
        f = dictf(ref)
        lines = [f(*el) for el in lines]

    return lines

str1681989658 = """
    
    margin: 6, 12, 18, 24
    padding: 6, 12, 18, 24
    rel
    abs
    grid: 2,3,4
    directions: 6, 12, 18, 24, -6, -12, -18, -24
"""
    #colors: background color outline border-color


s = """

def fn(key, value):
    unit = 'pt'
        case 'margin':
        case 'padding':
            const numbers = getNumbers(b)
            return DIRECTIONS.forEach((d, i) => {
                dirLetter = d[0]
                nameLetter = key[0]
                name = nameLetter + dirLetter
                store.push(name, d + '-')
            })
        case 'colors':
        case 'rel':
        case 'abs':
        case 'grid':
        case 'directions':
"""

def count_params(f):
    data = inspect.signature(f)
    return len(data.parameters)
#print(lines('rel', ref=pillars))
#fa(s, '\w+', map=fn, save=1)
#len(test)
"pillars.py"

#import pillars
#pprint(flat(lines(str1681989658, ref=pillars)))


#print(SystemCommand('npm i @flatten-js/core').success)
#printdir(nodedir2023 + '@flatten-js/core/dist')
