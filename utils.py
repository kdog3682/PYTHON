dldir = "/mnt/chromeos/MyFiles/Downloads/"
rootdir = "/home/kdog3682"
tocfile = "/home/kdog3682/2024/toc.txt"
typstdir = "/home/kdog3682/GITHUB/typst"
typstpackagedir = "/home/kdog3682/GITHUB/typst-packages"
loremdir = "/home/kdog3682/LOREMDIR"
hugodir = "/home/kdog3682/2024/quickstart"
githubdir = "/home/kdog3682/GITHUB"

from pprint import pprint
import sys
import env
from datetime import datetime, timedelta
import regex as re
from pathlib import Path, PosixPath
import json
import shutil
import variables
import webbrowser

dirdict = {"active_dir": "/home/kdog3682/2023", "downloads":"/mnt/chromeos/MyFiles/Downloads","node":"/home/kdog3682/2023/node_modules","r":"/home/kdog3682","nm":"/home/kdog3682/2023/node_modules","24":"/home/kdog3682/2024","budir":"/mnt/chromeos/GoogleDrive/MyDrive/BACKUP","g":"/home/kdog3682/latest-git-cloned-repo","2024":"/home/kdog3682/2024/","py":"/home/kdog3682/PYTHON","ftp":"/home/kdog3682/.vim/ftplugin","2023":"/home/kdog3682/2023/","23":"/home/kdog3682/2023","res":"/home/kdog3682/RESOURCES","trash":"/home/kdog3682/TRASH"}
def hr(n, newline = 1):
    s = "\n" if newline else ""
    return "-" * n + s

def chalk(s, color, bold = None):
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"
    purple = "\033[35m"
    cyan = "\033[36m"
    reset = "\033[0m"
    b = "\033[1m" if bold else ""
    color = locals().get(color, color)
    return color + str(s) + b + reset

def blue(x):
    return chalk(x, "blue")

def _blue_colon(a, b):
    color = "blue"
    hr = chalk("-" * 20, color)
    suffix = ":"
    a = chalk(a + suffix, color, True)
    b = chalk(b, color, False) if is_string(b) else b

    print(hr)
    print(a, b)
    print(hr)

def blue_colon(a, b):
    _blue_colon(a, b)
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
            print("error at map()")
            print("offender", item)
            raise e
            prompt("error", str(e))
        
    return store

def is_defined(x):
    return x != None

def is_array(x):
    array_types = ['list', 'tuple', 'dict_keys']
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

def has(x, key):
    if isinstance(x, dict) and key in x:
        return True


def add_extension(x, y):
    e = get_extension(y)
    if e == "": e = y
    return x + "." + e if not has_extension(x) else x

def has_extension(x):
    return bool(get_extension(x))

def append(file, content):
    assert content
    with open(normalize_file(file), "a") as f:
        f.write(to_string(content))

def write(file, content, dir = None, ext = None, log = False):
    """
        the file is normalized with dir and ext if provided
        if content is a str, write as text
        else write as json
    """
    assert content
    filename = normalize_file(file, dir, ext)
    if is_string(content):
        with open(filename, "w") as f:
            f.write(content)
            print(f"wrote file: {filename}")
    else:
        with open(file, "w") as f:
            json.dump(content, f, indent=4)
            print(f"wrote file: {filename} as json")

    if log:
        log_file(filename)


def npath(dir, file):
    return str(Path(dir, tail(file)))

def tail(x):
    return re.sub("/$", "", str(x)).rsplit("/", maxsplit=1)[-1]

def identity(s):
    return s

def normalize_file(file, dir = None, ext = None):
    if ext:
        file = add_extension(file, ext)
    if dir:
        return npath(get_dir(dir), file)
    if test(file, "^/"):
        return file
    dir = dir_from_file(file)
    return npath(dir, file)

def trim(s):
    return str(s).strip()

def join_lines(*args):
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
    return str(x) if is_primitive(x) else join_lines(x)
    
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

def strftime(key = "iso8601", dt=None):
    templates = {
        "iso8601": "%Y-%m-%d",
        "simple_date": "%Y-%m-%d",
        "simple_time": "%H:%M:%S",
        "datetime": "%A %B %d %Y, %-I:%M:%S%p",
        # Add more templates as needed
    }

    if dt is None:
        dt = datetime.now()

    template = templates.get(key, key)
    return dt.strftime(template)

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
    def parser(x):
        if is_array(ref):
            return ref[int(x) - 1] if is_number(x) else ref.pop(0)

        if is_object(ref):
            return ref.get(x, fallback(x))

    def runner(x):
        return parser(x.group(1))

    if not args:
        return s
    ref = (list(args) if is_primitive(args[0]) else args[0])
    r = "\$(\w+)"

    return re.sub(r, runner, s, kwargs.get("flags", 0))

