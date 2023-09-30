ftplugindir = "/home/kdog3682/.vim/ftplugin/"
gdjsonfile = '/home/kdog3682/2023/git-data3.json'
oldjdjsonfile = "/home/kdog3682/RESOURCES/jd.june.json"
jdjsonfile = '/mnt/chromeos/GoogleDrive/MyDrive/JSONS/jd.june.json'
temptextfile = '/home/kdog3682/RESOURCES/temp.txt'
hskjsondictfile = '/mnt/chromeos/GoogleDrive/MyDrive/JSONS/hsk-dict.json'
mathdir = '/home/kdog3682/MATH/'
bignotefile = '/mnt/chromeos/GoogleDrive/MyDrive/NOTES.TXT'

vimftfile = '/home/kdog3682/RESOURCES/file-table.txt'
drivejsondir = '/mnt/chromeos/GoogleDrive/MyDrive/JSONS/'
import env
import time
import os
import traceback
import sys
from collections import OrderedDict
from base import *

firedir = rootdir + "FIREBASE/"
npmdir = nodedir2023
firedir = rootdir + "FIREBASE/"
playdir = rootdir + "PLAYGROUND/"
resourcedir = rootdir + "Resources2023/"
resdir = rootdir + 'RESOURCES/' 
pipdir = "/usr/lib/python3/dist-packages/pip/"
cm2dir = rootdir + "CM2/"

def download_google_fonts():

    def get_media(x):
        
        if isUrl(x):
            r = requests.get(url, allow_redirects=True)
            if r.status_code != 200:
                raise Exception('not valid download')
            return r.content
        e = getExtension(x)
        if e:
            if isfile(x):
                return read(x)

    def write_media(outpath, data):
        with open(outpath, 'wb') as f:
            f.write(data)
            print('successfully wrote to dldir:', outpath)
    
    fontdir2023 = dir2023 + 'fonts/'
    fontfile = 'font.zip'

    for font in fonts:
        font_name = font.replace(' ', '+')
        url = f'https://fonts.google.com/download?family={font_name}'
    
        dirname = dash_case(font)
        outdir = fontdir2023 + dirname
        dprompt(dirname, outdir)
        data = get_media(url)
        write_media(fontfile, data)
        unzip(fontfile, mkdir(outdir))

def unzipLatest():
    f = glf()
    readzip(
        f,
        flatten=True,
        outpath=normpath(dldir, removeExtension(tail(f))),
    )

    return flatdir(mostRecent(dldir))


def to_array(x):
    if isArray(x):
        return x
    return [x]


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
    appendjson("clip.json", [s])


class FileState:
    def debug(self):

        def zip(self):
            return self.getZipFiles()
            
        def js(self):
            return 

        data = locals()
        fn = data.get(self.extension)
        if fn:
            pprint(fn(self))
            print(self.file)

    
    def getZipFiles(self):
        from zipscript import getZipFiles
        return getZipFiles(self.file, self.head)
    
    def __repr__(self):
        return self.file
    
    def __init__(self, file):
        self.file = file
        head, tail = headAndTail(file)
        self.head = head
        self.tail = tail
        self.name = removeExtension(self.tail)
        self.extension = getExtension(file)
        self.is_zip = self.extension == "zip"
        self.is_js = self.extension == "js"
        self.is_py = self.extension == "py"
        self.is_html = self.extension == "html"

    def remove(self):
        rfile(self.file)
    
    def unzip(self, dest=0, **kwargs):
        if not self.is_zip:
            return 

        from zipscript import unzip
        target = kwargs.get('target', None)
        saveIt = kwargs.get('save', None)

        if target:
            targetFile = findFile2(self.getZipFiles(), target)
            assert targetFile
            files = unzip(self.file, dest or self.head)
            pprint(files)
            targetFile = findFile2(files, target)
            return targetFile

        if saveIt:
            save(files)

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
        if q and test("^" + q, getattr(state, key)):
            return True

    keys = ["name", "extension", "tail", "file"]
    for item in smartItems:
        for key in keys:
            if runner(item, key):
                return item["fn"](state)


def appendVim(value, name="temp"):
    value = dumpJson(value)
    s = f"let g:{name} = {value}"
    append("/home/kdog3682/.vimrc", s)



def antichoose(items):
    assert items

    a = prompt2(items)
    if not a:
        return items
    indexes = [int(n) - 1 for n in a.strip().split(" ")]

    store = []
    for i, item in enumerate(items):
        if i not in indexes:
            store.append(item)
    return store


def pyargs(file="base.py"):
    name = getExtension(file) + "args"
    items = antichoose(
        fa(file, "\(([a-z]\w*)\)", filter="<9")
    )
    appendVim(items, name=name)


def toString(s):
    import inspect
    if isFunction(s):
        return inspect.getsource(s)
    return str(s)


def fa(s, r, flags=0, **kwargs):

    s = textgetter(s)
    m = re.findall(r, s, flags=flags)
    if kwargs.get("filter"):
        m = filter(m, kwargs.get("filter"))
    m = unique(m)

    if kwargs.get("choose"):
        m = antichoose(m)

    if kwargs.get("fn"):
        m = map(m, kwargs.get("fn"))

    if kwargs.get("map"):
        m = map(m, kwargs.get("map"))

    if kwargs.get("filter"):
        m = filter(m, kwargs.get("filter"))

    if kwargs.get("append"):
        if kwargs.get("append") == "self":
            appendVariable(dumpJson(m))

    if kwargs.get("clip"):
        clip(m)

    if kwargs.get("save"):
        prompt(m)
        append(currentFile(), join(m))
    pprint(m)
    return m


def map(items, x):
    f = x
    if isString(x):
        x = x.strip()
        f = lambda arg: templater(x, [arg])

    return [f(el) for el in items]


def filter2(items, x=exists):
    f = x
    if isString(x):
        if test("^[<>=]", x):
            f = eval(f"lambda x: len(x) {x}")
        else:
            f = eval(f"lambda x: {x}")

    return [el for el in items if f(el)]


