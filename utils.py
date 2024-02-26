"""
    we are not using 2024-python it seems ...
    we are still working in this directory
"""
from setup import *

def hr(n = 30, newline = 0):
    s = "\n" if newline else ""
    return "-" * n + s

def chalk(s, color = "", bold = None):
    color = env.chalk_colors.get(color)
    reset = env.chalk_colors.get("reset")
    bold = env.chalk_colors.get("bold") if bold else ""
    return color + stringify(s) + bold + reset

def blue(x, bold = 0):
    return chalk(x, color = "blue", bold = bold)

def blue_colon(a, b):
    print(blue(a, 0), ":", blue(b, 0))

def map(items, fn):
    """
        items (list|dict)
        the fn is always spread for entries and dicts

        it is rather inflexible
        for flexiblity and enumeration, use a comprehension
    """
    double = is_object(items) or is_nested_array(items)
    entries = items.items() if is_object(items) else items
    gn = lambda x: fn(*x) if double else fn(x)

    store = []
    for item in entries:
        try:
            push(store, gn(item))
        except Exception as e:
            kwargs = get_local_kwargs("e, item")
            inform(kwargs, header = "an error has occured")
    return store

def push(store, item):
    if is_defined(item):
        store.append(item) 

def is_defined(x):
    return x != None

def is_array(x):
    try:
        array_types = ['list', 'tuple', 'dict_keys']
        return type(x).__name__ in array_types
    except Exception as e:
        return False
    

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
    if x in env.file_extensions:
        return x
    return Path(x).suffix.lstrip(".")

def has(x, key):
    try:
        return key in x
    except Exception as e:
        return False

def add_extension(x, y):
    e = get_extension(y)
    if e == "": e = y
    return x + "." + e if not has_extension(x) else x

def has_extension(x):
    return bool(get_extension(x))

def append(file, content):
    assert content
    with open(normalize_file(file), "a") as f:
        f.write(stringify(content))

def write(file, content, dir = None, ext = None, log = False, ask = 0, openIt = 0):
    """
        the file is normalized with dir and ext if provided
        if content is a str, write as text
        else write as json
    """
    assert content
    filename = normalize_file(file, dir, ext)
    if ask:
        print(content) if is_string(content) else pprint(content)
        if not input("do you wish to write this content?"):
            return

    if is_string(content):
        with open(filename, "w") as f:
            f.write(content)
            print(f"wrote file: {filename}")
    else:
        with open(file, "w") as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
            print(f"wrote file: {filename} as json")

    if log:
        log_file(filename)
    if openIt:
        view(filename)


def npath(dir, file):
    return str(Path(dir, tail(file)))

def identity(s):
    return s

def normalize_file(file, dir = None, ext = None):
    if ext:
        file = add_extension(file, ext)
    if dir:
        return npath(get_dir(dir), file)

    if test(file, "^~"):
        file = sub(file, "^~", "/home/kdog3682")

    if test(file, "^/"):
        return file

    def dir_from_file(file):
        filetype = get_filetype(file)
        return env.dirdict.get(filetype, env.dirdict.get("default"))
        
    return npath(dir_from_file(file), file)

def trim(s):
    return str(s).strip()

def join_lines(*args):
    def runner(args):
        s = ""
        for item in args:
            if is_array(item):
                s += runner(item) + "\n\n"
            else:
                item = str(item)
                delimiter = "\n\n" if test(trim(item), "\n") else "\n"
                s += item + delimiter
        
    return trim(runner(args))

        
def is_primitive(x):
    return is_string(x) or is_number(x)

    
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
        print(e)
        return None

def everyf(*tests):
    def checkpoint(x):
        for test in flat(tests):
            if not test(x):
                return False
        return True
    return checkpoint


def head(x):
    return Path(x).parent