def prompt(*args):
    if len(args) == 1:
        print(chalk(args[0], "blue"))
        print()
        return input()
    elif is_string(args[0]):
        return blue_colon(*args)
    else:
        print("printing multiple prompt items\n")
        for arg in args:
            print(chalk(arg, "blue"))
            print("-" * 20)
        print()
        return input()


def to_array(x):
    return x if is_array(x) else [x]

def exists(x):
    return bool(x)

def filter(items, x = exists, anti = False):
    checkpoint = testf(x, anti = anti)
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
def split(s, r = "\s+", flags = 0):
    items = re.split(r, s.strip(), flags)
    return items[1:] if items[0] == "" else items
def run_tests(s, fn):
    items = map(split(s, "\n+"), eval)
    evaluations = map(items, fn)
    entries = list(zip(items, evaluations))
    for index,(a,b) in enumerate(entries):
        print(str(index + 1) + ". ", blue(a), b)


def package_manager(fn):
    def transform(x):
        if is_number(x):
            return int(x)
        if test(x.strip(), '^(?:""|\'\')$'):
            return ''
        return x

    args = sys.argv
    if len(args) > 1:
        fn(*map(args[1:], transform))

def to_argument(x):
    if is_number(x):
        return int(x)
    return x

def testf(x, flags=0, anti=0):
    if is_object(x):
        if len(x) == 1:
            a,b = list(x.items())[0]
            return lambda x: x.get(a) == b
        else:
            raise Exception("ndy")

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


#
def file_prompt():
    return prompt("choose an outpath file name")

# 

def debug(*args):
    print(*args)
    input("")
def npath(dir, file):
    return re.sub("/$", "", dir) + "/" + tail(file)

def copy_last_downloaded_file_into_active_dir():
    name = file_prompt()
    file = most_recent_file()
    active_dir = get_dir("active_dir")
    outpath = npath(active_dir, name)
    debug(file, outpath)
    shutil.copy(file, outpath)
    print("success!")
    # announce("copied last downloaded file: $1 to $2", file, outpath)

def is_dir(x):
    return Path(x).is_dir()

def get_dir(dir):
    if is_dir(dir):
        return dir
    dir = dirdict.get(dir)
    if is_dir(dir):
        return dir
    throw("not a valid directory: $1", dir)

def path(dir):
    return Path(get_dir(dir))

def most_recent_file(dir = "downloads"):
    directory = path(dir)
    files = directory.glob("*")
    target = max(files, key=lambda f: f.stat().st_ctime)
    return target


def is_jsonable(x):
    return is_array(x) or is_object(x)

def append_self(x):
    if empty(x):
        return

    value = json.dumps(x, indent=4) if is_jsonable(x) else str(x)
    append(sys.argv[0], value)



# print("Most recent file:", most_recent_file())
# print(copy_last_downloaded_file_into_active_dir())

def empty(x):
    if x == 0:
        return False
    if x:
        return False
    return True

def get_error_name(e):
    return e.__class__.__name__

def choose(x):
    items = list(x)
    if len(items) == 1:
        return items[0]

    for i, item in enumerate(items):
        print(blue(i + 1), item)

    a = input("\nchoose 1-based indexes\n")

    if a == "":
        return 

    return items[int(a) - 1]


def is_private(s):
	return test('^[._]', tail(s))

def view(file):
    webbrowser.open(file)

def openpdf(file = "/home/kdog3682/2024/test.pdf"):
    view(file)


def clip(payload, outpath = 1):
    ref = {
        1: "/home/kdog3682/2023/clip.js",
        2: "/home/kdog3682/2023/clip2.js",
        3: "/home/kdog3682/2023/clip3.js",
    }
    file = ref[outpath]
    write(file, stringify(payload))

def stringify(x):
    if empty(x):
        return 
    if type(x) == bytes:
        return x.decode()
    if is_primitive(x):
        return str(x)
    return json.dumps(x, indent=4)

def unique(a, b=None):
    if b:
        if is_array(a):
            return list(set(a).difference(b))
        if is_object(a):
            return filter(a, lambda k, v: k not in b)
    else:
        return list(set(a))