s = """
zip
javascript
python
html
css
"""
t = """
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
        print("returning cache")
        return m


def dictf(ref):
    def f(k):
        fn = getattr(ref, k, getattr(ref, "default", None))
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
            print("error")
            dprint(k, v)
            input("throw please")
            input("throw please")
            input("throw please")
            print("---------------")

    return runner

def hasValue(x = None):
    if x == None or x == False:
        return False
    return True

def fparse(fn, *args):
    if not fn:
        return args[0]
    elif isFunction(fn):
        value = fn(*args)
        if hasValue(value):
            return value
        return args[0]
    else:
        return fn[0]
        

def dictf(ref, fallback = None):
    def runner(item):
        return ref.get(item, fparse(fallback, item)) or item
    return runner
            
def lines(s, ref=0):
    s = s.strip()
    lines = map(s.split("\n"), trim)
    if test("^ *\w+:", s, flags=re.M):
        lines = map(lines, lambda x: splitonce(x, " *: *"))

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


"pillars.py"




def hashbang(filename):
    assert isfile(filename)
    # Add a hashbang line to the file if it doesn't already have one
    with open(filename, "r") as f:
        first_line = f.readline().strip()

    if not first_line.startswith("#!"):
        print("adding hasbang line")
        with open(filename, "r+") as f:
            content = f.read()
            f.seek(0, 0)
            f.write("#!/usr/bin/env python3\n" + content)

    # Set the execute permission for the file
    os.chmod(filename, 0o755)


def git_push_dir(dir):

    names = gitNames(dir)
    mainCommand = f"""
        cd {dir}
        git add .
        git commit -m "'message'"
        git push
    """

    response = SystemCommand(mainCommand, dir=dir)
    gitData = {
        "success": response.success,
        "error": response.error,
    }

    pprint(gitData)
    pprint(names)


def dprompt(*variables, **kwargs):

    strings = []
    caller = getCaller()
    store = OrderedDict()
    store["caller"] = caller

    for v in variables:
        try:
            vars = (
                inspect.currentframe().f_back.f_locals.items()
            )
            name = [
                v_name
                for v_name, v_val in vars
                if v_val is v
            ][0]
            store[name] = v
        except Exception as e:
            strings.append(v)

    for a, b in kwargs.items():
        store[a] = b

    if strings:
        store["strings"] = strings

    pprint(store)
    return input("")


def gitNames(dir):
    s = SystemCommand("git status --short", dir=dir).success
    pairs = unique(re.findall("(\S+) (\w+(?:\.\w+)+)", s))
    store = [[], []]
    for a, b in pairs:
        if a == "M":
            store[0].append(b)
        else:
            store[1].append(b)
    a, b = store
    return {
        "modified": a,
        "created": b,
    }


def mwrite(inpath, outpath, regex, flags=0):
    inpath = smart_path(inpath)
    outpath = smart_path(outpath, inpath)
    text = read(inpath)
    assert text

    a, payload = mget(regex, text, flags=flags, mode=list)
    assert payload

    append(outpath, payload)
    cfile(inpath, "temp.py")
    write(inpath, a)


def smart_path(file, refpath=0):
    if refpath:
        dir = dirFromFile(refpath)
        file = addExtension(file, getExtension(refpath))
        alert(dir, file)
    else:
        dir = dirFromFile(file)
    return npath(dir, file)


def tesseractExtractText(imageFile):
    from PIL import Image
    import pytesseract

    return pytesseract.image_to_string(
        Image.open(imageFile)
    )


def foo1682173868():
    """
    google -> clip -> delete based on comments = delete
    googleclip
    """

    files = clip()
    chdir(pydir)
    for file in files:
        if file.get("comments").startswith("dele"):
            rfile(file.get("name"))


def get_media(x):

    if isUrl(x):
        r = requests.get(url, allow_redirects=True)
        if r.status_code != 200:
            raise Exception("not valid download")
        return r.content
    e = getExtension(x)
    if e:
        if isfile(x):
            return read(x)


def write_media(outpath, data):
    with open(outpath, "wb") as f:
        f.write(data)
        print("successfully wrote to dldir:", outpath)


def download_google_fonts():

    fontdir2023 = dir2023 + "fonts/"
    fontfile = "font.zip"

    for font in fonts:
        font_name = font.replace(" ", "+")
        url = f"https://fonts.google.com/download?family={font_name}"

        dirname = dash_case(font)
        outdir = fontdir2023 + dirname
        dprompt(dirname, outdir)
        data = get_media(url)
        write_media(fontfile, data)
        unzip(fontfile, mkdir(outdir))


def dash_case(s):
    items = re.split("\W|(?=[A-Z]+[a-z])", s)
    return join(filter(items), delimiter="-").lower()


def unzipLatest():
    f = glf()
    readzip(
        f,
        flatten=True,
        outpath=normpath(dldir, removeExtension(tail(f))),
    )

    return flatdir(mostRecent(dldir))


def foo1682177487(r, type=str):
    """
    collectGlobalVariables
    """

    store = {}
    dir_vars = [var for var in globals() if test(r, var)]
    for var in dir_vars:
        value = globals().get(var)
        if isinstance(value, type):
            store[var] = value

    if store:
        appendVariable(dumpJson(store))


def strftime(strife=0):
    strife = "%A %B %d %Y, %-I:%M:%S%p"
    return datetime.now().strftime(strife)


def coerceToObject(x):
    return x if isObject(x) else {"value": x}


def ensure_object(func):
    def decorator(self, obj, *args, **kwargs):
        return func(
            self, coerceToObject(obj), *args, **kwargs
        )

    return decorator


def empty(x, key=0):
    if not key:
        return x == None or len(x) == 0
    try:
        return not hasattr(x, key)
    except Exception as e:
        return x == None or len(x) == 0


def info(var):
    var_info = {}
    var_info["class_instance"] = type(var)
    var_info["type"] = type(var).__name__
    var_info["type_str"] = str(type(var))
    var_info["name"] = var.__class__.__name__
    var_info["constructor"] = var.__init__.__func__
    return var_info


def t2s(x):
    return type(x).__name__
    return x.__class__.__name__


def isObjectArray(x):
    return isArray(x) and isObject(x[0])


dateRE = "^#? *(?:\d{6,}|\d\d\D\d\d\D\d\d\d\d)"


def makeRE(s):
    r = s.strip()
    r += "([\w\W]+?)"
    r += "^#? *(?:\d{6,}|\d\d\D\d\d\D\d\d\d\d)"
    return r


def fn(file):
    fileName = filePrompt(
        dir=resourcedir, e="txt", fallback="temp", ref=file
    )
    s = "^04-13-2023 Code for Kids"
    r = makeRE(s)
    s = search(makeRE(s), read(file), flags=re.M).strip()
    write(fileName, s)


def filePrompt(dir="", e="", fallback="temp", ref=0):
    if not dir and ref:
        dir = head(ref)

    if not e and ref:
        e = getExtension(ref)
    name = (
        prompt(dir=dir, message="name for file?")
        or fallback
    )
    name = addExtension(name, e)
    name = os.path.join(dir, name)
    logfile(name)
    return name


def logfile(x):
    if isArray(x):
        s = join(map(x, lambda x: datestamp() + " " + x))
        append("files.txt", s)
        print("append to log file", s)
    else:
        print("logging file", x, "to", "files.txt")
        append("files.txt", datestamp() + " " + x)


r = "https:.*?\.(?:css|js)"
f = lambda x: x.strip() and not test("\\\\u", x)


cmdir = "/home/kdog3682/CM/"


def copy_dir_to_dir(f):
    cfile(cmdir + f, dir2023)


def map(items, fn, *args, filter=1, **kwargs):
    _promptOnce = kwargs.pop('promptOnce', None)
    if not items:
        return []

    if isString(fn):
        _key = fn

        arg = toArray(items)[0]
        if isClassObject(arg):
            prompt('aa')
            fn = lambda x: getattr(x, _key)
        elif isObject(arg):
            fn = lambda x: x.get(_key)
        elif "$" in _key:
            fn = lambda x: templater(_key.strip(), [x])
        else:
            fn = lambda x: search(_key, x)

    if isNestedArray(items):
        return [fn(a, b) for a, b in items]

    if isObject(items):
        store = {}
        for k, v in items.items():
            value = fn(k, v)
            if value:
                store[k] = value
            elif filter:
                continue
            else:
                store[k] = v
        return store

    store = []
    for i, item in enumerate(toArray(items)):
        try:
            value = fn(item, *args, **kwargs)
            if not (filter and not value):
                if i == 0 and _promptOnce:
                    promptOnce(value, _promptOnce)
                store.append(value)
        except Exception as e:
            prompt(item, error="ERROR AT MAP", message=e)
            continue
    return store



def isClassObject(x):
    return type(x) not in env.builtins

def first(x):
    return x.values()[0] if isObject(x) else x[0]


def node_dir_search(*args, root="@codemirror"):
    path = os.path.join(npmdir, root, *args)
    files = os.listdir(path)
    if "dist" in files:
        files = os.listdir(os.path.join(path, "dist"))
    if "index.js" in files:
        path = os.path.join(path, "dist", "index.js")
        return ofile(path)
        cfile(path, os.path.join(dir2023, "commands.js"))


def getdir(*args):
    ff(os.path.join(*args), isdir=1)


def github_content_url(user, repo, file, master="master"):
    base = "https://raw.githubusercontent.com"
    return f"{base}/{user}/{repo}/{master}/{file}"


def textgetter(x):
    if isArray(x):
        return x
    if x == "self":
        return read(currentFile())
    if len(x) > 100:
        return x
    if isGithubUrl(x):
        user, repo, file = x.split("/")[-3:]
        dprompt(user, repo, file)
        url = github_content_url(user, repo, file, "master")
        s = request(url)
        if s == None:
            url = github_content_url(
                user, repo, file, "main"
            )
            s = request(url)
            if s == None:
                raise Exception(
                    "tried master & main -> both none"
                )
        return s
    if isUrl(x):
        return request(x)
    if isfile(normDirPath(x)):
        return normRead(x)
    return x


def request(url):
    r = requests.get(
        fixUrl(url), {"user-agent": env.BROWSER_AGENT}
    )
    if r.status_code == 200:
        return parseJSON(r.text)
    else:
        return None


def removeComments(s):
    r = "^ *(?:<!--|#|//).+\n*"
    return re.sub(r, "", s, flags=re.M)


def npm(s, dir=cm2dir):
    dir = dir2023
    items = (
        split(removeComments(s), "\s+")
        if isString(s)
        else s
    )
    cmd = join(items, delimiter=" ")
    cmd = "npm i " + cmd
    prompt(npmcmd=cmd, dir=dir)
    SystemCommand(cmd, dir=dir)
    printdir(npmdir)


str1682629691 = """
    #@replit/codemirror-vim
    #@codemirror/lang-markdown
    #@codemirror/lang-javascript
    #@codemirror/basic-setup

    #@lezer/common
    #@lezer/lr
    #@lezer/highlight
    #@lezer/generator
    js-yaml
"""

s = """