def tail(x):
    return Path(x).name

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
    def on_error(x):
        return f"Error: Key {x} not found"

    def parser(x):
        if is_array(ref):
            return ref[int(x) - 1] if is_number(x) else ref.pop(0)
        if is_object(ref):
            return stringify(ref.get(x), indent = 0) or on_error(x)

    def runner(x):
        return parser(x.group(1))

    if not args:
        return s
    ref = (list(args) if is_primitive(args[0]) else args[0])
    r = "\$(\w+)"

    return re.sub(r, runner, s, kwargs.get("flags", 0))

def prompt(*args):
    if len(args) == 1:
        pprint(args[0])
        return input()
    elif is_string(args[0]):
        blue_colon(*args)
        return input()
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

def filter(items, x = exists, anti = False, flags = 0):
    checkpoint = testf(x, anti = anti, flags = flags)
    return [el for el in items if checkpoint(el)]

def split(s, r = "\s+", flags = 0):
    base = re.split(r, s.strip(), flags = flags)
    items = map(base, trim)

    if items[0] == "":
        items.pop(0)
    if items[-1] == "":
        items.pop(-1)
    return items

def package_manager(fn):
    """
        i have messed around and broken some things in here
    """
    def transform(x):
        if is_number(x):
            return int(x)
        if test(x.strip(), '^(?:""|\'\')$'):
            return ''
        return x

    args = sys.argv
    if len(args) > 1:
        fn(*map(args[1:], transform))
    else:
        print("package manager is not active")

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

    fn = x if is_function(x) else lambda s: test(s, x, flags = flags)
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



def is_url(x):
    return test(x, "http")

def get_constructor_name(x):
    return type(x).__name__


def is_dir(x):
    return x and Path(x).is_dir()

def get_dir(dir):
    if is_dir(dir):
        return dir
    dir = env.dirdict.get(dir)
    if is_dir(dir):
        return dir
    panic("not a valid directory: $dir")

def path(dir):
    return Path(get_dir(dir))

def most_recent_file(dir = "downloads"):
    directory = path(dir)
    files = directory.glob("*")
    target = max(files, key=lambda f: f.stat().st_mtime)
    return target


def is_json_parsable(x):
    return is_string(x) and test(x, "^\s*[\{\[]") and test(x, "[\}\]]\s*$")

def is_jsonable(x):
    return is_array(x) or is_object(x)

def append_self(x):
    if empty(x):
        return

    value = dump_json(x) if is_jsonable(x) else str(x)
    append(sys.argv[0], value)

def dump_json(x, indent = 4):
    return json.dumps(x, indent=indent, ensure_ascii=False)

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

def open_url(x):
    webbrowser.open(x)

def ofile(file):
    webbrowser.open(file)

def view(file):
    webbrowser.open(file)

def openpdf(file = "/home/kdog3682/2024/test.pdf"):
    view(file)


def clip(*args, outpath = 1, openIt = 0):
    if len(args) == 0:
        try:
            return read_json("/home/kdog3682/2023/clip.js")
        except Exception as e:
            return read("clip.js")

    payload = args[0]
    ref = {
        1: "/home/kdog3682/2023/clip.js",
        2: "/home/kdog3682/2023/clip2.js",
        3: "/home/kdog3682/2023/clip3.js",
    }
    file = ref[outpath]
    write(file, stringify(payload), openIt = openIt)

def stringify(x, indent = 4):
    if empty(x):
        return ""
    if type(x) == bytes:
        return x.decode()
    if is_primitive(x) or is_function(x):
        return str(x)
    try:
        return dump_json(x, indent = indent)
    except Exception as e:
        return get_constructor_name(x)
    

def unique(a, b=None):
    if b:
        if is_array(a):
            return list(set(a).difference(b))
        if is_object(a):
            return filter(a, lambda k, v: k not in b)
    else:
        return list(set(a))

def mkdir(dir):
    path = Path(dir)
    try:
        path.mkdir(parents=True, exist_ok=False)
        print(f"Directory '{path}' was created.")
    except FileExistsError:
        print(f"Directory '{path}' already exists.")

    return str(path)