def mkdir(dir):
    dir_path = Path(dir)
    try:
        dir_path.mkdir(parents=True, exist_ok=False)
        print(f"Directory '{dir_path}' was created.")
    except FileExistsError:
        print(f"Directory '{dir_path}' already exists.")


def rglob(root):
    p = Path(root)
    results = p.rglob(key)
    list(results)

    from pathlib import Path

def get_files_recursive(root, fileRE = None, dirIgnoreRE = None):
    root_dir = Path(root)
    files = []

    def recurse(directory):
        for path in directory.iterdir():
            if path.is_dir():
                if dirIgnoreRE and test(path.name, dirIgnoreRE):
                    continue
                recurse(path)
            elif path.is_file():
                if fileRE and not test(path.name, fileRE):
                    continue
                files.append(str(path))

    recurse(root_dir)
    return files



def re_wrap(iterable, template = ''):
    ref = {
        '': '(?:$1)',
        'b': "\\b(?:$1)\\b",
    }
    template = ref.get(template, template)
    keys = list(iterable.keys() if is_object(iterable) else iterable)
    symbols = map(keys, re.escape)
    s = join(symbols, "|")
    return re.sub('\$1', s, template)


def decode(x):
    return x.decode("utf-8")


def rmdir(dir):
    shutil.rmtree(Path(dir))

def sub(s, r, rep, flags = 0):
    return re.sub(r, rep, s, flags = flags)

def join(x, delimiter = " "):
    return delimiter.join(x)


def system_command(template, *args, **kwargs):
    from subprocess import Popen, PIPE
    command = templater(template, *args, **kwargs)
    command = "; ".join(split(command.strip(), "\s*\n+\s*"))

    if env.GLOBAL_DEBUG_FLAG == 1:
        blue_colon("debugging the command", command)
    elif env.GLOBAL_DEBUG_FLAG == 2:
        return print(command)
    else:
        blue_colon("command", command)
    process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
    data = process.communicate()
    success, error = [decode(d) for d in data]
    return { "success": success, "error": error }

# clip(get_files_recursive(githubdir))
# pprint(is_dir("/usr/local/bin"))

def is_public_path(path):
    return test(path.name, "^\w")
def get_most_recent_file(directory = dldir):
    dir_path = Path(directory)
    files = filter(dir_path.iterdir(), is_public_path)
    file = max(files, key=lambda f: f.stat().st_mtime)
    return str(file)

def unzip_and_move_executable_in_progress():
    """
        used for downloading hugo but it didnt work
    """
    file = get_most_recent_file()
    filename = tail(file)
    key = match(filename, "[a-zA-Z]+")

    print(system_command(""" 
        cd $directory
        tar -xvf $file 
    """, dldir, filename))
    unzipped_file = get_most_recent_file()
    file_path = Path(unzipped_file)
    contents = list(file_path.iterdir())
    content = choose(contents)
    content_path = str(content)
    print(system_command("cp $content_path /usr/local/bin", content_path))
    key = content.name
    print(system_command(""" $key --version """, key))

def c2(x):
    clip(x, outpath = 2)

# mkdir("/home/kdog3682/PYTHON/apps/SectionExecutor.py")


def colon_dict(s):
    items = re.split("^([\w-]+): *", s.strip(), flags=re.M)
    items = map(items, trim)
    if items[0] == "":
        items.pop(0)
    config = dict(partition(items))
    return config

def partition(arr, n = 2):

    def partition_by_integer(arr, n):
        store = []
        for i in range(0, len(arr), n):
            store.append(arr[i : i + n])
        return store
    def partition_by_function(arr, f):
        store = [[], []]
        for item in arr:
            if f(item):
                store[0].append(item)
            else:
                store[1].append(item)
        return store

    if is_string(n):
        n = testf(n)
    if is_function(n):
        return partition_by_function(arr, n)
    else:
        return partition_by_integer(arr, n)

def every(a, b):
    if is_array(b):
        for item in a:
            if item not in b:
                return 
        return 1
    for item in a:
        if not b(item):
            return 
    return 1
def complete_overlap(x, y):
    a = list(x).sort()
    b = list(y).sort()
    return json.dumps(a) == json.dumps(b)


def not_none(x):
    return x != None

def is_valid(x):
    return x == 0 or x != None
def assertion(value, key = "exists", message = None):
    ref = {
        "not_none": not_none,
        "is_valid": is_valid,
        "exists": exists,
    }
    def parse(key):
        if is_function(key):
            return key
        elif key.startswith(">"):
            limit = int(match(key, "> *(.*)"))
            return lambda x: x > limit
        else:
            return ref.get(key)

    check = parse(key)(value)
    if check:
        return 
    raise CustomError(message or key)