/mnt/chromeos/MyFiles/Downloads/vite-repro/tokens.js
/mnt/chromeos/MyFiles/Downloads/vite-repro/yaml.js
/mnt/chromeos/MyFiles/Downloads/vite-repro/yaml.terms.js
/mnt/chromeos/MyFiles/Downloads/vite-repro/highlight.js
"""


r = """(\w+)['"]? *[:=]['"]? *(/[^/].+/)"""


s = """

"""


def isGithubUrl(x):
    return "https://github" in x


def ffstring(s):
    ref = {
        "j": "json",
        "c": ["mode", "partition"],
        "res": ["mode", "transfer-to-resources"],
    }

    def f(k):
        val = ref.get(k, k)
        if isArray(val):
            return val
        return val

    kwargs = reduce(split(s, " "), f)
    kwargs["partition"] = True

    ff(dir2023, **kwargs)


s = """

    "@codemirror/autocomplete": "^6.6.0",
    "@codemirror/lang-css": "^6.2.0",
    "@codemirror/lang-html": "^6.4.3",
    "@codemirror/lang-javascript": "^6.1.7",
    "@codemirror/lang-json": "^6.0.1",
    "@codemirror/lang-markdown": "^6.1.1",
    "@codemirror/lang-python": "^6.1.2",
    "@codemirror/language": "^6.6.0",
    "@codemirror/matchbrackets": "^0.19.4",
    "@codemirror/search": "^6.4.0",
    "@codemirror/state": "^6.2.0",
    "@codemirror/theme-one-dark": "^6.1.2",
    "@codemirror/view": "^6.10.1"
"""

    #@replit/codemirror-vim
def review(files=0, move=0, mode=0, **kwargs):
    if not files:
        files = absdir(dir2023)
    if not kwargs:
        kwargs = {
            'js': 1,
            'days': 10,
        }
    files = ff(files, **kwargs)
    if not files:
        print('no files ... early return')
        return 

    removed = []
    moved = []
    saved = []
    os.system("clear")

    for file in files:
        if alwaysDelete(file):
            removed.append(files)
            continue

        a = prompt(fileInfo(file))
        if a == "d":
            removed.append(files)
        elif a:
            saved.append(files)
            
    dprompt(removed, saved)
    clip(saved)
    map(removed, rfile)

def old(s):
    ofile(budir + s)

str1683347537 = """
    
{
  "name": "vite1",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "devDependencies": {
    "vite": "^4.3.2"
  }
}
"""
def getObservableInitialDataFromLink(url):
    s = request(url)
    r = '<script id="__NEXT_DATA__" type="application/json">([\w\W]+?)</script>'
    m = search(r, s)
    data = parseJSON(m)
    return data
    #s = srequest('https://observablehq.com/@d3/zoomable-circle-packing')

def parseObservableData(data):
    
    data = data.get('props').get('pageProps').get('initialNotebook')
    files = data.get('files')
    nodes = data.get('nodes')
    values = []
    nodes = filter(nodes, lambda x: not test('^md', x.get('value')))
    def sorter(x):
        value = x.get('value')
        return len(value)
        score = 0
        pinned = x.get('pinned')
        id = x.get('id')
        if pinned:
            score += 100

        score += int(id)
        return score
    
    nodes.sort(key=sorter)
    def mapper(node):
        value = node.get('value')
        #if test('a', b):
        return value
    nodes = map(nodes, mapper)
    prompt(nodes)
    prompt(files)

    #files = map(files, 'url')
    #pprint(nodes)
    #pprint(files)


def fo1(a, b):

    ref = {
        '1': 'standard',
        'del': 'delete',
        'd': 'delete',
        'clear': 'clear',
    }
    m = search('^(?:1|del|d|clear)$', b)
    if m:
        return ['mode', ref[m]]

    m = search('rn (\S+)', b)
    if m:
        if '$' in m:
            m = m.replace('$', a)
        return ['rename', m]

    return ['comment', m]

def mergejson(file, data):
    if not data: 
        return 
    prev = read(file) or {}
    for k,v in data.items():
        if k in prev:
            if isArray(v):
                prev[k].extend(v)
            else:
                prev[k].update(v)
        else:
            prev[k] = v
    write(file, prev)

def file_table_action():

    def fo2(a, b):
        c, d = fo1(a, b)
        return {'file': a, c: d}

    data=clip()
    r = '^\S+ *(\S+)(?: +(.+))?'
    #data = fa('file-table.txt', r, flags=re.M, fn=fo2)
    prompt(data=data)
    standard = []
    current = []
    for item in data:
        mode = item.get('mode')
        file = item.get('file')
        if mode == 'delete':
            rfile(file)

        elif mode == 'standard':
            standard.append(file)

        elif item.get('rename'):
            mfile(file, item.get('rename'))
        else:
            current.append(file)

    current.sort()
    standard.sort()
    payload = {
        'standard': standard,
        'items': [
            {'date': datestamp(), 'current': current}
        ]
    }
    mergejson('files.json', payload)

prosemirrorNpm = [
    "prosemirror-model",
    "prosemirror-keymap",
    "prosemirror-view",
    "prosemirror-transform",
    "prosemirror-state",
    "prosemirror-example-setup",
    "prosemirror-markdown",
    "prosemirror-inputrules",
    "prosemirror-history",
    "prosemirror-collab",
    "prosemirror-commands",
    "prosemirror-schema-basic",
    "prosemirror-schema-list",
    "prosemirror-schema-table",
    "prosemirror-tables",
]
def prosemirrorFileTable():
    
    def g(dir):
        files = ff(dir, recursive=1, js=1)
        if tail(files[0]) == 'index.es.js':
            return [files[0]]
        return files

    dirs = ff(npmdir, name='^prose')
    dirs = map(dirs, g)
    files = flat(dirs)
    write('pm-file-table.txt', join(files))

def github_usercontent_url(user, repo, *args, master='master'):
    base = 'https://raw.githubusercontent.com'
    file = '/'.join(args)
    return f"{base}/{user}/{repo}/{master}/{file}"

def manim():
    arg = choose(env.manimToc)
    ofile(github_usercontent_url('3b1b', 'manim', arg[0]))



def longstamp():
    strife = "%A %B %d %Y, %-I:%M:%S%p"
    return datestamp(strife=strife)

def mdir(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for item in os.listdir(source_dir):
        source = os.path.join(source_dir, item)
        destination = os.path.join(dest_dir, item)
        print('moving', item)

        if os.path.isfile(destination):
            a = input(f"Do you want to overwrite {destination}? (y/n): ")
            if a.lower() == 'n':
                continue

        shutil.move(source, destination)

    shutil.rmtree(source_dir)
    print('done')

markdowndir = '/home/kdog3682/MARKDOWN/'

class Save:
    def __init__(self, file, fallback = {}):
        self.file = file
        self.data = read(self.file) or fallback

    def __enter__(self):
        return self.data

    def __exit__(self, etype, value, traceback):
        if etype:
            return 
        print(self.data)
        #write(self.file, self.data)

def generate_markdown_toc():
    file = 'markdown-toc.json'
    def runner(file):
        print('file', file)

    with Save(file, []) as prev:
        prevFiles = map(prev, 'name')
        g = lambda x: tail(x) not in prevFiles
        files = filter(absdir(markdowndir), g)
        data = map(files, runner)
        prev.extend(data)
        prompt(prev=prev)

def moveChangeLogFile():
    changelogfile = '/home/kdog3682/2023/changelog.md'
    url = f"{markdowndir}me.{datestamp()}.md"
    mfile(changelogfile, url)


def push(store, x):
    if x != None:
        store.append(x)


def ignoreFile(name):
    r = '^(?:\W)|license|readme|rc|ignore'
    return test(r, name, flags=re.I)


def createLogger():

    import logging

    logging.basicConfig(filename='logging.txt', level=logging.INFO,
        format='%(message)s')

    logger = logging.getLogger()

    def log(*args):
        s = ' '.join(map(list(args), str))
        return logger.info(s)
    return log

def renameClipToDriveFile():
    newName = prompt('name for drive clip file?')
    cfile(clipfile, drivedir + newName)

def ask_reddit(s):
    import redditscript
    r = redditscript.Reddit()
    try:
        print(r.askString(s))
    except Exception as e:
        print(str(e))
    
def toArray(x):
    if not x:
        return []
    if isArray(x):
        return x
    if isString(x):
        return split(x, "\n")
    return [x]


def removeSmallFiles(files):
    for file in files:
        if isfile(file) and fsize(file) < 50:
            rfile(file)

def parseDiff(dir):

    result = SystemCommand('git status --short', dir=dir)
    r = '^ *(\?\?|M) (.+)'
    m = re.findall(r, result.success, flags=re.M)
    if not m:
        return 

    modified = []
    created = []
    for a,b in m:
        if removable(b):
            continue

        if a == '??':
            created.append(b)
        else:
            modified.append(b)

    date = datestamp()
    payload = {'date': datestamp()}
    if modified: payload['modified'] = modified
    if created: payload['created'] = created
    payload['directory'] = dir

    pprint(payload)
    appendjson('/home/kdog3682/2023/git-data3.json', payload, mode=list)

def gitPush(dir):

    mainCommand = f"""
        cd {dir}
        git add .
        git commit -m "'autopush'"
        git push
    """

    # git push -f origin master
    # use this when there is an error about different work

    if dir != resdir:
        parseDiff(dir=dir)
    SystemCommand(mainCommand, dir=dir, printIt=1)

def removable(f):
    if isfile(f) and fsize(f) < 50:
        rfile(f)
        return True

def FixGitCache():
    SystemCommand('''
        #git rm --cached -r
        #git add .
        #git commit -m "Fixed .gitignore not ignoring files"
        #git push
    ''')
    print('Git Cache has been fixed. The next push will see these changes in action.')






def moveRecentlyDownloadedFileToDrive(name):

    def drivepath(file, ext):
        return f"{drivedir}{name}.{timestamp()}.{getExtension(ext)}"

    file = glf(dldir)
    outpath = drivepath(name, ext=file)
    dprompt(outpath)
    mfile(file, outpath)

def cleanupDldir():
    chdir(dldir)
    files = os.listdir()
    
    print(files)
    #cleanupDldir()

    #Do it via javascript and server ... yes.

def foo():
    print('hi')


class Silence:
    def __init__(self, silencer = True):
        self.stdout = sys.stdout
        self.silencer = silencer

    def __enter__(self):

        class NullWriter:
            def write(self, s):
                pass

            def flush(self):
                pass
        
        if self.silencer:
            sys.stdout = NullWriter()

    def __exit__(self, etype, value, traceback):
        sys.stdout = self.stdout


def sysArg():
    try:
        return toArgument(sys.argv[1])
    except Exception as e:
        return 
    

def sysArgs():
    base = sys.argv[1:]
    length = len(base)
    if length == 0:
        return ['', []]
    if length == 1:
        return [base[0], []]
    return [base[0], base[1:]]

def runModule(module=0):
    
    data = None
    with Silence(True):
        arg, args = sysArgs()

        if not arg:
            return

        fn = None
        if module:
            if hasattr(module, arg):
                fn = getattr(module, arg)
        else:
            fn = globals().get(arg, None)

        if fn:
            try:
                data = {'success': fn(*args)}
            except Exception as e:
                error = {
                    "type": type(e).__name__,
                    "message": str(e),
                    "stack": traceback.format_exc()
                }
                data = {'error':  error}

    return json.dumps(data)


def backupFolder(dir):
    dir = dirgetter(dir)
    for file in absdir(dir):
        cfile(file, budir)

def seeBackup(file):
    file = f"{budir}{file}.backup"
    print(read(file))

def driveWrite(file, s):
     write(drivedir + addExtension(file, 'py'), s)

class DropBox:
    def __init__(self):
        from dropbox.files import WriteMode
        from dropbox import Dropbox
        self.dropbox = Dropbox(env.dropboxtoken)
        self.mode=WriteMode('overwrite')

    def push(self, file):
        path = '/' + tail(file)
        with open(npath(file), 'rb') as f:
            r = self.dropbox.files_upload(f.read(), path, mode=self.mode)
            return r

    def pull(self, file):
        path = '/' + tail(file)
        meta, response = self.dropbox.files_download(path)
        return response.content.decode('utf-8')


def npath(dir=0, file=0):
    if isArray(file):
        return map2(file, lambda x: npath(dir, x))
    if not dir:
        return file
    elif not file:
        return npath(dirFromFile(file), file)
    if isfile(dir):
        if not getExtension(file):
            file = addExtension(file, getExtension(dir))
        dir = head(dir)
    return os.path.join(dirGetter(dir), tail(file))

def gitCloneAndMove(repoUrl, move=1):
    repoUrl = search('.*?github.com/[\w-]+/[\w-]+', repoUrl)
    name = repoUrl.split('/')[-1]
    #dprompt(repoUrl, name)
    SystemCommand(f'''
        cd {dldir}
        git clone {repoUrl}
    ''')


    dir = npath(dldir, name)
    save(dir)

    if not move:
        return 
    if not isdir(dir):
        return 

    src = os.path.join(dir, 'src')
    if not isdir(src):
        src = dir
    files = getFiles(src)
    newdir = f'Git Repo - {name}'
    newdir = npath(dldir, newdir)
    shutil.move(src, newdir)
    rmdir(dir, force=1)

def createKwargs(s, ref, aliases):
    if not s:
        return {}

    r = "(\S+?) *= *(\S+?)(?= |$)"
    s, items = mreplace(r, s)
    s = dreplace(s, ref, template="(?<![\w=])(?:$1)\\b")
    s, moreItems = mreplace(r, s)

    aliaser = aliaserf(aliases)

    A = {aliaser(k) : toArgument(v) for k, v in items}
    B = {aliaser(k): True for k in split(s, " ")}
    C = {aliaser(k) : toArgument(v) for k, v in moreItems}
    return mergeToObject(A, B, C)

def mergeToObject(*args):
    store = {}
    for arg in args:
        if isArray(arg):
            prompt(arg)
            store[arg[0]] = arg[1]
        elif isObject(arg):
            store.update(arg)
        else:
            warn('arg can only be array or object', arg)
    return store



def toArgument(x):
    if isNumber(x):
        return int(x)
    if test('^(?:""|\'\')$', x.strip()):
        return ''
    return x

def aliaserf(dict):
    def runner(k):
        return dict.get(k, k)
    return runner

def getFilesWrapper(s):

    aliases = {
        'small': 'smallerThan',
        'big': 'biggerThan',
    }

    ref = {
        "backup": "dir=pub after=8pm js=1 copy=bu",
        "i": "ignore",
        "budir": "dir=bu",
        "old": "old=1",
        "budir": "dir=bu",
        "pdfjson": "json=1",
        "root": "dir=root",
        "pdf": "pdf=1",
        "5pm": "after=5pm",
        "6pm": "after=6pm",
        "7pm": "after=7pm",
        "8pm": "after=8pm",
        "9pm": "after=9pm",
        "10pm": "after=10pm",
        "11pm": "after=11pm",
        "midnight": "after=12am",
        "noon": "after=12pm",
        "1pm": "after=1pm",
        "2pm": "after=2pm",
        "3pm": "after=3pm",
        "4pm": "after=4pm",
        "pub": "dir=pub",
        "cwf": "dir=cwf",
        "dl": "dir=dl",
        "c": "copy",
        "cp": "copy",
        "debug": "mode=debug",
        "open": "mode=open",
        "o": "mode=open",
        "d": "mode=debug",
        "n": "name",
        "r": "mode=review",
        "today": "date=today",
        "t": "text",
        "ye": "date=yesterday",
        "sm": "small=2000",
        "small": "small=2000",
        "this": "date=today",
        "tf": "testfunction",
        "mv": "move",
        "of": "onlyFiles=1",
        "h": "html",
        "i": "mode=info",
        "s": "mode=save",
        "big": "big=100000",
    }

    kwargs = createKwargs(s, ref, aliases)
    files = getFiles(dir2023, **kwargs)
    return pprint(files)
    return write('clip.js', files)

def getFiles(dir=dir2023, **kwargs):
    if isArray(dir):
        return dir
    recursive = kwargs.pop('recursive', False)
    sortIt = kwargs.get('sort', False)
    promptIt = kwargs.get('prompt', False)
    parser = kwargs.get('parser', False)
    folders = kwargs.get('folders')
    n = kwargs.get('n')
    dir = dirGetter(dir)

    if n:
        files = sortByDate(absdir(dir))
        return getN(files, n)

    def runner(dir):
        for file in absdir(dir):
            try:
                if folders and isdir(file):
                    if checkpoint(file):
                        store.append(file)
                elif isfile(file) and checkpoint(file):
                    store.append(file)
                elif recursive and isdir(file):
                    runner(file)
            except Exception as error:
                errorPrompt(file, error)
            

    store = []
    checkpoint = checkpointf(**kwargs)
    runner(dir)
    if sortIt:
        store = sortByDate(store, reverse=kwargs.get('reverse', 0))
    if promptIt:
        prompt(store)
    if parser:
        return map2(store, parser)
    return store

def isIgnoredFile2(file):
    name = tail(file)
    ignore = [
        "vosk-api",
        "__pycache__",
        "node_modules",
        ".git",
        ".gitignore",
    ]
    ignoreRE = "^(?:\W)"

    if name in ignore:
        return True
    if test(ignoreRE, name):
        return True

def c2(s):
    write('clip.js', s)

class NYTimes:
    def __init__(self):
        pass

    def articlesearch(self, topic, **kwargs):
        base = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?'
        page = kwargs.get('page', 0)
        curl = f'{base}q={topic}&api-key={env.nytimesApiKey}&page={page}'
        data = request(curl)
        docs = data.get('response').get('docs')
        map(docs, ['abstract', 'web_url as url', 'pub_date as date', 'byline.original', 'word_count'])


def incrementalName(s=0, dir = 'drive'):
    if not s:
        s = prompt('choose a name because s is None')
    override = 0
    if s.endswith('!'):
        s = s[:-1]
        override = 1
    front = removeExtension(s)
    e = getExtension(s)
    d = dirGetter(dir)
    count = 1
    while count < 50:
        name = os.path.join(d, f'{front} {count}.{e}')
        if override:
            return name
        if not isfile(name): return name
        count += 1

def dirGetter(dir=None):
    if not dir:
        return os.getcwd()
    dir = dir.replace('~', '/home/kdog3682')
    value = env.dirdict.get(dir, dir)
    assert isdir(value)
    return value


def foo1689558041(f):
    mfile(f, incrementalName(f))

s='''NotoColorEmoji.ttf Sohne-Halbfett.otf'''
def moveToActiveDir(s):
    files = map(xsplit(s), lambda x: npath(dirGetter('dl'), x))
    for file in files:
        mfile(file, dir2023)

def rpw(file, f, check=0):
    payload = f(read(file))
    if check:
        prompt(payload)
    write(file, payload)

def relpath(s):
    prefix = ''
    return s.replace('/home/kdog3682/2023/', prefix)

def getStringArg(key, s):
    r = f"{key}\([\'\"]?(.*?)[\'\"]\)"
    return search(r, s, flags=re.M)

def getStringAttr(key, s):
    r = f"^ *[\'\"]?{key}[\'\"]? *: *[\'\"]?(.*?)[\'\"]?[,;]? *$"
    return search(r, s, flags=re.M)

def foo1689563342(s):

    chunks = re.split('\n+(?=[^\s\]\}])', s)
    d = {}
    for c in chunks:
        if test('^@font-face', c):
            name = getStringAttr('font-family', c)
            src = getStringArg('url', c)
            d[src] = name 

    def parser(x):
        f = x.group(0)
        if test('^\.?/?fonts/', f):
            return f

        name = addExtension(d[f], getExtension(f))
        outpath = npath('fonts', name)
        assert isfile(f)
        cssPath = relpath(outpath)
        mfile(f, outpath)
        return cssPath

    s = re.sub('[\w_/-]+\.(?:woff2?|ttf|otf)', parser, s)
    return s



def headAndTail(s):
    a, b = os.path.split(s)
    if a == '':
        a = '/home/kdog3682/2023'
    return a, b

def unzipfilestodir(outdir):
    files = getFiles('dl', zip=1, hours=1, recursive=0)
    prompt(files)
    for file in files:
        f = FileState(file)
        f.unzip(outdir)
        f.remove()

def extractAZipFile(file):
    f = FileState(glf())
    f.unzip(trashdir)
    g = trashdir + file
    mfile(g, dir2023)
    return file

def fo():
    def f(a):
        message = a.get('message')
        if not message:
            return 

        role = message.get('author').get('role')
        if role == 'assistant':
            parts = message.get('content').get('parts')
            s = join(parts)
            r = '```(\w+)\s+([\w\W]+?)```'
            m = re.findall(r, s)
            store.extend(m)

    store = []
    data = list(clip().get('mapping').values())
    map(data, f)
    #pprint(store)

    chromeExtensionName = 'myFirstExtension'
    dir = mkdir(dldir + chromeExtensionName)
    chdir(dir)
    for extension, contents in store:
        if extension == 'js':
            write('background.js', contents)

        if extension == 'json':
            write('manifest.json', parseJSON(contents))
        #'/mnt/chromeos/MyFiles/Downloads/myFirstExtension/manifest.json'
        #'/mnt/chromeos/MyFiles/Downloads/myFirstExtension/background.js'

def linKeSong():
    def getUrl(n):
        return "jjwxc.net/onebook.php?novelid=2337210&chapterid={n}"

    def parser(n):
        url = fixUrl(getUrl(n))
        s = request(url)
        c2(s)

    parser(1)

def oc():
    ofile('clip.js')

class LinKeSong:
    def __init__(self):
        pass

    def run(self):
        f = lambda x: int(findall('\d+(?!\))', x)[-1])
        items = sort(mostRecent(dldir, 9), f)
        store = []

        for i,item in enumerate(items):
            if i == 0:
                store.append(self.foo1689880202(item))
            else:
                store.append(self.foo2(item))

        clip(store)

    def openLinKeSong(self):
        items = list(range(1, 10, 1))
        urls = map(items, lambda x: fixUrl(f"jjwxc.net/onebook.php?novelid=2337210&chapterid={x}"))
        for url in urls:
            time.sleep(1)
            ofile(url)

        
    def parse(self, m):
        def f(x):
            return '\n' * len(findall('br', x.group(0))) 
        
        m = re.sub('[\t ]*(?:<br/?>\s*)+[\t ]*', f, m)
        m = re.sub('。 *', '. ', m)
        m = re.sub('”', '"', m)
        m = re.sub('“', '"', m)
        m = re.sub('“', '"', m)
        m = re.sub(' +"', '"', m)
        m = re.sub('^[\t ]+', '', m, flags=re.M)
        return m
    
    def foo1689880202(self, file):
        s = read(file)
        r = 'class="readsmall".*?>[\w\W]+?</div>\s*([\w\W]+?)<div'
        m = search(r, s)
        return {
            'title': 'aaaaaaaaaaaaaaaaaaaaaa',
            'text': self.parse(m),
        }

    def todohsk():
        hskjsonfile = "/mnt/chromeos/GoogleDrive/MyDrive/JSONS/hsk-master.json"
        data = read(hskjsonfile)
        store = {}
        
        for item in data:
            id = item.get('id')
            hanzi = item.get('hanzi')
            pinyin = item.get('pinyin')
            translations = item.get('translations')[0]

    def remove(self):
        files = getFiles('dl', recursive=0, name='jjwxc')
        rfiles(files)
    def check(self, n=0):
        a = clip()[n]
        if isObject(a):
            a = a.get('text')
        self.a(a)
    def a(self, a):
        write('a.txt', dumpJson(a))
        ofile('a.txt')
    

    def gpt(self):
        input_string = "<h2>舌尖上的吻</h2><br/></div> <div "
        chinese_pattern = r'[\u4e00-\u9fff]+'
        chinese_chars = re.findall(chinese_pattern, input_string)
        print(chinese_chars)  # Output: ['舌尖上的吻']
        return chinese_chars

    def foo2(self, file):
        r = r'<h2>([\u4e00-\u9fff]+.*?)<[\w\W]+?([\u4e00-\u9fff][\w\W]+?)</?div'
        s = search(r, read(file))
        assert(s)
        a, b = s 
        b = self.parse(b)
        return {
            'title': a,
            'text': b
        }

    def pinyin(self):
        from pypinyin import pinyin
        items = clip()
        for item in items:
            s = item.get('text')
            pinyinText = flat(pinyin(s))

            s = item.get('title')
            pinyinTitle = flat(pinyin(s))
            return 

    def jieba(self):

        import jieba
        from pypinyin import pinyin

        out = []
        items = clip()
        seen = set()

        for item in items:
            s = item.get('text')
            words = list(jieba.cut(s))
            titleWords = list(jieba.cut(item.get('title')))
            store = []
            out['body'] = words
            out['title'] = titleWords 
            out['vocabulary'] = store

            for i, item in enumerate(words):
                if not isChinese(item):
                    continue

                if len(item) == 2 and item[0] == '地':
                    item = item[1]

                if item in seen:
                    continue

                p = flat(pinyin(item))
                store.append({'index': i, 'pinyin': p, 'hanzi': item})
                seen.add(item)

        write('linKeSongData.json', out)
        

chineseRE = r'[\u4e00-\u9fff]+'
notChineseRE = r'[^\u4e00-\u9fff]+'
def isChinese(s):
    return test(chineseRE, s)
    

def foo(self):
    return 'export default ' + dumpJson(out)
def copyClipFileToDrive(name):
    name = npath('drive', name)
    cfile('clip.js', name)
    save(name)

def doStoryOfYangxiPalace():

    outpath = npath('jsondrive', 'storyOfYangxiPalace.jieba.json')
    touched = 0

    def parser(file):
        nonlocal touched
        episode = search('S01E(\d+)', file)
        if episode:
            episode = int(episode)
        else:
            return 

        print('doing file', file)
        lines = linegetter(file, fn=jieba.cut)

        if not touched:
            touched = 1

        return {
            'episodeNumber': episode,
            'lines': lines,
        }

    file = "drive-download-20230719T171808Z-001.zip"
    file = FileState(npath('trash', file))
    translations = file.getZipFiles()
    jieba = Jieba()
    payload = map2(translations, parser, sort='episodeNumber')
    try:
        write(outpath, payload)
    except Exception as e:
        clip(payload)
    

def skipPrompt(*args, **kwargs):
    
    import inspect
    message = None
    names = []

    for i, arg in enumerate(args):
        if i == 0 and arg != None:
            return 
        else:

            try:
                vars = inspect.currentframe().f_back.f_locals.items()
                els = [v_name for v_name, v_val in vars if v_val is arg]
                name = els[0]
                names.push(name)
            except Exception as e:
                message = arg
        
    printItems = [ f"{names[0]} does not exist" ]
    if message: printItems.append(message)
    if kwargs: printItems.append(kwargs)
    print(*printItems)
    return input('')

def initializeGlobalVariable(key=0):
    global promptOnceTouched
    try:
        if promptOnceTouched:
            print('already touched early return')
            return 
        promptOnceTouched = True
        return True
    except Exception as e:
        if (type(e) == NameError):
            promptOnceTouched = True
            return True
        else:
            raise e
        

def promptOnce(x, mode=0):
    if initializeGlobalVariable('promptOnceTouched'):
        prompt(x, mode)



class Jieba:
    def __init__(self, convert=0):
        import jieba
        from pypinyin import pinyin

        self.jieba = jieba
        self.ref = read(hskjsondictfile)
        self.pinyin = lambda x: ''.join(flat(pinyin(x)))
        self.watcher = Watcher()
        self.count = 0

        if convert:
            from opencc import OpenCC
            cc = OpenCC(convert)
            self.simpliefied = lambda x: cc.convert(x)


    def cut(self, s, timestamp=0):
        self.count += 1

        store = []
        tokens = self.jieba.cut(s.strip())

        for i, item in enumerate(tokens):
            data = {
                'index': i,
                'hanzi': item,
            }

            if not isChinese(item):
                type = 'punctuation'
                data['type'] = type
                store.append(data)
                continue

            data['pinyin'] = self.pinyin(item)

            if len(item) == 2 and item[0] == '地':
                type = 'adjectiveConversion'
                key = item[1]
                if key not in self.watcher:
                    data['new'] = True
                store.append(data)
                continue

            data['new'] = item not in self.watcher
            data['type'] = 'hanzi'
            store.append(data)

        chinesePinyin = ''
        for item in store:
            if item.get('type') == 'punctuation':
                chinesePinyin = chinesePinyin.rstrip()
                chinesePinyin += item.get('hanzi')
            else:
                chinesePinyin += item.get('pinyin')
                chinesePinyin += ' '

            if item.get('new'):
                ref = self.ref.get(item.get('hanzi'))
                if ref:
                    item['level'] = ref['level']
                    item['translation'] = ref['translations'][0]

        data = {
            'tokens': store,
            'hanzi': s,
            'pinyin': chinesePinyin.strip(),
        }
        if timestamp:
            data['timestamp'] = timestamp
        return data
        return store

def makehsk():
    """ asdfd2 """
    hskjsonfile = "/mnt/chromeos/GoogleDrive/MyDrive/JSONS/hsk-master.json"
    path = npath(hskjsonfile, 'hsk-dict')
    dprompt(path)
    data = read(hskjsonfile)
    store = {}
    for item in data:
        t = item.get('translations')[0]
        store[item.get('hanzi')] = item

    write(path, store)
    save(path, mode='python')
    return store
    
class Watcher:
    def __init__(self):
        self.seen = set()
    def __contains__(self, x):
        if x in self.seen:
            return True
        else:
            self.seen.add(x)
            return False


    #return fn.__doc__

def zokarious():
    write(npath('drive', 'foo.js'), 'aaa')

def map2(items, fn, **kwargs):
    if not fn:
        return items
    store = []
    for index, originalItem in enumerate(list(items)):
        try:
            value = fn(originalItem)
            if value == None:
                continue
            store.append(value)
        except Exception as error:
            errorPrompt(index, originalItem, error)
    if kwargs.get('sort'):
        return sort(store, kwargs.get('sort'))
    return store
        

def errorPrompt(*args, **kwargs):
    
    import inspect
    caller = getCaller()
    message = 'Error at: ' + caller
    for i, arg in enumerate(args):
        try:
            vars = inspect.currentframe().f_back.f_locals.items()
            e = [v_name for v_name, v_val in vars if v_val is arg]
            name = e[0]
            kwargs[name] = arg
        except Exception as e:
            message += ': ' + arg
        
    print(message)
    pprint(kwargs)
    return input('')

def makeFileDictResource():
    s = json.dumps(env.dirdict)
    appendVariable(s)

def chooseMultiple(items, fn=0):
    display = map2(items, fn)
    message = 'choose 1 based indexes'
    indexes = rangeFromString(prompt(number(display), message))
    return map2(indexes, lambda x: items[x])

s = '''
00:00:47,292 --> 00:00:49,487
電視機前的觀眾朋友大家好
'''

def getCookUpAStormSubtitles():
    
    def f(x):
        start, end, chinese = x
        data = jieba.cut(chinese, timestamp=[start, end])
        data['timestamp'] = {
            'from': start,
            'to': end,
        }
        promptOnce(data)
        return data

        

    file = glf()
    print(file)
    return 
    s = read(file)
    return print(len(s))
    r = r'(\d+:\d+:\d+).*?(\d+:\d+:\d+).*?\n([\u4e00-\u9fff]+)'
    jieba = Jieba(convert='tw2s')
    data = map2(re.findall(r, s), f)
    outpath = 'cookUpAStorm.jieba.json'
    path = npath('drive', addExtension(outpath, 'json'))
    prompt(path)
    write(path, data)


class ReadParse:
    def __init__(self, x):
        self.text = read(x)
        print(type(self.text))
        prompt()
        
    def run(self, fn, outpath):
        prompt(type(self.text))
        results = fn(self.text)
        path = npath('drive', addExtension(outpath, 'json'))
        dprompt(path)
        write(path, results)
    
def dprompt2(*args):
    dprint2(*args)
    print('----------------------------')
    print('press anything to continue')
    input()

def dprint2(*args):
    import inspect
    store={}
    for arg in args:
        try:
            vars = inspect.currentframe().f_back.f_locals.items()
            name = [v_name for v_name, v_val in vars if v_val is arg][0]
            store[name]=arg
        except Exception as e:
            store[arg] = True
        
    for k,v in store.items():
        print('key:', k, '         value:', v)




def stringBreaker(s, key):
    r = '[\w\W]+?' + key + '\s*'
    print(r)
    return re.sub(r, '', s)

def chineseMovieJiebaConverter(file, title, breaker=0):
    assert(isfile(file))
    name = camelCase(title)
    outpath = npath('jsondrive', name + '.jieba.json')
    
    dprompt(name, outpath)
    appleBreaker = 'face into\.\.\.'

    s = read(file)
    jieba = Jieba(convert='tw2s')

    if breaker:
        s = stringBreaker(s, breaker)
    s = linegetter(s)
    def parser(s):
        x = split(s, ',')
        a = x[1]
        b = x[2]
        c = x[-1]
        c = re.sub(notChineseRE, '', c)
        return jieba.cut(c, timestamp=[a,b])

    items = map2(s, parser)
    payload = {
        'title': title,
        'contents': items,
    }
    write(outpath, payload)

def filesFromString(s, e=''):
    dir, *items = linegetter(s)
    return map2(items, lambda x: npath(dir, addExtension(x, e)))

def doFonts(s):

    examplstr1689969711 = """
    todo
    ZCOOL_KuaiLe
    Zhi_Mang_Xing
    Liu_Jian_Mao_Cao
    Long_Cang
    """

    def fonter(file):
        files = FileState(file).unzip(fontdir)
        prompt(files)
        return files
    
    assert(isdir(fontdir))
    files = filesFromString(s, e='zip')
    allfiles = flat(map2(files, fonter))
    save(allfiles)

def hskPaperTests():
    chdir(trashdir)
    f = FileState(glf())
    files = f.unzip()
    names = map2(files, tail)
    names.sort()
    f = lambda x: toNumber(search('H\d(\d+)\.docx', x))
    transcriptIds = map2(names, f)
    checkpoint = checkpointf(extensions=['ogg', 'mp3'])
    audios = filter(names, checkpoint)

    checkpoint = checkpointf(extensions=['docx'])
    transcripts = filter(names, checkpoint)

    checkpoint = checkpointf(extensions=['pdf'], keepRE='answer', flags=re.I)
    exams = filter(names, checkpoint)

    checkpoint = checkpointf(extensions=['pdf'], keepRE='exam', flags=re.I)
    answers = filter(names, checkpoint)
    def boo(id, items):
        r = str(id)
        return find(items, lambda x: test(r, x))

    def parser(id):
        a = boo(id, audios)
        b = boo(id, exams)
        c = boo(id, answers)
        if not a:
            return 
        if not b:
            return 
        if not c:
            return 

        d = boo(id, transcripts)
        return [a, b, c, d]

    filePacks = map2(transcriptIds, parser)
    prompt(filePacks)

    for filePack in filePacks:
        files = npath(trashdir, filePack)

def toNumber(x):
    try:
        return int(x)
    except Exception as e:
        return 
        
    


def sortByDate(files, reverse=0):
    files.sort(key=mdate, reverse=reverse)
    return files



def filePicker(dir=dldir, **kwargs):
    saveIt = kwargs.pop('save', True)
    files = getFiles(dir, **kwargs)
    chosen = chooseMultiple(files, tail)
    if saveIt:
        save(chosen, mode='python', current=1)

f = '/mnt/chromeos/GoogleDrive/MyDrive/JSONS/storyOfYangxiPalace.jieba.json'
files = ["/mnt/chromeos/MyFiles/Downloads/2e1138925e9cc4385bf450593750cc57d2825701e8fc93a6a3ab1708ff2fc541-2023-05-06-03-43-21.zip", "/mnt/chromeos/MyFiles/Downloads/2e1138925e9cc4385bf450593750cc57d2825701e8fc93a6a3ab1708ff2fc541-2023-07-20-01-00-46.zip"]

def parseChatgptZipFiles():
    ''' gpt chat chatgpt openai '''

    def parser(file):
        promptIt = 1
        file = FileState(file)
        targetFile = file.unzip(trashdir, target='conversations.json')
        cfile(npath(trashdir, 'chat.html'), incName('Chatgpt.html', dir='drive', prompt=promptIt))
        data = read(targetFile)
        payload = map2(data, parseConversation)
        prompt(payload[0], 'first item of the payload')
        incwrite('Chatgpt', payload, prompt=promptIt)
        file.remove()
        prompt('success')
        return True

    r = '\w+(?:-\d+){6}\.zip'
    return getFiles(dldir, r=r, sort=1, prompt=0, parser=parser)

def parseConversation(x):
    def parser(item):
        message = item.get('message')
        if not message:
            return 
        author = message.get('author').get('role')
        if author == 'system':
            return 

        timestamp = message.get('create_time')
        id = item.get('id')
        parentId = item.get('parent')
        contentParts = message.get('content').get('parts')
        content = join(contentParts)
        return {
            'author': author,
            'id': id,
            'parentId': parentId,
            'timestamp': timestamp,
            'text': content,
        }

    title = x.get('title')
    id = x.get('id', None)
    timestamp = x.get('create_time', None)
    mapping = x.get('mapping')
    contents = map2(mapping.values(), parser)
    return {
        'title': title,
        'id': id,
        'timestamp': timestamp,
        'contents': contents,
    }

def incName(name, dir='jsondrive', **kwargs):
    aliases = {
        'ffr': 'File Function Ref',
    }
    name = aliases.get(name, name)
    promptIt = kwargs.get('prompt', None)
    if promptIt:
        dprompt2(name)
    name = incrementalName(npath(dir, addExtension(name, 'json')))
    return name


def incwrite(name=0, payload=0, prompt=0, save=1):
    n = incName(name, dir='jsondrive', prompt=prompt)
    write(n, payload, save=save)

def findFile2(files, r):
    fn = testf(r)
    names = map(files, tail)
    index = find(files, fn, mode=int)
    if index == None:
        return 
    return files[index]

def moveFontsToFontDir():
    fonts = getFiles(fonts=1)
    prompt(fonts)
    pprint(mfiles(fonts, dir=fontdir))


def clickThrough(chunks):
    for chunk in chunks:
        prompt(chunk)


ftpdir='/home/kdog3682/.vim/ftplugin/'
temp = [
    "/home/kdog3682/.vim/ftplugin/vim.vim",
    "/home/kdog3682/.vim/ftplugin/html.vim",
    "/home/kdog3682/.vim/ftplugin/css.vim",
    "/home/kdog3682/.vim/ftplugin/math.vim",
    "/home/kdog3682/.vim/ftplugin/python.vim",
    "/home/kdog3682/.vim/ftplugin/txt.vim",
    "/home/kdog3682/.vim/ftplugin/markdown.vim",
    "/home/kdog3682/.vim/ftplugin/javascript.vim"
]
'/home/kdog3682/.vim/after/ftplugin/vim.vim'
'/home/kdog3682/.vim/after/ftplugin/python.vim'
ftplugindir="/home/kdog3682/.vim/ftplugin/"

def mfiles(files=0, dir=0, to=0):
    if isArray(dir):
        to = dir

    if to:
        assert len(files) == len(to)
        for i, file in enumerate(files):
            mfile(file, to[i])
    elif dir:
        for file in files:
            mfile(file, dir)
    



def getSetStoreDecorator(file):
    base = read(file) or {}

    def wrapper(fn):
        def decorator(*args, **kwargs):
            value = fn(*args, **kwargs)
            base.update(value)
            write(file, base)
            pprint(base)
            return base
        return decorator
    return wrapper

def htmlRE(key):
    r = f'<{key}[\w\W]*?>([\w\W]+?)</{key}>'
    return r

@getSetStoreDecorator('svg-paths.json')
def createSvgPathLibrary(files):
    def parse(s):
        r = htmlRE('svg')
        r2 = htmlRE('style')
        r3 = '\r\n\t'
        value = re.sub(r3, '', re.sub(r2, '', search(r, s).strip()))
        assert value
        return value

    store = {}
    for file in toArray(files):
        name = re.sub('-(?:svgrepo).*', '', tail(file))
        s = read(file).decode()
        store[name] = parse(s)
        rfile(file)

    return store

temp = [
    "/mnt/chromeos/MyFiles/Downloads/clipboard-list-svgrepo-com.svg",
    "/mnt/chromeos/MyFiles/Downloads/clipboard-check-svgrepo-com.svg",
]
def createVariable2(name, value, prefix=None):
    value = dumpJson(value)
    if prefix: prefix += ' '
    s = f"{prefix}{name} = {value}"
    return s

def jsonToJavascript(file):
    assert(isJson(file))
    name = camelCase(removeExtension(file))
    #value = list(read(file).values())[2]
    print(json.dumps(read(file)))
    return 
    payload = 'export default ' + value
    outpath = file + '.js'
    write(outpath, payload)
    save(outpath)


def getN(items, n):
    if n > 0:
        return items[0:n]
    else:
        return items[n:]

gitignorefile = '/home/kdog3682/2023/.gitignore'




def appMoveLastFilesFromDownloadToMaindirAndGitIgnore(n):
    
    if n > 0:
        print('maybe n should be less than 0 ... early return')
        return 

    files = getFiles(dldir, n)
    def fn(file):
        name = tail(file)
        e = getExtension(name)
        a = search('[a-zA-Z]\w+$', removeExtension(name))
        return a + '.' + e
    names = map(files, fn)
    dprompt(names)
    mfiles(files, names)
    append(gitignorefile, join(names))

temp = [
    "/home/kdog3682/.vimrc",
    "/home/kdog3682/2023/cm.esm.js",
    "baseComponents.js",
    "changelog.md",
    "cm3.js",
    "utils.js",
    "/home/kdog3682/2023/cm-next.js",
    "/home/kdog3682/2023/pl-htmlBuilder.js",
    "/home/kdog3682/2023/pl-create.js",
    "/home/kdog3682/2023/xmlString.js",
    "class.js",
    "raw.js",
    "/home/kdog3682/2023/rp.js",
    "/home/kdog3682/2023/codeOrganizer2.js",
    "cm-lezer.js",
    "Lezer2.js",
    "save.txt",
    "saved.txt",
    "runVite.js",
    "git-data3.json",
    "/home/kdog3682/CLIPS/file-identifier-reference.june.json",
    "/home/kdog3682/.vim/ftplugin/markdown.vim",
    "/home/kdog3682/.vim/ftplugin/javascript.vim",
    "/home/kdog3682/2023/browser-utils.js",
    "/home/kdog3682/DIST/pl-htmlBuilder.js",
    "./juneJson.json.js",
    "/home/kdog3682/2023/setupComponent.js",
    "/home/kdog3682/2023/next.js",
    "/home/kdog3682/2023/variables.js",
    "./pl-invivoVueBuilder.js",
    "file-table.txt",
]


def rnc(newName=None):
    """
        writes to jsondrive in an incremental manner
        generally used for json type clips (like data aggregation)
    """
    name = incName(newName, dir='jsondrive', prompt=1)
    mfile('clip.js', name)

def fileDate(f):
    strife = "%A %B %d %Y, %-I:%M:%S%p"
    return datestamp(mdate(f), strife)


def gjf(hours=0):
    # get javascript files
    files = getFiles(js=1, sort=1, reverse=1, hours=int(hours))
    files = map(files, lambda x: x + ' :: ' + fileDate(x))
    s = join(comment(datestamp()), files)
    append('files.txt', s)

def folders():
    files = getFiles(folders=1, sort=1)
    pprint(files)

a = 1
b = 2
def read2(file):
    textExtensions = [
        "js",
        "css",
        "html",
        "py",
        "txt",
        "md",
    ]

    e = getExtension(file)
    mode = "r" if e in textExtensions else "rb"
    with open(file, mode) as f:
        return f.read()

def allFiles(dir):
    store = []
    for root, _, files in os.walk(dir):
        for file in files:
            path = os.path.join(root, file)
            store.append(path)
    return store

def viteMover():
    dir = "/home/kdog3682/2023/dist/"
    indexFile = find(absdir(dir), 'html$')
    mfile(indexFile, dir + 'index.html')
    dir = "/home/kdog3682/2023/dist/assets/"
    files = allFiles(dir)
    def runner(file):
        e = getExtension(file)
        if e == 'js':
            path = npath(dir, 'main.js')
            mfile(file, path)
            return path
        elif e == 'css':
            path = npath(dir, 'style.css')
            mfile(file, path)
            return path
        else:
            return file
    results = map(files, runner)
    return results

def findFileString(s):
    r = '/\S+'
    return search(r, s)

def askof():
    r = '^#.+'
    s = read('files.txt')
    item = re.split(r, s, flags=re.M)[-1]
    files = unique(linegetter(item, fn=findFileString))
    assert(every(files, isfile))
    def runner(item):
        if isLibraryFile(item):
            return 
        info = fileInfo(item)
        identifiers = getFunctionNames(item)
        info['identifiers'] = identifiers
        return info
    clip(map(files, runner))
    #return files

def getFiles2(dir=dir2023, **kwargs):

    checkpoint = checkpointf(**kwargs)
    dir = dirGetter(dir)

    def parse(file, depth):
        if isIgnoredFile2(file):
            return 
        elif isfile(file):
            return tail(file)
        elif checkpoint(file):
            if depth > 3 and not prompt(file):
                return log(file)
            return runner(file, depth + 1)

    def runner(dir, depth=0):
        children = []
        for file in absdir(dir):
            try:
                push(children, parse(file, depth))
            except Exception as error:
                errorPrompt(file, error)

        if empty(children):
            return 

        return {
            'dir': dir,
            'items': children,
        }

    return runner(dir)

def log(x=0):
    if x == None:
        return 

    append('temp.txt', str(x))


def zipToDrive(files, out):
    files = getFiles(files)
    outpath = incrementalName(npath('drivezip', addExtension(out, 'zip')))
    from zipscript import zip
    dprompt(files, outpath)
    zip(files, outpath)

def getDrive(x):
    d = drivedir + x.upper()
    assert isdir(d)
    return d


def isPublic(x):
    return test('^\w', tail(x))

def rmdirs(dirs):
    prompt('removing the following directories', dirs)
    for dir in dirs:
        rmdir(dir)

class DirectoryManager:
    def __init__(self):
        self.dirs = filter(absdir(rootdir), isdir, isPublic)
        dirs = chooseMultiple(self.dirs)
        rmdirs(dirs)

def aaarenameClipToDriveFile():
    newName = prompt('name for drive clip file?')
    cfile(clipfile, drivedir + newName)

    
def mget2(r, s):
    store = []
    def parser(x):
        m = x.groups()
        m = m if m else x.group(0)
        store.append(m)
        return ''

    text = re.sub(r, parser, s).strip()
    return [text, smallify(store)]

def doFileTable():
    
    def parseFileTable(s):
        r = '(?:(d|res|del|skip)|(rn|Dialogue|dia): *(.+)) *$'
        name, m = mget2(r, s)
        if not m:
            if isRemovableFile(name) or 'temp' in name:
                return rfile(name)
            return 

        return 
        deleteIt, renameIt, newName = m
        if deleteIt:
            if deleteIt == 'res':
                return mfile(name, resdir)
            if deleteIt == 'skip':
                return 
            return rfile(name)
        elif renameIt:
            if renameIt == 'rn':
                return mfile(name, changeName(newName, name))
            else:
                mathdir = '/home/kdog3682/MATH/'
                outpath = npath(mathdir, addExtension(name, 'txt'))
                return mfile(name, outpath)

    s = lastItem(vimftfile, mode='date')
    payload = linegetter(s, fn=parseFileTable)

def changeName(newName, name):
    head, tail = os.path.split(name)
    base = os.path.join(head, newName)
    return addExtension(base, getExtension(tail))

def lastItem(x, mode=None):
    s = textgetter(x)
    if mode == 'date':
        items = re.split('^\d+-\d+.*', s, flags=re.M)
    else:
        items = re.split('\n\n+', s)

    return items[-1]

def csvReader(file, fn=0):
    def parse(s):
        items = re.split(' *, *', s)
        if fn:
            return fn(items)
        else:
            return items
    items = linegetter(file, fn=parse, skip=1)
    return items

def submit(name, value, debug=0):
    if not value:
        return 
    if isString(value):
        prompt('hmm not set up yet')
        return 

    if debug: return pprint(value)
    outpath = npath(drivejsondir, addExtension(name, 'json'))
    write(outpath, value, open=1)


 
data = [
    {'name': 'Norah Wang', 'birthday': '9/28/2021'},
]






def emptyTrash():
    dir = trashdir
    assert isdir(dir)
    rmdir(dir, force=1)
    mkdir(dir)

def cleanup10(dir, size=150):
    files = getFiles(dir, smallerThan=size)
    rfiles(files)

def parseCsvBabyNameFrequencies():
    
    """
        date: 09-14-2023 
        entry: /home/kdog3682/TEXTS/yob2016.txt (deleted)
        data:
            Name,Sex,BirthCount
            Emma,F,19414
            Olivia,F,19246

        output: Popular Baby Names with Frequencies
        type: json
        schema: {
            boys: [(sam, 4)],
            girls: [(samantha, 4)],
        }

        notes: 
            cut off at frequencies less than 50
    """

    def parse(items):
        try:
            name, sex, count = items
            count = int(count)
            if count < 50:
                return 
        except Exception as e:
            return 

        if sex == 'F':
            girls.append((name, count))
        else:
            boys.append((name, count))

    boys = []
    girls = []
    items = csvReader(file, fn=parse)
    payload = {'boys': boys, 'girls': girls}
    submit('Popular Baby Names with Frequencies', payload)



def flattenAllDirectoriesWithinTheDirectory(dir):
    dirs = getFiles(dir, folders=1)
    for d in dirs:
        mfiles(absdir(d), dir)
        rmdir(d)

def moveAllPicturesToDrive(dir):
     pics = getFiles(dir, images=1)
     if not pics:
         printdir(dir)
         return print('no pics')
     print('a')
     prompt(pics)
     print('a')
     mfiles(pics, drivedir + 'PICTURES 2023')


def moveDriveFilesToDriveFolders(key, **kwargs):
    files = getFiles(drivedir, **kwargs)
    dir = f"{drivedir}{key.upper()} {getYearNumber()}"
    prompt(files)
    mfiles(files, dir)


def iqr(data):
    import numpy as np
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    def checkpoint(file):
        return lower_bound <= fsize(file) <= upper_bound

def review(files):
    def runner(file):
        a = prompt(file)
        if a == 'm':
            mfile(file, 'res')
        elif a == 'd':
            rfile(file)
        elif a == 'o':
            ofile(file)
            return runner(file)

    for file in files:
        runner(file)


def printdir(dir=dldir, printIt=0):
    dir = dirGetter(dir)
    files = os.listdir(dir)
    size = len(files)
    if size < 30:
        files = map(files, lambda f: normpath(dir, f))
        pprint(map(files, fileInfo))
    else:
        files = sorted(files)
        pprint(files)

    dprint(size, dir)
    if printIt:
        append(vimftfile, join(datestamp(), files))
    return files

def mfiles(files, dir, fn=0, ask=0):
    files = absdir(files)
    dir = dirGetter(dir)

    if ask:
        prompt(files, f"move the files to {dir}?")

    for f in files:
        if fn:
            dir = fn(dir + fn(tail(f)))
        if isfile(npath(dir, f)):
            if prompt('the file exists: are you sure you want to overide? type [y]es to confirm', tail(f)):
                mfile(f, dir)
        else:
            mfile(f, dir)


def sprawldir(dir, folder):
    items = getFiles(dir, name=folder, folders=1)
    while 1:
        if len(items) == 1 and isdir(items[0]):
            items = absdir(items[0])
        else:
            return items

fruits = [
  "apple",
  "banana",
  "cherry",
  "date",
  "elderberry",
  "fig",
  "grapes",
  "honeydew",
  "kiwi",
  "lemon",
  "mango",
  "nectarine",
  "orange",
  "pineapple",
  "raspberry",
  "strawberry",
  "watermelon",
][0:5]

str1695228324 = """
    fruits.pop(0)
    fruits.pop(1)
    fruits.pop(-1)
"""

def evaluate_text_invivo_for_python_article(s):
    lines = linegetter(s)
    for line in lines:
        eval(line)
        print(line, fruits)

def buildRequirements():
    """
        So this file does
    """
    def clean(s):
        return search('\S+', s)

    def runner(file):
        s = read(file)        
        r = '^(?:import|from) (\S+)'
        m = re.findall(r, s, flags=re.M)
        return m

    def checkpoint(file):
        f = npath(pydir, addExtension(file, 'py'))
        return not isfile(f)

    files = getFiles(pydir, py=1)
    imports = filter(unique(flat(map(files, runner))), checkpoint)
    imports.sort()
    prompt(imports)
    s = SystemCommand('pip list', dir=pydir)
    packages = linegetter(s.success, fn = clean)[2:]

    libraries = filter(imports, lambda x: x in packages)

    return {
        'packages': packages,
        'allImports': imports,
        'imports': libraries,
    }


def checkpointf(
    kb=0,
    keepRE=0,
    contains=0,
    gdoc=0,
    deleteIt=0,
    deleteRE=0,
    include="",
    size=0,
    svg=0,
    maxLength=0,
    image=0,
    images=0,
    today=0,
    flags=re.I,
    fonts=0,
    files=0,
    gif=0,
    weeks=0,
    month=0,
    old=0,
    ignore="",
    ignoreRE="",
    css=0,
    js=0,
    zip=0,
    py=0,
    txt=0,
    html=0,
    pdf=0,
    date=0,
    name=0,
    big=0,
    r=0,
    antiregex=0,
    anti=0,
    small=0,
    before=0,
    after=0,
    minLength=0,
    minutes=0,
    days=0,
    hours=0,
    regex=0,
    public=1,
    private=0,
    math=0,
    text=0,
    lib=0,
    log=0,
    onlyFiles=0,
    isf=0,
    isp=0,
    onlyFolders=0,
    folders=0,
    biggerThan=0,
    smallerThan=0,
    fn=0,
    e=0,
    json=0,
    vimInfo=0,
    **kwargs,
):
    if vimInfo:
        name = '^\.viminf[^o]'
        private = 1
    if private:
        public = 0
    if kb:
        smallerThan = kb * 1000
    if size:
        biggerThan = size
    if text:
        onlyFiles = 1
    if isf:
        onlyFiles = 1
    if r:
        keepRE = r
    extensions = kwargs.get("extensions", [])
    if kwargs.get("isdir"):
        onlyFolders = 1

    if fonts:
        extensions.extend(fonte)
    if log:
        extensions.append("log")
    if gdoc:
        extensions.append("gdoc")
        extensions.append("gsheet")

    if math:
        extensions.append("math")
    if css:
        extensions.append("css")
    if js: extensions.append("js")
    if svg: extensions.append("svg")
    if zip: extensions.append("zip")
    if json: extensions.append("json")
    if py:
        extensions.append("py")
    if txt:
        extensions.append("txt")
    if html:
        extensions.append("html")
    if pdf:
        extensions.append("pdf")
    if gif:
        extensions.append("gif")
    if image or images:
        for e in imge:
            extensions.append(e)
    if isArray(e):
        extensions.extend(e)
    elif e:
        extensions.append(e)

    if old:
        hours = 24 * 30
    elif days:
        hours = days * 24
    elif weeks:
        hours = 24 * 7 * weeks
    elif month:
        hours = 24 * 30
    elif today:
        hours = 12

    if include:
        print("deleting")
        include = xsplit(include, "\s+")
    if ignore:
        ignore = xsplit(ignore, "\s+")
    if deleteIt:
        isp = 1


    alwaysIgnore = [
        "vosk-api",
        "__pycache__",
        "node_modules",
        "readme.md",
        "license.md"
        ".git",
    ]
    def runner(f):
        filename = tail(f)

        if filename in alwaysIgnore:
            print("always ignore")
            return False

        if fn and not fn(f):
            return False

        if public and test('^\.', filename):
            return False
        if include and filename in include:
            return True
        if folders and not isdir(f):
            return False
        if ignore and filename in ignore:
            return False
        if isp and filename.startswith("."):
            return False
        if deleteIt and alwaysDelete(f):
            rfile(f)
            return False
        if regex and not test(regex, filename, flags=flags):
            return False
        if antiregex and test(antiregex, filename, flags=flags):
            return False

        if keepRE and not test(keepRE, filename, flags=flags):
            return False

        if deleteRE and test(deleteRE, filename, flags=flags):
            rfile(f)
            return False

        print(filename)
        if name and not test(name, filename, flags=flags):
            return False

        e = getExtension(filename)

        if text and e == 'pdf':
            return False

        if anti:
            nevermove = ['.git', 'node_modules', 'package.json', 'screenshot.jpg', '.vimrc', '.gitignore', 'package-lock.json']

            if e in extensions:
                return False
            if filename in nevermove:
                return False
            if isdir(f):
                return False
            #if fsize(f) < 50:
                #rfile(f)
                #return False
            
        elif extensions and e not in extensions:
            return False

        if minutes and not isRecent(f, minutes=minutes):
            return False

        if hours and not isRecent(f, hours=hours):
            return False

        if not lib and isLibraryFile(f):
            return False

        if onlyFiles and isdir(f):
            return False

        if contains:
            if not isdir(f):
                return True
            gn = lambda x: getExtension(x) == contains
            files = filter(os.listdir(f), gn)
            if len(files) < 5:
                print(f, 'has some files but not enuf of ', contains)
                return False
            return True

        if onlyFolders:
            if isdir(f):
                return 1
            return False

        if maxLength and isString(f) and len(f) > maxLength:
            return False

        if minLength and isString(f) and len(f) < minLength:
            return False

        if biggerThan and fsize(f) < biggerThan:
            return False
        if smallerThan and fsize(f) > smallerThan:
            return False
        if big and fsize(f) < big:
            return False
        if ignoreRE and test(ignoreRE, filename, flags=re.I):
            return False
        if text and not test(text, read(f), flags=flags):
            return False
        if date and not isSameDate(date, f):
            return False
        return True

    return trycatch(runner)
def note(*args):
    a = map(args, str)
    s = f"Note: {longstamp()} :: "
    s += json.dumps(a)
    append(temptextfile, s)
    prompt(s)


def chalkf(color, mode=0):

    reset = "\033[0m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"
    purple = "\033[35m"
    cyan = "\033[36m"
    bold = "\033[1m"

    colors = {
        'blue': blue,
        'red': red,
        'green': green,
        'yellow': yellow,
        'purple': purple,
        'cyan': cyan,
    }
    color = colors[color]

    def getDelimiter(a, b = None):
        if isString(b):
            if '\n' in b:
                return '\n'
            elif str(a).endswith(':'):
                return ''
        return ':'

    def promptChalk(a, b):
        delimiter = getDelimiter(a, b)
        print(bold + color + capitalize(a) + delimiter + reset, b)
        input()

    if mode == prompt:
        return promptChalk

    def chalk(*args, **kwargs):
        delimiter = getDelimiter(*args)
        if kwargs.get('bold') or isCapitalized(args[0]):
            print(bold + color + str(args[0]) + delimiter + reset, *args[1:])
        else:
            print(color + str(args[0]) + reset, *args[1:])

    return chalk

def isCapitalized(s):
    return test('^[A-Z]', s)

blue = chalkf('blue')
red = chalkf('red')


def sleep(n):
    time.sleep(n)

def warn(*args):
    red(*args)
    prompt('Exit')


def getChunks(s):
    r = '\n+(?=[\w.#])'
    trim = lambda x: x.strip()
    items = re.split(r, s.strip())
    return map(items, trim)


def dateTheFile(name):
    e = getExtension(name)
    name = removeExtension(name)
    return name + '.' + datestamp() + '.' + e

def v1(file):
    newName = npath(drivedir + 'DEPRECATED/', file)
    newName = dateTheFile(newName)
    prompt(newName)
    mfile(file, newName)

def getBackupFile(file):
    files = os.listdir(budir)
    f = lambda x: re.sub('\.\d+-\d+-\d+', '', x) == file
    files = filter(files, f)
    return npath(budir, files[-1])

def checkBackup(file):
    originalFile = file
    file = getBackupFile(file)
    print(read(file))
    blue('file', file)
    blue(linebreak)
    blue('original file', originalFile)
    blue('text', read(originalFile))
    blue(linebreak)

def revert(file):
    file = getBackupFile(file)
    dprompt2(file)
    warn('still in progress')
    if 'vimrc' in file:
        return cfile(file, '/home/kdog3682/.vimrc')

    dir = dir2023
    localPath = npath(dir, re.sub('\.\d+-\d+-\d+', '', file) )
    cfile(file, localPath)

env.basepyref['ff'] = 'getFilesWrapper'
def assertion(arg, requirement=None, message=None):
    if isFunction(requirement):
        if requirement(arg):
            return 
        red('Assertion requirement was not met', requirement.__name__)
        red('Arg', arg)
        raise Exception(message or '')
    else:
        if not arg:
            red('Assertion was not met', 'the arg is null')
            raise Exception(message or '')

def isHtmlFile(x):
    return getExtension(x) == 'html'


def makeSampleNestedFolder(dir=trashdir):
    files = [
        'abc/fileA.js',
        'abc/fileB.js',
        'abc/fileC.js',
        'abc/def/fileD.js',
        'abc/def/fileE.js',
        'abc/def/fileF.js',
    ]
    f = lambda file: forceWrite(os.path.join(dir, file), 'hi')
    map(files, f)
    pprint(getFiles(dir, recursive=1))

def forceWrite(file, s):
    head, tail = os.path.split(file)
    if not isdir(head):
        mkdir(head)
    write(file, s)

def removeHead(s):
    known = [
        '/home/kdog3682/2023',
        '/home/kdog3682/2023/dist',
    ]
    for known in known:
        if known in s:
            s = s.replace(known, '')
            break

    if s.startswith('/'):
        s = s[1:]

    return s



def shell(*args):
    def fixError(s):
        known = []
        if s in known:
            return ''
        r = '^(?:hint)'
        if test(r, s, flags=re.I):
            return ''
        return s

    def fixArg(s):
        if "\n" in s:
            return ';'.join(linegetter(s))
        return s
        
    from subprocess import Popen, PIPE

    command = map2(flat(args), fixArg).join(' ')
    process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
    data = process.communicate()
    success, error = [decode(d).strip() for d in data]
    error = fixError(error)

    blue('success', success)
    blue('error', error)

    return dict(success=success, error=error)

def javascript(file, *args):
    return shell('node', file, args)

def python(file, *args):
    return shell('node3', file, args)

# backupFolder('/home/kdog3682/.vim/ftplugin/')

Blue = chalkf('blue', prompt)
Red = chalkf('red', prompt)
# Blue('hi', 1)


def parseRedditString(s):
    r = '(\w+) (.*?)  ([\w\W]+)'
    m = search(r, s)
    if not m:
        return 
    a, b, c = m
    subreddit = env.subreddits.get(a, a)
    title = capitalizeTitle(b)
    body = toParagraph(c)
    return (subreddit, title, body)

def capitalizeTitle(title):
    if isCapitalized(title):
        return title
    smallWords = ["a", "an", "the", "and", "but", "or", "for", "nor", "on", "at", "to", "from", "by", "with"]

    def cap(word, i):
        if i == 0 or word.lower() not in smallWords:
            return word.capitalize()
        else:
            return word

    words = title.split()
    s = [cap(w, i) for i,w in enumerate(words)]
    return " ".join(s)

def shared(a, b):
    return list(set(a) & set(b))

def getArgsKwargs(fn, config, transform=None):
    argList, kwargList = getParameters2(fn)

    store = {}
    def get(key):
        if key == 'config':
            return {k:toArgument(v) for k,v in config.items()}
        try:
            a = config.get(key)
            t = transform.get(key) if transform else None
            value = t(a) if t else a
            store[key] = value
            return value
        except Exception as e:
            error = str(e)
            message = 'the error is in the transformer. Please Exit.'
            transformer = transform.get(key)
            prompt({"error": error, "message": message, "transformer": transformer, "key": key, "value": a})
            raise e
    
    fnArgs = filter(map2(argList, lambda x: get(x)))
    fnKwargs = reduce(kwargList, lambda x: [x, get(x)])
    blue('ParamRef @getArgsKwargs', store)
    return [fnArgs, fnKwargs]

def prettyProse(s):
    return s

def getParameters(s):
    m = search('\((.*?)\)', s)
    if m:
        parts = re.split(', *', m)
        args = []
        kwargs = []
        for part in parts:
            if test('\*\w', part):
                continue
            elif test('\w+ *=', part):
                kwargs.append(re.split(' *= *', part))
            else:
                args.append(part)
        return [args, kwargs]

def getParameters2(fn):
    import inspect
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


def compose(*functions):
    def composed(*args, **kwargs):
        result = None
        for i, fn in enumerate(reversed(flat(functions))):
            result = fn(*args, **kwargs) if i == 0 else fn(result)

        return result

    return composed

class Config:
    def __init__(self, x):
        d = dict(x)
        for k,v in d.items():
            setattr(self, k, v)
        
def mapFilter(items, fn = None):
    store = []
    for item in list(items):
        if fn:
            value = fn(item)
            if hasValue(value):
                if isinstance(value, bool):
                    store.append(item)
                else:
                    store.append(value)
        elif hasValue(item):
            store.append(item)
    return store

def packageManager(fn):
    args = sys.argv
    if len(args) == 1:
        red('PackageManager', 'no arg = no run')
    else:
        fn(*map(args[1:], toArgument))



def toCallableFromConfig(name, params, config):
    def fix(s):
        if test('\n', s):
            escaped = re.sub('\n', '\\\\n', s)
            return f'"""{escaped}"""'
        elif isNumber(s):
            return s
        elif isJsonParsable(s):
            return json.dumps(s)
        else:
            return singleQuote(s)
    args, kwargs = params
    store = []
    for arg in args:
        v = config.get(arg)
        if v != None:
            push(store, fix(v))
    for a,b in kwargs:
        v = config.get(a)
        if v != None:
            push(store, f"{a} = {fix(v)}")

    paramString = ', '.join(store)
    return f"{name}({paramString})"


def tomorrow():
    date = datetime.today() + timedelta(days=1)
    return date.strftime("%m-%d-%Y")

def pick(items, display = identity, get = identity):

    for i, item in enumerate(items):
        blue(i + 1, display(item))

    indexes = rangeFromString(input('Select 1-based indexes: '))

    store = [get(el) for i,el in enumerate(items) if i in indexes]
    return smallify(store)


def getIdentifier(s):
    r = '^(?:class |def )(\w+)|^(\w+) *= *'
    m = search(r, s)
    if m:
        return m[0] or m[1]

def codeLibrary(s):
    r = '\n+(?=class|def|\w+ *=)'
    items = re.split(r, s)
    
    def runner(s):
        text = s.strip()
        name = getIdentifier(text)
        if name:
            params = getParameters(text)
            return { 'name': name, 'params': params, 'text': text, }
    
    return mapFilter(items, runner)

# print(codeLibrary('\n' + toString(codeLibrary)))

# c2(getFiles('/mnt/chromeos/GoogleDrive/MyDrive/CWF', py = 1))
# print(SystemCommand('curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'))


ftplugindir = "/home/kdog3682/.vim/plugged/goyo.vim"
# printdir(ftplugindir)
