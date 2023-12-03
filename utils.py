from pprint import pprint
import env
from datetime import datetime, timedelta
import regex as re
from pathlib import Path, PosixPath
import json
import variables

def get_global_value(key):
    return getattr(variables, key, None)
def chalk(s, color, bold = None):
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"
    purple = "\033[35m"
    cyan = "\033[36m"
    reset = "\033[0m"
    bold = "\033[1m" if bold else ""
    color = locals().get(color, color)
    return color + str(s) + bold + reset

def blue(x):
    return chalk(x, "blue")

def blue_colon(a, b):
    color = "blue"
    hr = chalk("-" * 20, color)
    suffix = ":"
    a = chalk(a + suffix, color, True)
    b = chalk(b, color, False) if is_string(b) else b

    print(hr)
    print(a, b)
    print(hr)
    answer = input("")
    return answer

def confirm(x):
    word = "confirm"
    return bool(blue_colon(word, x))
def map(items, fn):

    double = is_object(items) or is_nested_array(items)
    entries = items.items() if is_object(items) else items
    gn = lambda x: fn(*x) if double else fn(x)

    store = []
    for item in entries:
        try:
            value = gn(item)
            if is_defined(value):
                store.append(value)
        except Exception as e:
            print("offender", item)
            prompt("error", str(e))
        
    return store

def is_defined(x):
    return x != None

def is_array(x):
    array_types = ['list', 'tuple', 'dict_types']
    return type(x).__name__ in array_types

def test(s, r, flags = 0):
    return is_string(s) and bool(match(s, r, flags))

def is_string(x):
    return type(x) == str

def is_integer(x):
    return type(x) == int

def is_number(x):
    r = "^\d+(?:[.,]\d+)?$"
    return type(x) == int or type(x) == float or test(x, r)

def match(s, r, flags = 0):
    m = re.search(r, str(s), flags)
    if not m:
        return ""
    g = m.groups()
    if g:
        if len(g) == 1:
            return g[0]
        else:
            return g
    return m.group(0)

def get_extension(x):
    return Path(x).suffix.lstrip(".")

def has_extension(x):
    return bool(get_extension(x))

def write_json(file, content):
    assert content
    with open(normalize_file(file), "w") as f:
        json.dump(content, f, indent=4)

def append(file, content):
    assert content
    with open(normalize_file(file), "a") as f:
        f.write(to_string(content))

def write(file, content):
    assert content
    with open(normalize_file(file), "w") as f:
        f.write(to_string(content))

def npath(dir, file):
    return str(Path(dir, tail(file)))

def normalize_file(file):
    dir = dir_from_file(file)
    return npath(dir, file)

def trim(s):
    return str(s).strip()

def join(*args):
    def runner(args):
        s = ""
        for item in args:
            if is_array(item):
                s += runner(item) + "\n\n"
            else:
                delimiter = "\n\n" if test(trim(item), "\n") else "\n"
                s += item + delimiter
        
    return trim(runner(args))

        
def is_primitive(x):
    return is_string(x) or is_number(x)
def to_string(x):
    return str(x) if is_primitive(x) else join(x)
    
def append_json(file, data):
    assert data
    file = normalize_file(file)
    store = read_json(file) or [] if is_array(data) else {}
    store.extend(data) if is_array(data) else store.update(data)
    announce("appending $1 items to $2, which now has: $3 items", str(len(data)), file, str(len(store)))
    write_json(file, store)
    return file


def is_array_dictionary(x):
    return is_object(x) and is_array(x.values()[0])

def is_object_array(x):
    return is_array(x) and len(x) and is_object(x[0])

def read_json(file):
    try:
        with open(file) as f:
            return json.load(f)
    except Exception as e:
        return None

def everyf(*tests):
    def checkpoint(x):
        for test in flat(tests):
            if not test(x):
                return False
        return True
    return checkpoint

def pretty_print(x):
    return json.dumps(x, indent = 2)

def identity(x):
    return x

def head(x):
    return Path(x).parent
def tail(x):
    return Path(x).name

def dir_from_file(file):
    e = get_extension(file)
    key = e + "dir"
    return get_global_value(key) or throw("$1 does not match any directory in variables", file)

def red(x):
    return chalk(x, "red")

def throw(message, *args):
    m = red(templater(message, *args))
    raise Exception(m)
def timestamp(x=None):
    t = type(x)

    if t == datetime: return int(x.timestamp())
    if t == str: 
        p = Path(x)
        assert is_file(p)
        return int(p.stat().st_mtime)

    return int(datetime.now().timestamp())


def clear(x):
    x = normalize_file(x)
    if is_file(x):
        with open(x, "w") as f:
            pass

def is_file(x):
    if type(x) == PosixPath:
        return x.exists()
    if type(x) == str:
        return Path(x).exists()

def is_function(x):
    return callable(x)

def templater(s, *args, **kwargs):

    def fallback(x):
        y = globals().get(x)
        return y() if is_function(y) else y
        
    def parser(x):
        if is_array(ref):
            return ref[int(x) - 1] if is_number(x) else fallback(x)

        if is_object(ref):
            return ref.get(x, fallback(x))

    def runner(x):
        return parser(x.group(1))

    ref = args if is_primitive(args[0]) else args[0]
    r = "\$(\w+)"

    return re.sub(r, runner, s, kwargs.get("flags", 0))

def prompt(*args):
    return blue_colon(*args) if len(args) > 1 else input(print(args[0]))


def to_array(x):
    return x if is_array(x) else [x]

def exists(x):
    return bool(x)

def filter(items, x = exists):
    checkpoint = testf(x)
    return [el for el in items if checkpoint(el)]

s = """
[]
{}
[1,2]
0
None
1
""
"""
def split(s, r, flags = 0):
    return re.split(r, s.strip(), flags)
def run_tests(s, fn):
    items = map(split(s, "\n+"), to_argument)
    evaluations = map(items, fn)
    entries = list(zip(items, evaluations))
    for index,(a,b) in enumerate(entries):
        print(str(index + 1) + ". ", blue(a), b)

def to_argument(x):
    return eval(x)
# run_tests(s, exists)

def testf(x, flags=0, anti=0):
    fn = x if is_function(x) else lambda s: test(s, x, flags)
    if anti:
        return lambda x: not fn(x)
    else:
        return fn


def is_object(x):
    return type(x) == dict

def is_nested_array(x):
    return x and is_array(x) and is_array(x[0])

def is_today(x):
    n = x
    if hasattr(x, "created_utc"):
        n = x.created_utc

    dt = datetime.fromtimestamp(n)
    today = datetime.today()
    return dt.date() == today.date()

def datestamp(x):
    strife = "%A %B %d %Y, %-I:%M:%S%p"
    return datetime.fromtimestamp(x).strftime(strife)

def announce(message, *args):
     print(blue(templater(message, *args)))


def flat(items):
    def runner(items):
        for item in items:
            if is_array(item):
                runner(item)
            elif is_defined(item):
                store.append(item)

    store = []
    runner(items)
    return store



def get_sentences(text):
    """
    Split the text into sentences.

    If the text contains substrings "<prd>" or "<stop>", they would lead 
    to incorrect splitting because they are used as markers for splitting.

    :param text: text to be split into sentences
    :type text: str

    :return: list of sentences
    :rtype: list[str]
    """
    alphabets= "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov|edu|me)"
    digits = "([0-9])"
    multiple_dots = r'\.{2,}'
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences]
    if sentences and not sentences[-1]: sentences = sentences[:-1]
    return sentences

def is_url(x):
    return test(x, "http")

def get_constructor_name(x):
    return type(x).__name__