class CustomError(Exception):
    RED = '\033[91m'
    RESET = '\033[0m'

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return red(self.message)


def reduce(items, fn):
    store = {}

    if is_object(items):
        for k, v in items.items():
            value = fn(k, v)

            if not value:
                continue
            elif is_array(value) and len(value) == 2:
                if value[1] != None:
                    store[value[0]] = value[1]
            else:
                store[k] = value
    else:
        for item in list(items):
            value = fn(item)

            if not value:
                continue
            elif is_array(value) and len(value) == 2:
                store[value[0]] = value[1]
            else:
                store[item] = value

    return store


def find(iterable, fn):
    fn = testf(fn)

    for i, item in enumerate(list(iterable)):
        if fn(item):
            return item


def read(file):
    byte_files = [
        "img",
        "jpg",
        "svg",
    ]

    e = get_extension(file)
    mode = "rb" if e in byte_files else "r"
    with open(file, mode) as f:
        return f.read()


def shared(a, b):
    return list(set(a) & set(b))


def noop(*args, **kwargs):
    return 

def default_path_ignore(path: Path) -> bool:
    """
        Used in various file finders.
        Ignores dot files and node modules
    """
    if test(path.name, "^\W|node_modules"):
        return True
    return False

def indent(x, indentation = 2):
    return sub(x, "^", " " * indentation, flags = re.M)


def remove_python_comments(s):
    return sub(s, "^#.+\n*", "", flags = re.M)


def get_kwargs(s):
    """
        there have been multiple attempts at writing this function over the years

    """
    def runner(a, b):
        return [a, to_argument(trim(b))]
    return dict(map(partition(split(s, "(\w+) *= *")), runner))

env.verify = 1
def verify(*args, **kwargs):
    """
         early returns when env.verify is not active
         
         sometimes you want to verify something before you proceed 

         2 args: (1: value, 2: message)
         n args: (n: values)

         All the values are printed out one by one
         and they are colored blue
    """
    if len(args) == 2 and not kwargs and is_string(args[1]):
        kwargs["message"] = args[1]
        args = [args[0]]
    if env.verify == 0:
        return 
    print(blue(hr(30, newline = 0)))
    for arg in args:
        print(arg)
    print(blue(hr(30)))
    if kwargs.get("message"):
        print(chalk("message:", "blue", 1), kwargs.get("message"))

# verify("foo", "a")


class blue_sandwich:
    def blue(self):
        print(blue(hr(30, False)))

    def __enter__(self):
        self.blue()

    def __exit__(self, exc_type, exc_value, traceback):
        self.blue()


def smart_dedent(s):
    s = re.sub("^ *\n*|\n *$", "", s)
    if test(s, "^\S"):
        return s
    spaces = match(s, "^ *(?=\S)", flags=re.M)
    secondLineSpaces = match(s, "\n *(?=\S)")
    if (
        not spaces
        and secondLineSpaces
        and len(secondLineSpaces) > 4
    ):
        return re.sub(
            "^" + secondLineSpaces[5:], "", s, flags=re.M
        ).trim()

    return re.sub("^" + spaces, "", s, flags=re.M).strip()


def write_git_ignore(dir):
    """
        fn_degree: 2
        writes the .gitignore
        todo: python or javascript gitignore
    """
    assert(is_dir(dir))

    patterns = choose_dict_item(env.git_ignore_patterns)
    if patterns:
        write(".gitignore", join(patterns), dir = dir)

def log_file(file):
    """
        fn_degree: 2
        creates a string that lookes like this:
        2024-01-11 /home/kdog3682/2023/lezer-runExampleFile.js

        linked to function:write via kwargs.log
    """
    s = strftime("iso8601") + " " + file + "\n"
    append("/home/kdog3682/2024/files.log", s)


def force_write(*args, **kwargs):
    """
        fn_degree: 2
        args: [string]
        kwargs: {content?: string}

        the args join together to form the final path
        the text value is kwargs.content or "howdy"

        return: None
    """

    content = kwargs.get("content", "howdy")
    path = Path(*args)
    if not path.parent.is_dir():
        path.parent.mkdir(parents=True, exist_ok=False)

    filename = path.resolve()
    with open(path.resolve(), "w") as f:
        f.write(content)
        print("wrote", filename)
    file_log(filename)


def is_private_filename(s):
	return test('^[._]', tail(s))