def re_wrap(iterable, template = ''):
    ref = {
        '': '(?:$1)',
        'start': '^(?:$1)\\b',
        'b': "\\b(?:$1)\\b",
        'bc': "\\b($1)\\b",
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

def sub(s, r, rep, flags = 0, count = 0):
    return re.sub(r, rep, s, flags = flags, count = count)

def join(x, delimiter = " "):
    return delimiter.join(x)


def system_command(template, *args, **kwargs):
    from subprocess import Popen, PIPE
    command = smart_dedent(templater(template, *args))

    if env.GLOBAL_DEBUG_FLAG or kwargs.get("confirm"):
        inform("""
            this is the system_command to be executed:
            ------------
            $command
            ------------
        """)
    else:
        blue_colon("command", command)

    process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
    data = process.communicate()
    success, error = [decode(d) for d in data]
    return { "success": success, "error": error }

def is_public_path(path):
    return test(path.name, "^\w")

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

def assertion(value, key = "exists", message = None, anti = 1):
    ref = {
        "not_none": not_none,
        "is_valid": is_valid,
        "exists": exists,
    }
    def parse(key):
        if is_function(key):
            if anti:
                return lambda x: not key(x)
            return key
        elif key.startswith(">"):
            limit = int(match(key, "> *(.*)"))
            return lambda x: x > limit
        elif key.startswith("<"):
            limit = int(match(key, "< *(.*)"))
            return lambda x: x < limit
        else:
            return ref.get(key)

    check = parse(key)(value)
    if check:
        return 
    raise CustomError(message or key)


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
    byte_files = [ "img", "jpg", "svg", ]
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


def remove_extension(s):
    return re.sub("(?:\.json)?\.\w+$", "", s)
    
def remove_python_comments(s):
    return sub(s, "^#.+\n*", "", flags = re.M)


def get_kwargs(s):

    """
        abc = def, ghi = 123 -> 
        abc = def ghi = 123 -> 
    """

    def runner(a, b):
        return [a, to_argument(trim(b))]
    items = split(s, "(?:, *)?(\w+) *= *")
    return dict(map(partition(items), runner))

class blue_sandwich:
    def blue(self):
        print(blue(hr(30)))

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

    content = kwargs.get("content", "")
    path = Path(*args)
    if not path.parent.is_dir():
        path.parent.mkdir(parents=True, exist_ok=False)

    filename = path.resolve()
    with open(path.resolve(), "w") as f:
        f.write(content)
        print("wrote", filename)
    file_log(filename)


def file_log(file):
    content = str(timestamp()) + " " + file
    append("/home/kdog3682/2024/files.log", content)
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
    if is_object(x): return {b:a for a,b in x.items()}
    return list(reversed(x))



def choose_dict_item(ref):
    return choose(ref.values())

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

def get_frame_locals(degree = 1):
    frame = inspect.currentframe()
    for i in range(degree + 1):
        frame = frame.f_back
    return frame.f_locals

def printf(s, degree = 1):
    return templater(smart_dedent(s), get_frame_locals(degree)) if is_string(s) and "$" in s else s

def panic(s):
    raise Exception(printf(s, degree = 2))

def inform(s, accept_on_enter = 0, header = "inform"):
    message = printf(s, degree = 2)
    with blue_sandwich():
        print(header + ":")
        print("")
        print(message)
        print("")

    if accept_on_enter:
        print("press enter to confirm the response. (you must press the enterkey)")
    else:
        print("press anything to continue")

    answer = input()
    if accept_on_enter and answer == "":
        return 1
    return 0


def ask(s):
    print(printf(s, degree = 2))
    return input()

def tally(items):
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1

    return counts

def get_last(x):
    return x[-1]
def get_local_kwargs(s, degree = 1):
    """
        permits string programming (usually a bad idea)
        first used in map() to see the error
    """
    keys = xsplit(s)
    locals = get_frame_locals(degree)
    return {key: locals.get(key) for key in keys}


def xsplit(x, r="[,|] *| +"):
    """
        if the input is an array, return it
        splits on commas and pipes and spaces
        does not split on newlines
        does not split on anything else
    """
    assertion(x, has_newlines, anti = 1)
    return split(x, r) if is_string(x) else x


def get_filetype(x):
    return env.filetype_aliases.get(get_extension(x)) or panic("key: [$x] could not be found as a filetype in env.filetype_aliases")

def check(*keys):
    blue("checking keys")
    prompt(json.dumps(get_local_kwargs(keys, degree = 2)))

def press_anything_to_continue():
    input("press anything to continue")

def sort(x, f=None, reverse=0):
    sorter = lambda x: x.get(f) if is_string(f) else int if is_number(x[0]) else str 
    return sorted(list(x), key=f, reverse=reverse)


def cpfile(a, b):
    return copy_file(a, npath(head(a), add_extension(b, a)))


def copy_file(a, b):
    shutil.copy(str(a), str(b))
    print(f"copied {a} to {b}")


def remove_file(file):
    path = Path(file)
    print(f"removing file permanently: {path}")
    return path.unlink()

def rename_file(file, name = None):
    name = name if name else ask("choose a new name for: $file")
    path = Path(file)
    return str(path.with_name(name + path.suffix))

def move_file(file, dest):
    shutil.move(str(file), str(dest))
    print(f"moved {file} to {dest}")

def trash(file):
    move_file(file, "/home/kdog3682/TRASH/")

def anti_choose(items):

    for i, item in enumerate(items):
        print(blue(i + 1), item)

    message = 'anti_choose 1 based indexes: (space-delimited)'

    answers = split(input().strip(), "\s+")
    if not answers:
        return items
    indexes = [int(n) - 1 for n in answers]

    store = []
    for i, item in enumerate(items):
        if i not in indexes:
            store.append(item)
    return store

def printdir(dir):
    pprint(listdir(dir))


def yes(*args, **kwargs):
    return True
    
def listdir(dir, *checkpoints):
    def checkpoint(f):
        for checkpoint in checkpoints:
            if not checkpoint(f):
                return 
        return 1
    return filter(list(Path(dir).iterdir()), checkpoint)

def dash_split(s):
    return filter(map(re.split("^-{20,}", s, flags = re.M), trim))

def has_newlines(s):
    return test(s, "\n")

def split_once(s, r):
    return match(s, f"(.*?){r}([\w\W]+)") or [s, ""]


def dreplace(s, dict, flags=0, template=''):
    regex = re_wrap(dict, template)
    def parser(x):
        return (
            dict.get(x.group(1))
            if x.groups()
            else dict.get(x.group(0))
        )
    return sub(s, regex, parser, flags)

def shellunescape(s):
    if not is_string(s):
        return s
    if 'zz' not in s:
        return s

    s = dreplace(s, shellescapedict, template="zz($1)")
    return parse_json(s)

def parse_json(x):
    if is_string(x):
        return json.loads(x) if test(x, "^[{\[]") else x
    return x

class CD:

    def __init__(self, newPath=None):
        if not newPath:
            newPath = os.getcwd()
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def get_file_info(file):
    path = Path(file)
    if not path.exists():
        return 
    stats = path.stat()
    size = stats.st_size
    timestamp = stats.st_mtime
    return {
        "name": path.name,
        "size": size,
        "date": timestamp,
        # "date": strftime("iso8601", datetime.fromtimestamp(timestamp)),
    }



def to_timestamp(date):
    return datetime.strptime(date, "%Y-%m-%d").timestamp()

# data = map(listdir(dldir), get_file_info)
# clip(sort(data, lambda x: x.get("date")))
# pprint(most_recent_file("/home/kdog3682/2023/"))


def line_getter(s):
    return s if is_array(s) else map(s.strip().split("\n"), trim)

def get_files(dir, ext = None):
    def checkpoint(path):
        if ext:
            return get_extension(path) == ext
        else:
            return path.is_file()
    return map(listdir(dir, checkpoint), str)

def findall(s, r, flags = 0):
    return re.findall(r, s, flags = flags)



def remove_chinese_accents(input_text):
    import unicodedata
    nfkd_form = unicodedata.normalize('NFKD', input_text)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode('ASCII')

def run_tests(s, *scopes):
    def runner(item):
        result = eval(item, *scopes)
        pprint({"item": item, "result": result})
    map(line_getter(remove_comments(s)), runner)

def remove_comments(s):
    return sub(s, "^#.+\n*", "", flags = re.M)

def quote(s, d = "\""):
    return f"{d}{s}{d}"

def sympify_wrapper(s):
    if test(s, "//"):
        s = join(map_templater(split(s, "//"), "($1)"), " / ")
    return sub(s, "(\w)x", lambda x: x.group(1) + " * x")

def replace_quotes(s, fn):
    return sub(s, "\"(.*?)\"", lambda x: quote(fn(x.group(1))))

def map_templater(items, template):
    def fn(item):
        return templater(template, item.strip())
    return [fn(item) for item in items]


# apps.py

def most_recent_file_groups(dir=dldir, minutes=3):
    base_files = Path(dir).glob("*")
    paths = reverse(sort(base_files, lambda f: f.stat().st_mtime))
    store = []
    last_date = 0
    ignore = []

    for path in paths:
        if test(path.name, '\(\d\)') or path.name in ignore:
            continue
        file_date = path.stat().st_mtime
        d = abs(file_date - last_date)
        limit = to_seconds(minutes=minutes)
        passes = d < limit or last_date == 0
        if passes:
            store.append(path)
        else:
            return reverse(map(store, str))
        last_date = file_date

def to_seconds(
    minutes=0, hours=0, seconds=0, days=0, weeks=0, months=0
):
    return (
        seconds
        + minutes * 60
        + hours * 3600
        + days * 3600 * 24
        + months * 3600 * 24 * 30
    )



def rpw(file, fn):
    data = read_json(file) if get_extension(file) ==  "json" else read(file)
    value = fn(data)
    write(file, value, ask = 1)

def merge_objects_if_key_missing(objects, key = "chinese"):
    store = []

    last_object_with_key = None

    for obj in objects:
        if key in obj:
            store.append(obj)
            last_object_with_key = obj
        else:
            if last_object_with_key is not None:
                last_object_with_key.update(obj)
            else:
                store.append(obj)

    return store


def dot_backup(file):
    outpath = str(head(file)) + "." + str(tail(file))
    copy_file(file, outpath)

def walk(x, fn):
    def walker(x, key=None, depth=0):
        new_depth = depth + 1
        
        if is_array(x):
            items = [walker(y, key, new_depth) for y in x]
            return [item for item in items if item is not None]

        if is_object_literal(x):
            o = {}
            for a, b in x.items():
                new_value = walker(b, a, new_depth)
                if new_value is not None:
                    o[a] = new_value
            return o if o else None

        value = fn(x, key, depth)
        return value if value is not None else x

    return walker(x)

def is_object_literal(x):
    return isinstance(x, dict)

def remove_javascript_comments(s):
    return sub(s, "^ *//.*", "", flags = re.M)


def merge(*input):
    base = input if len(input) > 1 else input[0]
    assert base
    array = is_array(base[0])
    store = [] if array else {}

    for arg in base:
        if not arg:
            continue
        store.extend(arg) if array else store.update(arg)
    return store


def splice(items, start, delete_count=None):
    """
    Removes elements from a list and returns the removed elements.

    :param items: The list from which elements will be removed.
    :param start: The zero-based location in the list from which to start removing elements.
    :param delete_count: The number of elements to remove.
    :return: A list containing the removed elements.
    """
    # Adjust negative start index
    if start < 0:
        start = max(0, start + len(items))

    # Determine the end index for removal
    if delete_count is not None:
        end = start + delete_count
    else:
        end = len(items)

    # Extract the elements to be removed
    removed_elements = items[start:end]

    # Remove the elements from the original list
    items[start:end] = []

    return removed_elements

# items = [1, 2, 3, 4, 5, 6]
# print(splice(items, -3))  # Output: [4, 5, 6]
# print(splice(items, 1, 2))  # Output: [2, 3]
# print(items)  # Output: [1, 6]

def text_getter(s):
    return read(s) if is_file(s) else s

def dictify(x, regex = None):
    s = text_getter(x).strip()
    regexes = [
        "^(\S+):", 
        "^[#/]+ *(\S+)",
    ]

    if regex == None:
        regex = find(regexes, lambda regex: test(s, regex))

    items = partition(split(s, regex, flags = re.M))
    return dict(items)

def copy_files(files, dest):
    map(files, lambda x: copy_file(x, dest))

def remove_files(files):
    map(files, remove_file)

temp = [
    "/home/kdog3682/2024-chrome-extensions/web-nanny/0.0.1/manifest.json",
    "/home/kdog3682/2024-chrome-extensions/web-nanny/0.0.1/background.js",
    # "*://*/*"
    "/home/kdog3682/2024-chrome-extensions/web-nanny/0.0.2/manifest.json",
    "/home/kdog3682/2024-chrome-extensions/web-nanny/0.0.2/background.js",
    "/home/kdog3682/2024-chrome-extensions/web-nanny/0.0.2/options.html",
    "/home/kdog3682/2024-chrome-extensions/web-nanny/0.0.2/options.js",
]

def file_creator(file):
    dir = "/home/kdog3682/2024-writing/math/"
    mkdir(dir)
    cd(dir)

    if is_file(npath(dir, file)):
        print("the file already exists in this directory")
        print("early return")

    data = {
        **multi_prompt("grade", "name", "topic", "desc", "prereqs"),
        'file': file,
    }
    append_json("index.json", [data])
    mkdir(dir)

def multi_prompt(*args, **kwargs):
    return {k: prompt("choose a value for: " + str(k)) for k in args}


def cpdir(src, to):
    shutil.copytree(src, to)
    print(f"copying directory: {src} to {to}")

def typst_manager():
    a = "/home/kdog3682/GITHUB/typst-packages/packages/preview/"
    package = choose(listdir(a))
    name = tail(package)
    version = tail(most_recent_file(package))
    srcpath = str(Path(package, version))
    outpath = f"/home/kdog3682/.cache/typst/packages/preview/{name}/{version}"
    if is_dir(outpath):
        print("outpath already exists", outpath)
    else:
        cpdir(srcpath, outpath)


def get_path(x):
    x = sub(x, "~", "/home/kdog3682")
    if is_dir(x):
        return x
    print(x)
    return 

# files = filter(map(line_getter(read("/home/kdog3682/2023/clip.js")), get_path))
# print(files)

# typst_manager()




def copy_recently_downloaded_files_to_dir():
    dir = "/home/kdog3682/2024-typst/emoji-assets/"
    mkdir(dir)
    files = most_recent_file_groups()
    map(files, lambda file: copy_file(file, npath(dir, rename_file(file))))

# copy_recently_downloaded_files_to_dir()

get_most_recent_file = most_recent_file
# print(copy_file(get_most_recent_file(), "/home/kdog3682/PYTHON/credentials.json"))


# copy_file("/home/kdog3682/2023/test.pdf", "/home/kdog3682/2023/mmgg.morning_walk.pdf")

# 0
# words = list("a _ b c")
# clip("aa")
# pprint(clip())