def read_bytes(f):
    with open(f, "rb") as f:
        return f.read()


def getErrorMessage(e):
    s = search('"message": "(.*?)"', str(e))
    return re.sub('\.$', '', s.strip())

def breaker(n=10):
    env.breaker_count += 1
    if env.breaker_count >= n:
        raise Exception()


def reverse(x):
    if isObject(x):
        return {b:a for a,b in x.items()}
    return list(reversed(x))


ignore_patterns = {
        'python': ['__pycache__/', '*.py[cod]', '*$py.class', '.pytest_cache/', 'venv/', 'env/', '.idea/', '*.sqlite3', '*.ipynb_checkpoints'],
        'java': ['target/', 'bin/', '*.log', '*.class', '.idea/', '*.jar', '*.war'],
        'javascript': ["env.js", "package-lock.json", 'node_modules/', 'npm-debug.log', 'dist/', '.env', 'logs', '*.log', 'npm-debug.log*', 'yarn-debug.log*', 'yarn-error.log*'],
        'cpp': ['*.o', '*.obj', '*.exe', '*.dll', '*.so', '*.dylib', 'bin/', 'obj/', '.vscode/'],
        'ruby': ['*.gem', '.bundle/', 'log/', 'tmp/', 'vendor/bundle/', '.env', '*.rbc', 'capybara-*.html', '.rspec', '/db/*.sqlite3', '/db/*.sqlite3-journal', '/public/system', '/coverage/', 'spec/tmp*', '**.orig', 'rerun.txt', 'pickle-email-*.html'],
        'go': ['bin/', 'pkg/', '*.o', '*.a', '*.so', 'dist/', 'build/', '.env', 'vendor/']
}

def choose_dict_item(ref):
    return ref.get(choose(list(ref)))



def get_git_status_and_last_modified(directories):
    import os
    import subprocess
    git_info = {}
    o = ""

    for dir_path in directories:
        if not is_git_directory(dir_path):
            continue

        o += dir_path + "\n"
        os.chdir(dir_path)
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        status_lines = result.stdout.splitlines()

        files = []
        ref = {
           '??': 'created',
           'M': 'modified',
        }
        for line in status_lines:
            status, file_path = line[:2].strip(), line[3:].strip()
            if not file_path:
                continue
            if not is_file(file_path):
                continue
            status = ref.get(status, status)
            mtime = os.path.getmtime(file_path)
            dt = datetime.fromtimestamp(mtime)
            expr = pluralize_unit(days_ago(dt), "days")
            last_modified = strftime("datetime", dt)
            last_modified += f" ({expr} ago)"
            s = {
                'name': tail(file_path),
                'date': status + " " + last_modified,
            }
            files.append(s)
            for k,v in s.items():
                o += f"  {k}: {v}\n"
            o += "\n"

        o += "\n\n"
        # git_info.append({"dir": dir_path, "contents": files})

    outpath = "/home/kdog3682/2024/git-status.01-14-2024.txt"
    write(outpath, o)

def is_git_directory(dir_path):
    return Path(dir_path, ".git").is_dir()

def days_ago(target_datetime):
    """
    Calculate how many days ago a given datetime was from the current date.

    :param target_datetime: A datetime object representing the past date and time.
    :return: Number of days as an integer.
    """
    current_datetime = datetime.now()
    # print(strftime(dt = current_datetime))
    # print(strftime(dt = target_datetime))
    delta = current_datetime - target_datetime
    return delta.days + 1

def ordinal(number):
    """
    Convert a number into its ordinal representation.

    :param number: An integer number.
    :return: A string representing the ordinal form of the number.
    """
    if 10 <= number % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')

    return f"{number}{suffix}"

def pluralize_unit(n, unit):
    """
    Return a string with 'day' or 'days' correctly pluralized based on the number.

    :param n: An integer number representing the number of days.
    :return: A string with the number and 'day' or 'days'.
    """
    unit = sub(unit, "s$", "")
    if n == 1:
        return f"{n} {unit}"
    else:
        return f"{n} {unit}s"


directories = [
"/home/kdog3682/2024/", "/home/kdog3682/2023/", "/home/kdog3682/.vim/ftplugin/", "/home/kdog3682/PYTHON/"
]
# get_git_status_and_last_modified(directories)

def git_push_directories(*args):
    template = """
        cd $1
        git add .
        git commit -m 'pushing directory'
        git push
    """

    for dir in flat(args):
        print(system_command(template, dir))

git_push_directories(directories)
