import os
import inspect
from subprocess import Popen, PIPE

__alerting = 0

vimfiles = [
    "/home/kdog3682/VIM/functions.vim",
    "/home/kdog3682/.vimrc",
    "/home/kdog3682/VIM/variables.vim",
    "/home/kdog3682/.vim/ftplugin/javascript.vim",
]

linebreak = "-" * 50
hammyfirebasehtml = (
    "/home/kdog3682/FIREBASE/public/index.html"
)
localbackupdir = "/home/kdog3682/LOCALBACKUP/"
publishdir = "/home/kdog3682/PUBLISHED/"
firebasedir = "/home/kdog3682/FIREBASE/"
publicfirebasedir = "/home/kdog3682/FIREBASE/public"
latexdir = "/home/kdog3682/LATEX/"
alist = ["a", "b", "c", "d"]
glogfile = "/home/kdog3682/2023/log.json"
gunkExtensions = [
    "recent",
    "mp3",
    "ass",
    "eps",
    "zip",
    "url",
    "gz",
    "backup",
    "webp",
    "asy",
    "vcf",
    "js",
]
pdfdir2 = "/home/kdog3682/PDFS2/"
archdir = "/mnt/chromeos/GoogleDrive/MyDrive/ARCHIVES/"
sshfile = "/home/kdog3682/.ssh/id_rsa.pub"
dir2023 = "/home/kdog3682/2023/"
nodedir2023 = "/home/kdog3682/2023/node_modules/"
mathchadir = dir2023 + "mathcha/"
githuburl = "https://github.com/"
drivedir = "/mnt/chromeos/GoogleDrive/MyDrive/"
outdir = "/mnt/chromeos/GoogleDrive/MyDrive/OUTBOUND/"
zipdir = "/mnt/chromeos/GoogleDrive/MyDrive/ZIP/"
gdocdir = "/mnt/chromeos/GoogleDrive/MyDrive/GDOC/"
backupdir = "/mnt/chromeos/GoogleDrive/MyDrive/BACKUP/"
dropboxdir = "~/DropBox"

pythondir = (
    "/home/kdog3682/.local/lib/python3.7/site-packages"
)

pythondir = "/home/kdog3682/PYTHON/"
javascriptdir = "/home/kdog3682/JAVASCRIPT/"
swiftdir = "/home/kdog3682/SWIFT-LATEX/"
htmlbudir = "https://drive.google.com/drive/folders/16gpifAlQhHxBHr3SP0IbRiwnGLwbmF59"
teachdir = "/home/kdog3682/TEACHING/"
vimdir = "/home/kdog3682/VIM & SH/"
nodedir = "/home/kdog3682/.npm-global/lib/node_modules/"
nodedir2023 = "/home/kdog3682/2023/node_modules/"
linebreak = "-" * 50
tododir = "/mnt/chromeos/GoogleDrive/MyDrive/TODO"
boadir = "/mnt/chromeos/GoogleDrive/MyDrive/TODO/BOA"
yearRE = "20(?:[012][0123456789])"
examdir = "/home/kdog3682/EXAMS/"
productiondir = "/home/kdog3682/PRODUCTIONS/"
productiondir = "/home/kdog3682/PRODUCTIONS/"
lezfile = "/home/kdog3682/.npm-global/lib/node_modules/@lezer/html/dist/index.cjs"
filelogfile = "/home/kdog3682/LOGS/today.log"
clipdir = "/home/kdog3682/CLIPS/"

lezerdir = (
    "/home/kdog3682/.npm-global/lib/node_modules/@lezer/"
)

pubnodedir = "/home/kdog3682/CWF/public/node_modules/"
cwfnodedir = "/home/kdog3682/CWF/node_modules/"
servernodedir = "/home/kdog3682/CWF/node_modules/"
svgdir = "/home/kdog3682/SVG/"

nodemodulesdir = (
    "/home/kdog3682/.npm-global/lib/node_modules/"
)

servedir = "/home/kdog3682/SERVER/"
gmailsenturl = "https://mail.google.com/mail/u/0/#sent"
gmailurl = "https://mail.google.com/mail/u/0/#inbox"
testpdf = "/mnt/chromeos/MyFiles/Downloads/test.pdf"

googleassignmentdir = (
    "/home/kdog3682/CWF/public/assignments"
)

ONE_MINUTE = 60
homedir = "/home/kdog3682/"
rootdir = "/home/kdog3682/"
dir2023images = dir2023 + "images"
tempappscriptfile = "/home/kdog3682/appscript.temp.json"
tempfile = "/home/kdog3682/CWF/public/temp.json"
chifile = "/mnt/chromeos/GoogleDrive/MyDrive/JSONS/hsk-pinyin-dict.json"
nonutfe = ["ttf", "mp3", "gz", "gifv"]
clipfile = ".clip.js"
clipfile = "/home/kdog3682/2023/clip.js"
cvfile = "Kevin Lee Cover Letter.pdf"
resumefile = "Kevin Lee Resume.pdf"
jsdir = "/home/kdog3682/CWF/public/"
dldir = "/mnt/chromeos/MyFiles/Downloads/"
pdfdldir = dldir + "PDFS/"
sandir = "/mnt/chromeos/removable/Sandisk/"

usbdir = "/mnt/chromeos/removable/"
usbdrivedir = "/mnt/chromeos/removable/USB Drive/"
pydir = "/home/kdog3682/PYTHON/"
pdfdir = "/home/kdog3682/PDFS/"
logdir = "/home/kdog3682/LOGS/"
oldtxtdir = "/home/kdog3682/TEXTS/"
txtdir = "/home/kdog3682/2023/TEXTS/"
jsondir = "/home/kdog3682/JSONS/"
emojifile = "/home/kdog3682/JSONS/emojis.json"
mathdir = "/home/kdog3682/MATH/"
picdir = "/home/kdog3682/PICS/"
colordir = "/home/kdog3682/COLORING/"
colordistdir = "/home/kdog3682/COLORING/dist/"
trashdir = "/home/kdog3682/TRASH/"
fontdir = "/home/kdog3682/CWF/public/fonts/"
jchdir = "/home/kdog3682/CWF/jch/"
pubdir = "/home/kdog3682/CWF/public/"
budir = "/mnt/chromeos/GoogleDrive/MyDrive/BACKUP/"
tempbudir = "/mnt/chromeos/GoogleDrive/MyDrive/BACKUP/TEMP/"

bucurdir = (
    "/mnt/chromeos/GoogleDrive/MyDrive/BACKUP/CURRENT/"
)

currentdir = dir2023

dirdict = {
    "root": rootdir,
    "math": mathdir,
    "home": rootdir,
    "js": jsdir,
    "html": jsdir,
    "py": pydir,
    "py": pythondir,
    "pdf": pdfdir,
    "txt": txtdir,
    "json": jsondir,
    "jpg": picdir,
    "jpeg": picdir,
    "png": picdir,
    "svg": picdir,
    "log": logdir,
    "dl": dldir,
    "dldir": dldir,
    "trash": trashdir,
    "fonts": fontdir,
    "dldir": dldir,
    "budir": budir,
    "current": dir2023,
    "dir2023": dir2023,
}

macdirdict = {
    "drive": "/users/harfunmaterials/Google Drive/",
    "outbound": "/users/harfunmaterials/Google Drive/OUTBOUND/",
}

olddirdict = {
    "bu": "/mnt/chromeos/GoogleDrive/MyDrive/BACKUP",
    "outbound": "/mnt/chromeos/GoogleDrive/MyDrive/OUTBOUND",
    "cwf": "/home/kdog3682/CWF",
    "root": "/home/kdog3682/",
    "jch": jchdir,
    "cwd": "/home/kdog3682/CWD",
    "pub": "/home/kdog3682/CWF/public",
    "root": "/home/kdog3682/",
    "a": "ASSETS",
    "drive": "/mnt/chromeos/GoogleDrive/MyDrive/",
    "drivecwf": "/mnt/chromeos/GoogleDrive/MyDrive/CWF",
    "0104": "/mnt/chromeos/GoogleDrive/MyDrive/CWF/01-04-2022",
    "dl": "/mnt/chromeos/MyFiles/Downloads/",
}

import regex as re
from pprint import pprint
from datetime import datetime, timedelta
import sys
import env
import json
import webbrowser
import shutil

emptyBlockRE = "^ *(?:function )?\\w+\\(.*?\\) {\\s*},?"
callableRE = "^[a-zA-Z.]+\\([^\\n`]+$"
callableRE = "^[a-zA-Z]\w*(?:.\w+)*\\([^\\n`]*"

blockQuoteRE = (
    "^ *(?:let |)?\\w+ =\\s*(?<!\\)`[^]+?(?<!\\)`.*\\n?"
)

cwfdir = "/home/kdog3682/CWF/"
cdir = "/home/kdog3682/CWF/"
drivecwfdir = "/mnt/chromeos/GoogleDrive/MyDrive/CWF/"

drivedir0104 = (
    "/mnt/chromeos/GoogleDrive/MyDrive/CWF/01-04-2022/"
)

BROWSER_AGENT = "Mozilla/5.0 (X11; CrOS aarch64 13310.93.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.133 Safari/537.36"

utfe = [
    "",
    "txt",
    "grammar",
    "drafts",
    "js",
    "py",
    "vim",
    "json",
    "css",
    "html",
    "math",
    "history",
    "ts",
    "vue",
    # "pdf",
]

imge = ["jpg", "jpeg", "png", "svg"]
fonte = ["ttf", "otf", "woff", "woff2"]
musice = ["m4a", "mp3", "mp4", "wav"]
macdir = "/users/harfunmaterials/"
drivedir = "/mnt/chromeos/GoogleDrive/MyDrive/"
original = print


def exists(x):
    t = type(x)
    if t == str:
        return x.strip() != ""
    if t == list:
        return len(x) > 0
    if t == dict:
        return len(x.keys()) > 0
    return x != None


def test(r, s, flags=0):
    if not isString(s):
        return
    return bool(re.search(r, s, flags))


def isPublicFile(x):
    if isIgnoredFile(x):
        return 0
    return test("^[a-zA-Z]|^\d+$", tail(x))


def isPrimitive(s):
    return isString(s) or isNumber(s)


def isFunction(x):
    return callable(x)


def isString(x):
    return type(x) == str


def isNumber(x):
    if isString(x):
        return test("^\d[.,\d]*$", x)
    return type(x) == int or type(x) == float


def isArray(x):
    return type(x) == list or type(x) == tuple


def isObject(x):
    return type(x) == dict


def head(f):
    return (
        re.sub("/$", "", str(f)).rsplit("/", maxsplit=1)[0]
        + "/"
    )


def tail(x):
    return re.sub("/$", "", str(x)).rsplit("/", maxsplit=1)[
        -1
    ]


def identity(s):
    return s


def getExtension(s):
    if "json.js" in s:
        return "json.js"
    return search("\.([a-zA-Z]+)$", s).lower()


def unique(a, b=None):
    if b:
        if isArray(a):
            return difference(a, b)
        if isObject(a):
            return filter(a, lambda k, v: k not in b)
    else:
        return list(set(a))


def difference(a, b):
    return list(set(a).difference(b))


def intersection(a, b):
    return list(set(a).intersection(b))


def toArray(x):
    if isArray(x):
        return x
    if isString(x):
        return split(x, "\n")
    return [x]


def every(items, fn):
    for item in list(items):
        if not fn(item):
            return False
    return True


def datestamp(x=None, strife="%m-%d-%Y"):
    if hasattr(x, "created_utc"):
        x = x.created_utc
        strife = "praw"
    elif isObject(x) and x.get("created_utc"):
        x = x["created_utc"]
        strife = "praw"

    ref = {
        "/": "%m/%d/%Y",
        "-": "%m-%d-%Y",
        "human": "%A %B %d, %-I:%M:%S%p",
        "praw": "%m-%d-%Y %-I:%M:%S%p",
    }
    strife = ref.get(strife, strife)
    if isString(x):
        if isfile(x):
            x = mdate(x)
            return datetime.fromtimestamp(x).strftime(
                strife
            )
        return datetime.strptime(x, strife)
    if type(x) == float or type(x) == int:
        return datetime.fromtimestamp(x).strftime(strife)
    if type(x) == datetime:
        return x.strftime(strife)

    return datetime.now().strftime(strife)


def getLast(s):
    return s[-1]


def search(regex, item, flags=0):
    match = re.search(regex, item, flags)
    if not match:
        return ""
    if match.groups():
        if len(match.groups()) == 1:
            return match.groups()[0]
        return match.groups()
    return match.group(0)


def toNumber(x):
    return int(x) if isNumber(x) else x


def isUrl(s):
    return test("^http|www|\.(?:com|net|io|org)\\b", s)


def clear(x):
    if isfile(x):
        with open(x, "w") as f:
            pass

    elif isdir(x):
        rmdir(x, None, True)


def absdir(dir="."):
    if isArray(dir):
        return dir
    dir = abspath(dir)
    return [os.path.join(dir, f) for f in os.listdir(dir)]


def getCaller(n=0):
    from inspect import stack

    stack = stack()
    if n == -1:
        return stack[2][3]
    else:
        return stack[len(stack) - 2][3]


def filter(items, f=exists, *args, **kwargs):
    if not f:
        return items
    if isString(f):
        r = f
        f = lambda s: test(r, s)
    if isObject(items):
        return {k: v for k, v in items.items() if f(k, v)}
    else:
        if isArray(f):
            ignore = f
            f = lambda x: x not in ignore

        return [
            x for x in list(items) if f(x, *args, **kwargs)
        ]


def isfile(f):
    return os.path.isfile(abspath(f))


def isdir(f):
    return isString(f) and os.path.isdir(f)
    return os.path.isdir(os.path.expanduser(f))


def toSeconds(
    minutes=0, hours=0, seconds=0, days=0, weeks=0, months=0
):
    return (
        seconds
        + minutes * 60
        + hours * 3600
        + days * 3600 * 24
        + months * 3600 * 24 * 30
    )


def isRecent(file, before=0, after=0, **kwargs):
    if isNumber(file):
        n = int(file)
    elif isfile(file):
        n = mdate(file)
    else:
        return False

    if before:
        return n < dategetter(before)
    if after:
        return n > dategetter(after)

    seconds = toSeconds(**kwargs)
    currentTime = timestamp()
    lastAcceptableTime = currentTime - seconds
    if n > lastAcceptableTime:
        return True


def timestamp(x=int):
    if type(x) == datetime:
        return int(x.timestamp())
    if x == int:
        return int(datetime.now().timestamp())


def mdate(f):
    return int(os.path.getmtime(f))


def mostRecent(dir, n=1, reverse=0, **kwargs):
    from glob import glob

    files = glob(dir + "/*") if isString(dir) else dir

    if kwargs:
        files = filter(files, checkpointf(**kwargs))

    files.sort(key=mdate)

    if not files:
        return None
    if n == 1:
        return files[-1]
    elif isNumber(n):
        return files[-n:]
    else:
        if reverse:
            return files[-n:][::-1]
        else:
            return files[-n:]


def npath(dir=0, file=0):
    if not dir:
        return file
    elif not file:
        return os.path.join(os.getcwd(), dir)
    return os.path.join(dir, tail(file))


def normpath(dir, file):
    dir = abspath(dir) if isdir(dir) else head(dir)
    return os.path.join(dir, tail(file))


def abspath(file=None):
    if file == None:
        return os.path.expanduser("~/")
    elif file == ".":
        return os.getcwd()
    elif file.startswith("~"):
        return os.path.expanduser(file)
    elif file.startswith("./"):
        return os.path.join(os.getcwd(), file[2:])
    else:
        return os.path.abspath(file)


google_url = "https://google.com/"


def ofile(f):
    if hasattr(f, "permalink"):
        return openBrowser("https://redd.it/" + f.id)
    return map(f, openBrowser)


def mfiles(files, dir, fn=0, ask=0):
    if isString(files):
        files = absdir(files)
    if not isdir(dir):
        dprompt("not a dir", dir, "press a key to make it")
        mkdir(dir)

    if ask:
        prompt(files, "move these files to", dir, "?")
    for f in files:
        if fn:
            dir = fn(dir + fn(tail(f)))
        mfile(f, dir)


def cfiles(files, dir, ask=0):
    if ask:
        prompt(
            files,
            tempbudir,
            "are you sure you want to copy these files and overwrite existing files in the directory?",
        )

    mkdir(dir)
    for f in files:
        cfile(f, dir)
    if ask:
        printdir(dir)


def cfile(f, t):
    mfile(f, t, mode="copy")


def mfile(f, t, mode="move"):
    assert isfile(f)
    if not getExtension(t) and not isdir(t):
        mkdir(t)
    elif not getExtension(t):
        t = normpath(t, f)

    if tail(f) == tail(t):
        print(mode, "file", tail(f), "to", head(t))
    else:
        print(f"{mode} file: {f} to {t}")

    if mode == "move":
        try:
            shutil.move(f, t)
            return 1
        except Exception as e:
            return 0
            pass

    elif mode == "copy":
        try:
            shutil.copy(f, t)
            return 1
        except Exception as e:
            return 0
            pass


def rfile(f):
    mfile(f, "/home/kdog3682/TRASH")


def cfile(f, t):
    if not getExtension(t):
        t = normpath(t, f)
    shutil.copy(f, t)
    print(f"copying file: {f} to {t}")


def cdir(dir, t):
    newDir = npath(t, dir)
    if isdir(newDir):
        if prompt("it is already a dir", newDir):
            return
    prompt(newDir)
    shutil.copytree(dir, newDir)
    print(f"copying directory: {newDir}")


def isMacbook():
    return not os.path.exists("/mnt")


def isCurrentDir(d):
    return abspath(os.getcwd()) == abspath(d)


def chdir(d, force=0):
    d = dirgetter(d)
    if not getExtension(d) and not isdir(d):
        if not force:
            prompt("mkdir?", d)
        mkdir(d)
    if isdir(d) and not isCurrentDir(d):
        print(f"changing to directory: {d}")
        os.chdir(d)


def prompt(*args, **kwargs):
    message = kwargs.pop("message")
    for arg in args:
        if arg:
            if isString(arg):
                print(arg)
            else:
                pprint(arg)
    if kwargs:
        pprint(kwargs)
    if message:
        print("message:", message)
    return input() or kwargs.get("fallback", "")


def isIgnoredFile(name):
    name = tail(name)
    ignore = [
        "vosk-api",
        "__pycache__",
        "node_modules",
        ".git",
    ]
    ignoreRE = "^(?:\W)"
    recursiveIgnoreRE = "^(?:LICNSE|README\.[mM][dD])$"
    return name in ignore or test(ignoreRE, name)


def fileInfo(f, r=0):
    if isfile(f):
        strife = "%A %B %d %Y, %-I:%M:%S%p"
        name = tail(f)
        date = datestamp(f, strife)
        size = fsize(f)
        return {
            "name": tail(f),
            "size": fsize(f),
            "date": date,
        }
    else:
        print(["not a file", f])


def dirgetter(dir=None):
    if not dir:
        return os.getcwd()
    return dirdict.get(dir, dir)
    return dirdict.get(dir, os.path.expanduser(dir))

    key = "macbook" if isMacbook() else "chromebook"
    dicts = {"macbook": macdirdict, "chromebook": dirdict}
    dict = dicts[key]

    dir = dict.get(dir, dir)
    assert isdir(dir)
    return dir


def number(items):
    for i, item in enumerate(items):
        print(i + 1, item)


def askToRemove(file):
    pprint(read(file))
    print(file)
    a = input()
    if a:
        rfile(file)


def fixBrowserPath(f):
    if not f:
        return
    if isfile(f):
        return f
        prompt(f)
    aliases = {
        "red": "reddit",
    }
    if f in aliases:
        return fixUrl(aliases[f])
    ref = {
        "json": [dldir, jsondir],
        "pdf": [dldir, pdfdir],
    }
    e = getExtension(f)

    if e:
        for dir in ref.get(e, []):
            temp = npath(dir, f)
            if isfile(temp):
                return temp
            raise Exception("cant find the file")

    if isUrl(f):
        return f

    return f"https://google.com/search?q={f}"


def openBrowser(f):
    if not f:
        return
    f = fixBrowserPath(f)
    print(f"opening file: {f}")
    webbrowser.open(f)


def choose(x, mode=0, filter=0, auto=1):
    if isString(x) and isdir(x):
        x = absdir(x)
    else:
        x = list(x)
    if not isPrimitive(x[0]):
        mode = 1
    if auto and len(x) == 1:
        return x[0]

    if isString(x[0]) and isfile(x[0]):
        x = map(x, tail)
    a = prompt2(x)
    if not a:
        return
    if filter:
        while isWord(a):
            newList = [
                el
                for el in x
                if test(a, filter(el), flags=re.I)
            ]
            if newList:
                x = newList

            a = prompt2(x)

    if a == "x":
        return []

    value = None
    if not a:
        return x
    else:
        value = [
            x[int(n) - 1] for n in a.strip().split(" ")
        ]

    if value:
        if mode == 1:
            return value[0]
        if mode == 0:
            return unique(value)


def find(arr, fn, mode=None, flags=0):
    if isObject(arr):
        for k, v in arr.items():
            if fn in v:
                return os.path.join(k, fn)
        return

    for i, item in enumerate(list(arr)):
        if ftest(fn, item, flags=flags):
            return i if mode == int else item


def createKwargs(s):
    if not s:
        return {}

    dict = {
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
        "this": "date=today",
        "tf": "testfunction",
        "mv": "move",
        "of": "onlyFiles=1",
        "h": "html",
        "i": "mode=info",
        "s": "mode=save",
        "big": "big=100000",
    }
    s, quote = mreplace('"(.*?)"', s)
    s = dreplace(s, dict, template="(?<![\w=])(?:$1)\\b")
    regex = "(\S+?) *= *(\S+?)(?= |$)"
    s, items = mreplace(regex, s)
    f = lambda x: int(x) if isNumber(x) else x

    items1 = {k: f(v) for k, v in items}
    items2 = {a: 1 for a in split(s, " ")}
    items1.update(items2)
    if quote:
        items1["text"] = quote[0]
    return items1


def configurable(fn):
    def wrapper(s="", **bargs):
        if s:
            s += " of"
        kwargs = createKwargs(s)
        kwargs.update(bargs)
        return fn(**kwargs)

    return wrapper


def sort(x, f=int, reverse=0):
    if isObject(x):
        return {
            k: v
            for k, v in sorted(
                x.items(),
                key=lambda item: f(item[1]),
                reverse=reverse,
            )
        }
    else:
        return sorted(list(x), key=f, reverse=reverse)


def append(f, s):
    if f.endswith(".json"):
        return appendjson(f, s)
    if isObject(s):
        s = s.values()

    value = toString(s)

    if value:
        with open(f, "a") as _:
            _.write("\n" + value)
            print(f"appending file: {f}")


def fixUrl(s):
    s = re.sub("(?:https://)?view-source:", "", s)
    if "." not in s:
        s += ".com"
    if not test("^http", s):
        s = "https://" + s
    return s


def getDomainName(url):
    return re.sub("(?<!/)/\w.*$", "", fixUrl(url))


def downloadWebsite(url):
    chdir(pubdir)
    downloader = lambda x: write(
        tail(x), request(x), open=1
    )
    domainName = getDomainName(url)

    s = request(url)

    def runner(x):
        m = x.group(1)
        if m.startswith("/"):
            m = os.path.join(domainName, m[1:])

        # print(m)
        # downloader(m)
        return quote(tail(m))

    regex = "['\"]" + "(\S+\.(?:js|css))" + "['\"]"
    s = re.sub(regex, runner, s)
    write("index.html", s, open=1)


def toNumber(x):
    if isNumber(x):
        return int(x)
    return x


def toString(x):
    return str(x) if isPrimitive(x) else join(x)


def gatherArgs(args):
    if isArray(args[0]):
        return args[0]
    return args


def join(*args, delimiter="\n"):
    if not args:
        return ""

    if not args[0]:
        return ""

    s = ""
    for item in gatherArgs(args):
        if isArray(item):
            item = join(item)
        s += item
        s += "\n\n" if "\n" in item else delimiter

    return backspace(s) if delimiter else s


def moveClipToLogJson(key):
    value = clip()
    logger(key=key, value=value)


def logger(**kwargs):
    if not kwargs:
        return

    from collections import OrderedDict

    store = OrderedDict()
    store["action"] = getCaller()
    store["date"] = datestamp()
    entries = sort(
        kwargs.items(), lambda x: len(json.dumps(x))
    )
    for a, b in entries:
        store[a] = b

    appendjson(glogfile, store, mode=list)


def backup(f):
    if isArray(f):
        assert every(f, isfile)
        dirName = budir + prompt(
            "Creating new Directory: Name for the back-up directory (it will be located in drive/budir)?"
        )
        cfiles(f, dirName)
        logger(action="backup", dirName=dirName, files=f)
    elif isfile(f):
        shutil.copy(f, npath(budir, f + ".backup"))
    elif isdir(f):
        return print("no dirs yet")

    print("backed up", f)


def backspace(s):
    return s[:-1]


def camelCase(s):
    s = uncapitalize(s.strip())
    s = re.sub("[- .](\w)", lambda x: x.group(1).upper(), s)
    return s


def decode(x):
    return x.decode("utf-8")


def node(*args):
    return system("node", *args)


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


def quote(s):
    return (
        '"""\n' + s.strip() + '\n"""'
        if "\n" in s
        else '"' + s + '"'
    )


def some(items, x):
    for item in items:
        if ftest(x, item):
            return True


def addExtension(s, extension="py", force=0):
    if not s:
        return ""
    return (
        s
        if getExtension(s) and force == 0
        else s + "." + extension
    )


def ftest(f, arg, flags=0):
    if isArray(f):
        return every(f, lambda f: ftest(f, arg))
    if isString(f):
        return test(f, arg, flags=flags)
    if isFunction(f):
        return f(arg)
    return True


def handleError(e):
    print([getCaller(), "error", str(e)])


def rigidSort(items, order, f=identity):
    order = {k: i for k in order}
    items.sort(key=lambda x: order[f(x)])
    return items


def breaker(n=10):
    global a
    a += 1
    if a >= n:
        raise Exception()


def _setup_chromebook():
    os.system("clear")
    print("Install Pip Libraries")


def _cleanup_base():
    # cleanup base.py
    # uses globals() to organize everything

    from inspect import getsource

    lib = globals()
    preset = {"pprint": "from pprint import pprint"}

    f = testf("^__", 0, 1)
    keys = filter(list(lib.keys()), f).sort()
    keys.sort()

    def f(key):
        v = lib.get(key)
        t = type(v)
        if t == str:
            s = f"{key} = '{str(v)}'"
            name = "primitives"
        elif t == int or t == float:
            s = f"{key} = {str(v)}"
            name = "primitives"
        elif t == module:
            s = str(v)
            name = search("<module '([\w-]+)'", s)
            if name == key:
                s = f"import {name}"
            else:
                s = f"import {key} as {name}"
            name = "modules"

        elif key in preset:
            name = "modules"
            s = preset[key]
        else:
            s = getsource(v)

        if name:
            pass
        elif test("^_", s):
            name = "apps"
        elif t == type:
            name = "classes"
        elif t == function:
            name = "functions"

        storage.add(name, s)

    storage = Storage()
    map(keys, f)
    items = storage.store.items()
    order = [
        "modules",
        "primitives",
        "functions",
        "classes",
        "apps",
    ]
    rigidSort(items, order, lambda x: x[0])
    s = ""
    for k, v in items:
        v.sort()
        s += join(v)
        s += "\n\n"
    return s
    breaker(3)


def testf(r, flags=0, reverse=0):
    if reverse:
        return lambda x: not test(r, x, flags)
    else:
        return lambda x: test(r, x, flags)


def rmdir(dir, force=0, create=0):
    if (
        len(os.listdir(dir)) < 10
        and absdir(dir) not in dirdict.values()
    ):
        shutil.rmtree(dir)
        print("removing dir", dir)

    elif (
        len(os.listdir(dir)) == 0
        or force
        or prompt("rmdir for sure?")
    ):
        shutil.rmtree(dir)
        print("removing dir", dir)

    if create:
        mkdir(dir)


quoteRE = "(?<!\\)'.*?(?<!\\)'|(?<!\\)\".*?(?<!\\)\""


def mkdir(dir):
    if isdir(dir):
        print("dir alrady exists. early return")
        return dir
    elif getExtension(dir):
        raise Exception("dir has an extension...")
    else:
        os.makedirs(dir)
        print(f"creating new directory: {dir}")
        return dir
        return True


def write(f, s, open=0):
    try:
        _write(f, s, open)
    except Exception as e:
        print(e)
        return
        dir = head(f)
        mkdir(dir)
        _write(f, s, open)


def _write(f, s, _open=0):
    if not exists(s):
        return
    e = getExtension(f)

    if e == "json.js":
        name = camelCase(removeExtension(tail(f)))
        value = createVariable(name, stringify(s), "js")
        with open(f, "w") as _f:
            _f.write(value)
        # log(file = f)

    elif e == "recent":
        with open(f, "w") as _f:
            if isString(s):
                _f.write(s)
            else:
                json.dump(s, _f, indent=2)

    elif e == "json":
        with open(f, "w") as _f:
            json.dump(s, _f, indent=2)
    else:
        with open(f, "w") as _f:
            _f.write(toString(s))

    print(f"writing file: {f}")
    if _open:
        ofile(f)


def uncapitalize(s):
    return re.sub(
        "[a-zA-Z]", lambda x: x.group(0).lower(), s, count=1
    )


def lineCount(s):
    return len(re.findall("\n", s))


def stringify(x):
    if type(x) == bytes:
        return x.decode()
    if isPrimitive(x):
        return str(x)
    return json.dumps(x, indent=4)


def removeComments(s, e=None):
    raise Exception()
    js = "(?://|/\*[\w\W]+?\*/)"
    html = "<!--[\w\W]*?-->"
    start = "^ *"
    end = ".*\n+"

    if not e:
        if test(html, s):
            e = "html"

        elif test(js, s):
            e = "js"

    r = start + locals().get(e, "js") + end
    return re.sub(r, "", s, flags=re.M)


def removeExtension(s):
    return re.sub("(?:\.json)?\.\w+$", "", s)


def createVariable(name, s, lang="py"):
    if test("^(fun|def|class)", s):
        return s
    prefix = "var " if lang == "js" else ""
    if not name:
        name = "PLACE_HOLDER"
    if isString(s) and not isJsonParsable(s):
        s = quote(s)
    s = stringify(s)
    return prefix + name + " = " + s


def unidecode(s):
    from unidecode import unidecode

    return unidecode(s)


def wrap(a, b="()"):
    dict = {
        "()": ["(", ")"],
        "[]": ["[", "]"],
        "{}": ["{", "}"],
    }
    a, c = dict.get(b, [b, b])
    return f"{b}{a}{c}"


def templater(template, ref):

    if isString(ref):
        ref = [ref]
    regex = "\$(\w+)"

    def parser(x):
        if isArray(ref):
            return ref[int(x) - 1]

        if isObject(ref):
            return ref.get(x)

        if isFunction(ref):
            return ref(x)

    def runner(x):
        return parser(x.group(1))

    return re.sub(regex, runner, template)


def map(items, fn, *args, filter=1, **kwargs):
    if not items:
        return []
    if isString(fn):
        _key = fn
        if isObject(items[0]):
            fn = lambda x: x.get(_key)
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
    for item in toArray(items):
        try:
            value = fn(item, *args, **kwargs)
            if not (filter and not value):
                store.append(value)
        except Exception as e:
            prompt(item, error="ERROR AT MAP", message=e)
            continue
    return store


def raw(f):
    with open(f, "rb") as f:
        return str(f.read())


def read(file):
    e = getExtension(file)
    mode = "rb" if e in imge else "r"
    try:
        with open(file, mode) as f:
            return json.load(f) if e == "json" else f.read()
    except Exception as error:
        return None


def snakeCase(s):
    return re.sub(
        "([a-z])([A-Z])",
        lambda x: x.group(1) + "-" + x.group(2).lower(),
        s,
    )


def pop(x, key):
    if isNumber(key):
        return x.pop(key)
    elif isArray(x):
        return x.pop(x.index(key))
    else:
        return x.pop(key, None)


def parseJSON(x):
    if isString(x):
        x = x.strip()
    try:
        return json.loads(x) if isJsonParsable(x) else x
    except Exception as e:
        prompt(text=x)


def isJsonParsable(x):
    return isString(x) and test("^[{\[]", x)


def request(url, delay=0):
    from requests import get

    if delay:
        import time

        time.sleep(delay)

    r = get(fixUrl(url), {"user-agent": BROWSER_AGENT})
    return parseJSON(r.text) if r.status_code == 200 else ""


def stringcall(fn, args):
    f = lambda x: int(x) if isNumber(x) else quote(x)
    return fn + "(" + ", ".join(map(args, f)) + ")"


def clip(s=0, name=0):
    presetClipFiles = ["reddit", "booga"]
    if s == 2:
        return parseJSON(read(jsdir + "clip2.js"))
    if s in presetClipFiles:
        return read(clipdir + s + ".json")

    n = None
    if isNumber(s):
        n = s
        s = None

    if not s:
        data = parseJSON(normRead(clipfile))
        if isArray(data) and n:
            return data[0:n]
        return data
    if isString(s) and isdir(s):
        s = os.listdir(s)
    if s:
        write(name or clipfile, stringify(s), open=1)


def googleYouTubeVideosFromUrl():
    url = "https://www.youtube.com/watch?v=qNgZxjJBey4&ab_channel=Mario%27sMathTutoring"
    url = re.sub(
        "watch\?.+?channel=(.*?)",
        lambda x: "c/" + x.group(1),
        url,
    )
    url = re.sub("%\d+", "", url)
    data = request(url)
    id = search('externalId.*?(\w.*?)"', data)
    clip(id)


def mergefiles(s):
    return join(map(s, read))


def split(s, r=" ", flags=0):
    if r == "linebreak":
        flags = re.M
        r = "^----+"

    return map(
        filter(re.split(r, s.strip(), flags=flags)), trim
    )


def trim(s):
    return s.strip()


def splitonce(s, r=" "):
    if isArray(s):
        return [s[0], s[1:]]
    return force(re.split(r, s, maxsplit=1))


def force(arr, n=2):
    while len(arr) < n:
        arr.append("")
    return arr


def fsize(f):
    return os.path.getsize(f)


def isRemovableFile(file):
    removeRE = "\\bboo\\b|debug|dela|foo|\(|^-?\d+$"
    removeList = ["log", "aux", "mhtml", "tex", "zip"]
    e = getExtension(file)
    size = fsize(file)

    return (
        (e and size < 100)
        or test(removeRE, tail(file))
        or e in removeList
        or e == "js"
        and size < 100
        or size == 0
        or (e == "json" and size < 1000)
    )


def getArgsKwargs(s):
    r = "(\w+) *= *(\S+?)(?= |$)"
    s, kwargs = mreplace(r, s)
    args = split(s, " ")
    return args, {k: v for k, v in kwargs}


def dategetter(s, mode=int):
    today = datetime.today()
    year = today.year
    day = 1
    value = 0

    if s == True:
        value = today.replace(minute=today.minute - 10)
    elif test("^\d", s):
        a, b, c = search(
            "(\d+):?(\d*) *([ap]m)?", s, flags=re.I
        )
        print(a, b, c)
        offset = 0 if test("am", s, flags=re.I) else 12
        hour = int(a) + offset
        minute = int(b)
        # date = datetime()
        day = (
            today.day - 1
            if today.hour < hour
            else today.day
        )
        value = today.replace(
            day=day, hour=hour, minute=minute, second=0
        )
        # strife = "%A %B %d, %-I:%M:%S%p"
        # print(datestamp(value, strife))
        # return
    elif s == "yesterday":
        value = today.replace(day=today.day - 1)
    elif s == "today":
        value = today
    elif s == "month":
        value = today.replace(day=1)

    return int(value.timestamp()) if mode == int else value


def isSameDate(date, f):

    fdate = datetime.fromtimestamp(mdate(f))
    date = dategetter(date, None)
    return date.day == fdate.day


def checkpointf(
    contains=0,
    deleteIt=0,
    include="",
    size=0,
    maxLength=0,
    image=0,
    today=0,
    flags=re.I,
    files=0,
    gif=0,
    weeks=0,
    month=0,
    old=0,
    ignore="",
    ignoreRE="",
    css=0,
    js=0,
    py=0,
    txt=0,
    html=0,
    pdf=0,
    date=0,
    name=0,
    big=0,
    r=0,
    antiregex=0,
    small=0,
    before=0,
    after=0,
    minLength=0,
    minutes=0,
    days=0,
    hours=0,
    regex=0,
    public=0,
    math=0,
    text=0,
    lib=0,
    log=0,
    onlyFiles=0,
    isf=0,
    isp=0,
    onlyFolders=0,
    biggerThan=0,
    smallerThan=0,
    fn=0,
    e=0,
    json=0,
    **kwargs,
):
    if size:
        biggerThan = size
    if text:
        onlyFiles = 1
    if isf:
        onlyFiles = 1
    if r:
        name = r
    extensions = kwargs.get("extensions", [])
    if kwargs.get("isdir"):
        onlyFolders = 1
    if log:
        extensions.append("log")
    if math:
        extensions.append("math")
    if css:
        extensions.append("css")
    if js:
        extensions.append("js")
    if json:
        extensions.append("json")
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
    if image:
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

    def runner(f):
        filename = tail(f)

        if fn and not fn(f):
            return False

        if include and filename in include:
            return True
        if ignore and filename in ignore:
            return False
        if isp and filename.startswith("."):
            return False
        if deleteIt and alwaysDelete(f):
            rfile(f)
            return False
        if regex and not test(regex, filename, flags=flags):
            return False
        if antiregex and test(
            antiregex, filename, flags=flags
        ):
            return False

        if name and not test(name, filename, flags=flags):
            return False

        e = getExtension(filename)

        if text and e == "pdf":
            return False

        if extensions and e not in extensions:
            return False

        if hours and not isRecent(f, hours=hours):
            return False

        if not lib and isLibraryFile(f):
            return False

        if public and not isPublicFile(f):
            return False

        if onlyFiles and isdir(f):
            return False

        if contains:
            if not isdir(f):
                return True
            gn = lambda x: getExtension(x) == contains
            files = filter(os.listdir(f), gn)
            if len(files) < 5:
                print(
                    f,
                    "has some files but not enuf of ",
                    contains,
                )
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
        if small and fsize(f) > small:
            return False
        if big and fsize(f) < big:
            return False
        if ignoreRE and test(
            ignoreRE, filename, flags=re.I
        ):
            return False
        if text and not test(text, read(f), flags=flags):
            return False
        if date and not isSameDate(date, f):
            return False
        return True

    return trycatch(runner)


def trycatch(fn):
    def runner(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            print("hiiiiiiiiiii", str(e), *args)
            raise Exception()
            return

    return runner


def mreplace(r, s, **kwargs):
    store = []

    def runner(x):
        if x.groups():
            store.append(
                x.group(1)
                if len(x.groups()) == 1
                else x.groups()
            )
        else:
            store.append(x.group(0))

        return ""

    text = re.sub(r, runner, s, **kwargs).strip()
    return text.strip(), store


def flat(items, depth=None):
    def runner(items, limit=0):
        for item in items:
            if isArray(item) and (
                not depth or limit < depth
            ):
                runner(item, limit + 1)
            else:
                store.append(item)

    store = []
    runner(items)
    return store


def changeExtension(s, e, unique=False):
    # if isArray(s):
    # return map(s, lambda x: changeExtension(x, e, unique))

    def incrementName(s):
        count = 1
        while isfile(s):
            count += 1
            s = re.sub("(?=\.)", str(count), s)
        return s

    name = re.sub("(?:\.\w+)?$", "." + e, s, count=1)
    if unique:
        name = incrementName(name)
    return name


def capitalize(s):
    return s[0].upper() + s[1:]


def getfiles(dir, recursive=0, mode=dict, sort=0, **kwargs):

    if recursive and not mode == list:
        mode = dict

    checkpoint = checkpointf(**kwargs)

    def runner(dir):
        store = []
        files = absdir(dir)
        for file in files:
            name = tail(file)

            if isIgnoredFile(name):
                continue

            elif isfile(file):
                if checkpoint(file):
                    if mode == dict:
                        store.append(name)
                    else:
                        output.append(file)
            elif isdir(file) and recursive:
                runner(file)

        if mode == dict:
            if sort:
                store = map(
                    store, lambda x: os.path.join(dir, x)
                )
                if sort == datestamp:
                    store = {
                        tail(f): datestamp(f)
                        for f in sorted(store, key=mdate)
                    }
                else:
                    store.sort()
            output[dir] = store

    output = {} if mode == dict else []
    runner(dirgetter(dir))
    return output


def printdir(dir=dldir, printIt=0):
    dir = dirgetter(dir)
    files = os.listdir(dir)
    size = len(files)
    if size < 30:
        files = map(files, lambda f: normpath(dir, f))
        pprint(map(files, fileInfo))
    else:
        pprint(sorted(files))

    dprint(size, dir)
    if printIt:
        clip(files)
    return files


NCG_TEMPLATE_LIBRARY = {
    "b": "\\b(?:$1)\\b",
}


def reWrap(dict, template=""):
    ref = {
        "": "(?:$1)",
        "b": "\\b(?:$1)\\b",
    }
    template = ref.get(template, template)
    keys = list(dict.keys() if isObject(dict) else dict)
    symbols = map(keys, re.escape)
    s = "|".join(symbols)
    return re.sub("\$1", s, template)


def ncg(template, ref):
    if not template:
        template = "(?:$1)"
    if NCG_TEMPLATE_LIBRARY.get(template):
        template = NCG_TEMPLATE_LIBRARY.get(template)
    s = "|".join(list(ref.keys()))
    r = template.replace("$1", s)
    return r


def dreplace(s, dict, flags=0, template=""):

    regex = reWrap(dict, template)

    def parser(x):
        value = (
            dict.get(x.group(1))
            if x.groups()
            else dict.get(x.group(0))
        )
        if None == value:
            prompt(dreplace_error=x)
        return value

    return re.sub(regex, parser, s, flags=flags)


def execute(s):
    if isfile(s):
        e = getExtension(s)
        if e == "py" and not tail(s) == "base.py":
            print(f"executing file: file{s}")
            s = read(s)
        else:
            return

    try:
        if test("\n|^\w+ \w+", s.strip()):
            return exec(s)
        else:
            return eval(s)
    except Exception as e:
        handleError(e)


def toKwargs():
    ref = {
        "ds": "doubleSided",
        "c": "copies",
        "ls": "landscape",
    }
    f = lambda x: ref.get(x)
    # s = "ds c ls"
    s = input("input  ")
    args = {k: 1 for k in map(split(s), f)}
    return args


def partitionByFunction(arr, f):
    store = [[], []]
    for item in arr:
        if f(item):
            store[0].append(item)
        else:
            store[1].append(item)
    return store


def partition(arr, n=2):
    if isString(n):
        n = testf(n)
    if isFunction(n):
        return partitionByFunction(arr, n)

    store = []
    for i in range(0, len(arr), n):
        store.append(arr[i : i + n])
    return store


class Partitioner:
    def run(self):
        while len(self) > 0:
            done = self.partition()
            if done:
                break

    def __len__(self):
        return len(self.keys)

    def toJSON(self):
        return self.inputs

    def __init__(self, items, dest=0):
        self.defaultDest = dest
        self.inputs = {}
        if isArray(items):
            self.keys = items
        elif isObject(items):
            self.items = items
            self.keys = list(self.items.keys())

        self.storage = Storage()
        self.run()

    def partition(self):
        number(self.keys)
        pprint(self.storage.store)
        a, b = splitonce(
            input("write s and destination\n\n")
        )
        if not a and not b:
            return 1
        elif b:
            destination = a
            self.lastDestination = destination
            s = b
        elif hasattr(self, "lastDestination"):
            destination = self.lastDestination
            s = a
        elif self.defaultDest:
            destination = self.defaultDest
            s = a
        else:
            destination = prompt("write a destination")
            s = a

        self.inputs[destination] = s
        store = []
        items = unique(split(s))

        for item in items:
            if "-" in item:
                a, b = item.split("-")
                for item in range(int(a), int(b) + 1):
                    value = self.keys[int(item) - 1]
                    store.append(value)

            elif isNumber(item):
                value = self.keys[int(item) - 1]
                store.append(value)

            else:
                values = filter(
                    self.keys, testf(item, re.I)
                )
                store.extend(values)

        for key in store:
            pop(self.keys, key)
            self.storage.add(destination, key)


class Storage:
    def toJSON(self):
        return self.store

    def __repr__(self):
        return stringify(self.store)

    def __init__(self):
        self.store = {}

    def add(self, k, v):
        if not v:
            print("return")
            return
        if k in self.store:
            self.store[k].append(v)
        else:
            self.store[k] = [v]


def includef(items):
    return lambda x: x not in items


def edit(o, fn):
    if isObject(o):
        store = {}
        for k, v in o.items():
            value = fn(k, v)
            if value == None:
                value = v
            store[k] = value
        return store

    if isArray(o):
        for i, item in enumerate(o):
            o[i] = fn(o[i]) or item
        return o


def self():
    return sys.argv[0]


def isWord(s):
    return test("^[a-zA-Z]+$", s)


def inferlang(s):
    if isString(s) and len(s) <= 4 and isWord(s):
        return s
    if s in utfe:
        return s
    if getExtension(s):
        return getExtension(s)
    match = search(
        "^(?:\{|\[]\$|mkdir|touch|cd|npm|touch|function|def|<|\.|let|var|const)",
        s,
        flags=re.M,
    )
    ref = {
        "[": "json",
        "{": "json",
        "touch": "npm",
        "mkdir": "npm",
        "cd": "npm",
        "$": "npm",
        "touch": "npm",
        "nano": "npm",
        "var": "js",
        "let": "js",
        "function": "js",
        "const": "js",
        "def": "py",
        "<": "html",
        ".": "css",
    }
    return ref.get(match)


def jspy(lang, key):
    lang = inferlang(lang)

    namePY = "^(?:\w+(?= )|(?<=def |class )\w+)"
    nameJS = (
        "^(?:(?:async )?function|def|class|const) ([\w\$]+)"
    )
    callablePY = "\w\w\w+\.(?!log|toString)[a-z]\w+(?=\()"
    callablePY = "[\w\.]{8,}(?=\()"
    callableJS = (
        "new \w+|\w\w\w+\.(?!log|toString)[a-z]\w+(?=\()"
    )
    # variableJS = '(?:const )?\w+ = (?:.+?[^\[\{](?=\n)|[\w\W]+?\n[\]\}])'
    variableJS = "^(?:const )?\w+ = \w.+"
    cleanupJS = "^(?:const )?\w+ = \w.+"
    cleanupJS = "^\w+(?:\.\w+)*\(.+"
    cleanupPY = "^(?:const )?\w+ = \w.+|^(?:new \w+|\w\w\w+\.(?!log|toString)[a-z]\w+\().+"
    variablePY = "\w+ = (?:.+[^\[\{]|[\w\W]+?\n[\]\}]"
    commentJS = "// "
    commentPY = "# "
    functionJS = "(?:(?<=\n)|^)(?:(?:async )?function|class) \w+\\b[\w\W]+?\n}(?=\n|$)"
    functionJS = "(?:(?<=\n)|^)(?:const [\w\$]+ = [\[\{][\w\W]+?\n[\]\}]|(?:(?:async )?function|class) [\w\$]+\\b[\w\W]+?\n})(?=\n|$)"
    functionPY = (
        "^(?:@.+\n)*(?:def|class) \w+\\b[\w\W]+?(?=\n\S)"
    )

    functionBodyJS = (
        "^(?:(?:async )?function|class) [\w\W]+\n}"
    )
    functionBodyPY = "^(?:def|class) [\w\W]+(?=\n\S+)"

    codeJS = "(?:(?<=\n)|^)(?:(?:(?:async )?function|class) \w+\\b|const \w+ *= *[\[\{])[\w\W]+?\n[\]\}]"
    codePY = "^(?:def|class) [\w\W]+(?=\n\S+)"
    linebreakJS = (
        "/* ------------------------------------- */"
    )
    linebreakPY = "# -------------------------------------"

    indexes = ["js", "py", "vim", "bash", "css", "html"]

    ref = {
        "compiler": ["node", "python3", None, "bash"],
        "runtime": ["node", "python3", None, "bash"],
        "const": ["const ", "", "let"],
        "callableRE": [callableJS, callablePY],
        "nameRE": [nameJS, namePY],
        "functionRE": [functionJS, functionPY],
        "functionBodyRE": [functionBodyJS, functionBodyPY],
        "commentRE": [commentJS, commentPY],
        "superComment": ["//// ", "#### "],
        "//": ["//", "#"],
        "variableRE": [variableJS, variablePY],
        "cleanupRE": [cleanupJS, cleanupPY],
        "codeRE": [codeJS, codePY],
        "linebreak": [linebreakJS, linebreakPY],
        "comment": [commentJS, commentPY],
    }

    value = ref[key][indexes.index(lang)]
    return value


def prepend(file, content):
    write(file, content + "\n\n" + read(file))


def getFunctionName(s):
    rA = "^(?:@.+\n)*(?:(?:async )?function|def|class|const|var|let) ([\w\$]+)"
    rB = "^([\w\$]+) ="
    return search(rA, s) or search(rB, s)


def getFunctionNames(s):
    r = "^(?:(?:async )?function|class|def) ([\w\$]+)"
    return unique(re.findall(r, get_text(s), flags=re.M))


def get_text(x):
    if len(x) > 100:
        return x
    if isUrl(x):
        return request(x)
    if isfile(normDirPath(x)):
        return normRead(x)
    return x


def functiongetter(x, lang=None):
    regex = jspy(lang or x, "functionRE")
    matches = re.findall(regex, get_text(x))
    return {getFunctionName(item): item for item in matches}


def isLibraryFile(f):
    name = tail(f)
    return name in env.js_libraries or ".min" in name


def normalize_fn_parameters(fn, item):
    p = count_function_params(fn)
    if p == 1 and (isObject(item) or isNestedArray(item)):
        return lambda k, v: fn(v)
    return fn


def reduce(items, fn):
    store = {}

    fn = normalize_fn_parameters(fn, items)
    if isObject(items):
        for k, v in items.items():
            value = fn(k, v)
            if value != None:
                store[k] = value
    else:
        for item in list(items):
            value = fn(item)

            if value != None:
                store[item] = value

    return store


def hasLookAround(s):
    return test("\(\?\<", s)


def btest(r, s):
    return test("\\b" + r + "\\b", s, flags=re.I)


def curpath():
    print(abspath(os.getcwd()))


def filegetter(s):
    if s.endswith("files.txt"):
        try:
            data = read(s)
            files = split(data, "\n+")
            number(files)
            return files
        except Exception as e:
            return []


class RequestLimiter:
    def __init__(self, limit=10, sleep=60, maximum=100_000):
        self.count = 0
        self.cycles = 0
        self.maximum = maximum
        self.limit = limit
        self.sleep = sleep
        import time

    def get(self, *args, **kwargs):
        if self.count > self.maximum:
            return

        if self.count == self.limit:
            self.count = 0
            self.cycles += 1
            time.sleep(self.sleep)
            print(self.cycles, "cycles")
        else:
            self.count += 1

        return request(*args, **kwargs)


def srequest(url):
    if isRecent("request.temp.txt", minutes=20):
        print("returning recent file")
        return read("request.temp.txt")

    s = request(url)
    write("request.temp.txt", s, open=1)
    return s


def finder(url, term):
    s = srequest(url)
    templates = [
        "(?:b)>$1</(?:b)",
        "(?:name|value) *= *[\"']$1[\"']",
    ]

    for template in templates:
        r1 = templater(template, term)
        a1 = search(r1, s)
        if a1:
            r = r1.replace(term, "([\w-.]+)")
            m = rf(r, s)
            write("found.json", m, open=1)
            return m


def hasNewline(s):
    return "\n" in s


def regexjoin(*args):
    return "|".join(list(args))


def findall(r, text):
    def parser(s):
        if isArray(s):
            s = smallify(filter(s))
        return s

    m = re.findall(r, text)
    return [parser(x) for x in m]


def smallify(items):
    return items[0] if len(items) == 1 else items


RegexLib = {
    "caps": "[A-Z_]{3,}+\d*",
}


def getPureHtml(s):
    import bs4

    return bs4.BeautifulSoup(s, "html.parser").get_text()


def regexdiv(
    tag, attrs=0, content="[\w\W]+?", after="", before=""
):
    content = parens(content)
    attrs = " " + attrs + ".*?" if attrs else "[\w\W]*?"
    return f"<{tag}{attrs}>{before}{content}{after}</{tag}>"


def parens(s):
    return f"({s})"


def shellescape(s):
    dict = reverse(env.shellescapedict)
    regex = reWrap(dict)

    def parser(x):
        value = (
            dict.get(x.group(1))
            if x.groups()
            else dict.get(x.group(0))
        )
        if not value:
            prompt(x=x, error="shellescape")
        return "zz" + value

    return re.sub(regex, parser, s)


def shellunescape(s):
    if not isString(s):
        return s
    if "zz" not in s:
        return s
    s = dreplace(s, shellescapedict, template="zz($1)")
    return parseJSON(s)


def isMovie(s):
    return s.endswith("MOV")


def partitionByDate(files):
    files = sort(files, mdate, reverse=1)
    lastDate = timestamp()
    for file in files:
        date = mdate(file)


def toRoot(s):
    return rootdir + tail(s)


def itest(r, s):
    return test(r, s, flags=re.I)


def newlineIndent(x):
    s = join(x)
    return "\n" + re.sub("^", "    ", s, flags=re.M) + "\n"


def toCallable(f, *args):
    if not f:
        return ""
    if test("^\w+\(", f):
        return f
    payload = ", ".join(map(filter(args), toStringArgument))
    return f + parens(payload)


def toStringArgument(s):
    if isString(s):
        return quote(s)
    return json.dumps(s)


def dumpJson(payload):
    if isString(payload):
        return payload
    return json.dumps(payload)


def mimeTypeFromFile(file):
    return env.mimetypes[getExtension(file)]


def upcomingDate(day, mode=0, strife="/", next=0):
    day = capitalize(day)
    today = datetime.now()

    def increment():
        nonlocal today
        today = today + timedelta(days=1)

    while 1:
        weekday = env.weekdays[today.weekday()]
        if weekday == day:
            if next:
                today = today + timedelta(weeks=next)
            if mode == list:
                return [today.month, today.day, today.year]
            if mode == datetime:
                return today
            return datestamp(today, strife=strife)
        else:
            increment()


def dirFromFile(f):
    if f.startswith("/"):
        return head(f)
    e = getExtension(f)
    if e == "py":
        return pydir
    return dir2023
    # return dirdict.get(e, pubdir)


def dirFromFile2(f):
    e = getExtension(f)
    if e == "py":
        return pydir
    return dir2023


def removeDateStamp(s):
    datestampRE = "\d+[-/]\d+[-/]\d+"
    return re.sub("-?" + datestampRE, "", s)


def isRecentFile(f, days=1, **kwargs):
    return isfile(f) and isRecent(f, days=days, **kwargs)


def changeFileName(file, newName=0, dir=0):

    if not newName:
        newName = prompt(file, "new name?")
    head, tail = os.path.split(file)
    if dir:
        head = dir

    if isFunction(newName):
        newName = newName(removeExtension(tail))

    newName = addExtension(newName, getExtension(tail))
    return os.path.join(head, newName)


def isUtf(file):
    return getExtension(file) in utfe


def isImage(file):
    return getExtension(file) in imge


def isPrivateFile(f):
    return tail(f).startswith(".")


def alwaysDelete(f):
    deleteList = [".clip.js", "passwords.csv"]
    keepList = ["scratchpad.txt", "notes.txt"]
    deleteRE = "view-source|released-items|\\bboo\\b|debug|dela|foo|\(|^-?\d+$"
    deleteExtensions = ["log", "aux", "mhtml", "tex", "zip"]
    name = tail(f)
    if isPrivateFile(f):
        return False
    if name in keepList:
        return False
    if name in deleteList:
        return True
    if test(deleteRE, name, flags=re.I):
        return True
    if fsize(f) < 20:
        return True
    if getExtension(f) in deleteExtensionsList:
        return True


deleteExtensionsList = [
    "gif",
    "wav",
    "ts",
    "ggb",
    "zip",
    "matchcha",
    "m4a",
]


def currentFile():
    return sys.argv[0]


def isRemovablePdfFile(f):
    name = tail(f)[0:-4]
    if len(name) < 4 or test("sdf|asd|\(\d", name):
        return 1


def isWebsite(url):
    from requests import get

    return get(url).status_code == 200


def alert(*args, **kwargs):
    global __alerting
    if __alerting:
        return

    kwargs["caller"] = getCaller()
    kwargs[
        "stop-message"
    ] = "Press [k] to stop seeing this message"
    a = dprompt(*args, **kwargs)
    if a == "k":
        __alerting = 1


def mget(r, s, flags=0, mode=dict):

    if test("^\^", r) and not flags:
        alert(
            "Implicitly setting the flags to re.M",
            r=r,
            flags=flags,
        )
        flags = re.M

    store = []

    def parser(x):
        if x.groups():
            store.append(
                x.group(1)
                if len(x.groups()) == 1
                else x.groups()
            )
        else:
            store.append(x.group(0))

        return ""

    s = re.sub(r, parser, s, flags=flags).strip()

    if mode == list:
        return [s.strip(), store]
    if mode == str:
        if not store:
            config = ""
        else:
            config = store[0]
        return [s, config]

    if not store:
        config = {}
    elif isNestedArray(store):
        config = {k: v for k, v in store}
    else:
        config = {k: True for k in store}

    return s, config


def isNestedArray(x):
    return isArray(x) and exists(x[0]) and isArray(x[0])


def delta(a, b):
    return abs(a - b)


def unzip(file, to):
    import zipfile

    with zipfile.ZipFile(file, "r") as z:
        z.extractall(to)


class DrivePrep:
    def __init__(self, files, debug=0):
        self.files = map(
            files, lambda f: normpath(dldir, f)
        )
        self.dir = outdir
        self.debug = debug

    def __enter__(self):
        if self.debug:
            return
        map(self.files, cfile, self.dir)

    def __exit__(self, *args):
        if self.debug:
            return

        print("done exiting")
        printdir(self.dir)
        emptydir(self.dir)
        printdir(self.dir)


def normDirPath(file):
    dir = dirFromFile(file)
    return npath(dir, file)


def moveToAppropiateDir(name=0):
    file = glf()
    name = changeFileName(file, name)
    path = normpath(dirFromFile(file), name)
    mfile(file, path)


htmlRE = "(?:[\"']|&quot;)(https.*?)(?:\"|&quot;|')"
urlRE = "http.+"


def isPdf(s):
    return isString(s) and getExtension(s) == "pdf"


def writeBuffer(name, data):
    with open(name, "wb") as f:
        f.write(data)
    print("writing name", name)


def unescapeHtml(s):
    import html

    return html.unescape(s)


def isJson(f):
    return getExtension(f) == "json"



def get_text_lines(s):
    s = removeComments(s)
    s = smart_dedent(get_text(s))
    lines = split(s, '\n+')
    lines = map(lines, trim)
    return lines


def smart_dedent(s):
    s = re.sub("^ *\n*|\n *$", "", s)
    if test("^\S", s):
        return s
    spaces = search("^ *(?=\S)", s, flags=re.M)
    secondLineSpaces = search("\n *(?=\S)", s)
    if (
        not spaces
        and secondLineSpaces
        and len(secondLineSpaces) > 4
    ):
        return re.sub(
            "^" + secondLineSpaces[5:], "", s, flags=re.M
        ).trim()

    return re.sub("^" + spaces, "", s, flags=re.M).strip()


def lowerCase(s):
    return s.lower()


def filterTwice(items, ref):
    a = []
    b = []
    for item in items:
        if item in ref:
            a.append(item)
        else:
            b.append(item)
    return [a, b]


def push(store, data=0):
    if not data:
        return
    elif isArray(data):
        store.extend(data)
    else:
        store.append(data)


def appendjson(file, data, mode=0):
    if not data:
        return
    placeholder = [] if mode == list else {}
    store = readjson(file, placeholder)

    if mode == list and not isArray(store):
        store = [store]

    if isArray(store):
        push(store, data)
    elif isObject(store):
        store.update(data)

    # return pprint(stringify(store)) #debugAppendJson
    write(file, store, open=1)


def readjson(file, placeholder={}):
    if isfile(file):
        with open(file) as f:
            return json.load(f)
    else:
        return placeholder


def rangeFromString(s, offset=1):
    if isArray(s):
        return s

    def f(s):
        if "-" in s:
            a, b = split(s, " *- *")
            store = []
            for i in range(int(a), int(b) + 1):
                store.append(i - offset)
            return store
        elif s == "x":
            return None
        else:
            return [int(s) - offset]

    return flat(map(split(s, ", *| +(?=\w)"), f, filter=0))


def zulustamp(date):
    return date.strftime("%Y-%m-%dT%H:%M:%SZ")


def hms():
    return datetime.now().strftime("%c")
    return datetime.now().strftime("%H:%M:%S")


def flatdir(dir):
    files = getfiles(dir, recursive=1, mode=list)
    map(files, mfile, dldir)
    rmdir(dir)
    return map(files, lambda x: npath(dldir, x))


def toVariable(a, b):
    return a + " = " + dumpJson(b)
    prefix = "var"
    return prefix + " " + a + " = " + dumpJson(b)


def renameClipFile():
    f = input("rename clip file as?")
    mfile(
        normDirPath(clipfile),
        normDirPath(addExtension(f, "js")),
    )


def googleId(s):
    return search("d/(.*?)/", s) or s


def cleanupFileName(fileName, date=0, prepend=0):
    if prepend:
        fileName = prependFilePath(tail(fileName), prepend)
    fileName = appendFileName(fileName, date)
    return removeExtension(fileName)


def appendFileName(file, payload=""):
    if not payload:
        return file
    if test("^\.", payload):
        space = ""
    else:
        space = " "
    if test("\.\w+$", file):
        s = re.sub(
            "(?=\.\w+$)", space + payload, file, count=1
        )
    else:
        s = file + space + payload
    return s


def prependFilePath(file, payload):
    if payload:
        payload = capitalize(payload + " ")
    else:
        return file
    head, name = os.path.split(file)
    r = "(?<=(^(?:[a-zA-Z]+ *\d+ +)))"
    if test(r, name):
        return re.sub(r, payload, name)
    return os.path.join(head, payload + name)


class SystemCommand:
    def __init__(self, *args, dir=dir2023, **kwargs):
        chdir(dir)

        def fix(s):
            if "\n" in s and not ";" in s:
                return join(get_text_lines(s), delimiter="; ")
            return s

        if test("^(node|python)", args[0]):
            a = " ".join(map(args, dumpJson))
            a, b = mget(
                "^(?:node|python) \S+ \S+ ", a, mode=str
            )
            if not b:
                b = a
                a = ""
            # prompt(b=b, a=a)
            command = b + shellescape(a)
            # prompt(command=command)
            command += " " + shellescape(dumpJson(kwargs))
            # dprint(a, b, command)
            # pprint('ccc')
            # return
        else:
            command = " ".join(
                map(map(args, dumpJson), fix)
            )

        process = Popen(
            command, stdout=PIPE, stderr=PIPE, shell=True
        )

        data = process.communicate()
        success, error = [decode(d) for d in data]

        clean = lambda x: re.sub(
            "\.$", "", re.sub("^[eE]rror: ", "", x.strip())
        )
        if error:
            error = clean(error)

        self.error = error
        self.success = success.strip()

        pprint(
            {
                "getCaller": "SystemCommand",
                "command": command,
                "error": error,
                "success": success,
            }
        )


def getFirstWord(s):
    return search("[a-zA-Z]+", s)


def xsplit(s, r=" "):
    return split(s, r) if isString(s) else s


def objectf(s):
    keys = xsplit(s)

    def runner(o):
        return {k: v for k, v in o.items() if k in keys}

    return runner


def ff(
    dir=dir2023,
    mode=0,
    once=0,
    sort=0,
    reverse=0,
    recursive=0,
    **kwargs,
):
    if isArray(dir):
        return dir
    # if isString(dir) and getExtension(dir):
    # return findFile(dir)

    if mode == "smallclean":
        kwargs["smallerThan"] = 2
        kwargs["zip"] = 1
        kwargs[
            "include"
        ] = """
            doo.js
            foo.js
            a.js
            b.js
            test.pdf
        """

        kwargs[
            "ignore"
        ] = """
            scratchpad.js

        """

    elif mode == "print":
        sort = True

    if isArray(dir):
        rawFiles = dir
    elif recursive:
        rawFiles = getFilesRecursive(dirgetter(dir))
    else:
        rawFiles = absdir(dirgetter(dir))

    checkpoint = checkpointf(**kwargs)
    if once:
        return find(rawFiles, checkpoint)
    files = filter(rawFiles, checkpoint)
    print("num files", len(files))

    if not files:
        return

    if reverse:
        sort = 1
    if sort:
        if isString(sort):
            if sort == "size":
                sort = fsize

            elif sort == "date":
                sort = mdate

        files.sort(
            key=mdate if sort == 1 else sort,
            reverse=reverse,
        )

    if mode == "smallclean":
        prompt(files, "remove?")
        rfiles(files)
        printdir(dir)
    elif mode == "filetable":
        return write(
            "file-table.txt",
            tabular(
                map(sorted(files, key=mdate), nameAndDate)
            ),
        )

    elif mode == "rename":
        map(files, promptRenameFile)

    elif mode == "save":
        return appendVariable(files)

    elif mode == "print":
        map(files, fileInfo)
    elif mode == "delete":
        prompt(map(files, tail), "delete?")
        map(files, rfile)
    elif mode == "cleanup":
        cleanfiles(files)
    elif mode == "open" or mode == "o":
        map(files, openBrowser)
    elif mode == "info":
        os.system("clear")
        pprint(map(files, fileInfo))
        pprint(len(files))
    elif mode == "clipinfo":
        files.sort(key=mdate, reverse=1)
        f = lambda x: join(map(x, str), delimiter="  ")
        return clip(tabular(map(files, fileInfo, delete=1)))
    elif mode == "delete" or mode == "d":
        prompt(map(files, fileInfo), "delete these files?")
        map(files, rfile)
    elif mode == "backup":
        map(files, cfile, budir)
    elif mode == "label":
        files = choose(files)
        label = prompt("label as?")
        appendVariable(files)
    elif mode == "moveToWorkSpace":
        files = choose(files)
        for file in files:
            dest = changeFileName2(file)
            cfile(file, dest)
    elif mode == "review":
        reviewfiles(files)
    else:
        pprint(files)
        print(len(files))
        return files


def abrev(s):
    r = "\W|(\d)"
    items = filter(re.split(r, s))
    return "".join(map(items, lambda x: x[0])).lower()


def appendVariable(x, name="temp", outpath=0, str=0):
    if isString(x) and isfile(x):
        name = camelCase(removeExtension(x))
        x = read(x)
        outpath = dir2023 + "variables.js"

    s = createVariable(name, x)
    if str:
        s = join(s)

    append(outpath or currentFile(), s)


def arrayToObject(a, f):
    return {f(x): x for x in a}


def getFilesRecursive(dir):
    store = []

    def runner(dir):
        files = absdir(dir)
        for file in files:
            if isIgnoredFile(tail(file)):
                continue
            elif isdir(file):
                runner(file)
            else:
                if len(store) > 100:
                    raise Exception("not allowed to many")
                store.append(file)

    runner(dir)
    return store


def is_empty_dir(dir):
    def runner(dir):
        for file in absdir(dir):
            if isfile(file):
                return False
            elif not runner(file):
                return False

        return True

    return runner(dir)


def getLastNumber(s):
    n = search("(\d+) *(?:\.\w+)?$", s)
    return int(n)


def pdfIt(f):
    name = changeExtension(f, "pdf")
    mfile(f, name)


def mapdir(files, dir):
    return map(files, lambda x: normpath(dir, x))


def toJSON(x):
    name = objectClassName(x)
    if test("Storage$", name):
        return x.store


def getTime():
    return int(datetime.timestamp(datetime.now()))


def getFileName(file):
    return removeExtension(tail(file))


def cleanup(dir, r):
    with CD(dir):
        for f in os.listdir(dir):
            if test(r, f, flags=re.I):
                rfile(f)


def getWords(s):
    return re.findall("[a-zA-Z]{3,}", s)


def getLastWord(s):
    return getWords(s)[-1]


def dirName(s):  # head ?
    return os.path.split(re.sub("/*$", "", s))[1]


def rpw(file, f):
    normWrite(file, f(normRead(file)))


def n2char(n):
    return chr(n + 97)


def normFileToDir(file, name=0):
    if not name:
        name = prompt(file, "name?")
    e = getExtension(file)
    return dirdict.get(e) + addExtension(name, e)


sentenceRE = "(?:\. \"?|\n)([A-Z]\w*(?:'\w+)?)"


base = "https://www.nysedregents.org/ei"


def incrementName(file):
    count = 1
    a, b = mget("(?:\.\w+)+$", file, mode=str)
    while isfile(file):
        count += 1
        file = a + str(count) + b
    return file


def removeFileParens(s):
    return re.sub(" *\(.*?\) *", "", s)


def overrideFile():
    f = glf()
    mfile(f, removeFileParens(f))


def isEmptyDir(dir):
    return isdir(dir) and not os.listdir(dir)


def renameFiles():
    for file in ff(dldir, reverse=1):
        if isEmptyDir(file):
            rfile(file)
            continue

        a = prompt(file)
        if a == "d":
            rfile(file)
        elif a == "c":
            continue
        elif a:
            out = npath(dldir, addExtension(a, "pdf"))
            mfile(file, out)
        else:
            break


def fixUrls(source, links):
    url = fixUrl(source)
    base = url
    first = links[0]
    if not isWebsite(os.path.join(url, first)):
        url = head(url)
        if not isWebsite(os.path.join(url, first)):
            print("ERROR")
        else:
            base = url

    return map(links, lambda x: os.path.join(base, x))


def downloadPDF(url, name=0):
    if not name:
        name = addExtension(
            prompt(url, "outpath name"), "pdf"
        )
    outpath = npath(dldir, name)

    from requests import get

    r = get(url, stream=True)
    chunkSize = 10000
    with open(outpath, "wb") as fd:
        for chunk in r.iter_content(chunkSize):
            fd.write(chunk)

    ofile(outpath)
    return outpath


def reverse(x):
    if isObject(x):
        return {b: a for a, b in x.items()}
    return list(reversed(x))


def to2023(*files):
    def runner(file):
        a = jsdir + file
        b = dir2023 + file
        if not isfile(a):
            a = dldir + file
        assert isfile(a)
        cfile(a, b)

    map(files, runner)


def cleandir(dir):
    print("cleaning the dir", dir)
    files = filter(absdir(dir), alwaysDelete)
    pprint(files)
    map(files, rfile)


def renameLastFile(file="Extra Worksheet"):
    mfile(glf(), npath(dldir, addExtension(file, "pdf")))


def finfo(f):
    if isfile(f):
        name = tail(f)
        date = datestamp(f)
        size = fsize(f)
        return [name, date, size]
    else:
        return [name]


def isGunk(file):
    return getExtension(file) in gunkExtensions


def seeVersions():
    SystemCommand(
        """
        npm -v
        node -v
    """
    )


def renameLastFile():
    f = glf()
    mfile(f, changeFileName(f, prompt(f)))


def pickFileFromDir(dir=dldir):
    ofile(choose(absdir(dir)))


def sub(s, r, f, **kwargs):
    def g(x):
        if isString(f):
            return f
        if x.groups():
            return f(*x.groups())
        else:
            return f(x.group())

    return re.sub(r, g, s, **kwargs)


def memoize(fn):
    store = {}

    def wrapper(*args):
        if args in store:
            return store[args]
        else:
            value = fn(*args)
            store[args] = value
            return value

    return wrapper


def dollarPrompt(x):
    if isArray(x):
        item = choose(x, mode=1)
    elif isObject(x):
        item = choose(list(x.values()), mode=1)
    else:
        item = x

    @memoize
    def f(x):
        return prompt(item=item, fallback=x) or x

    @memoize
    def g(x):
        return prompt(item, "input:")

    while True:
        if test("\$([a-zA-Z]\w*)", item):
            item = sub(item, r, f, count=1)
        else:
            break

    n = 0
    while True:
        n += 1
        r = "\$" + str(n)
        if test(r, item):
            item = sub(item, r, g)
        else:
            break

    return item


def getNameArgsKwargs(s):
    if test("^\w+$", s):
        return [s, [], {}]
    name, s = search("(\w+)\((.*?)\)", s)
    s, kwargs = mget("(\w+) *= *([^\s,]+)", s)
    args = split(s, ", *| +")
    return name, args, kwargs


def stringCall(fn, *args):
    # prompt(args)
    items = map(args, dumpJson)
    # prompt(items)
    argString = ", ".join(items)
    return f"{fn}({argString})"


def dprint(*variables, **kwargs):

    store = ["DPRINT:"]

    for v in variables:
        vars = (
            inspect.currentframe().f_back.f_locals.items()
        )
        name = [
            v_name for v_name, v_val in vars if v_val is v
        ][0]
        store.append([name, v])

    for a, b in kwargs.items():
        store.append([a, b])

    pprint(store)


env.basepyref["rnlf"] = "rnl"
env.basepyref["nd"] = "newdir"


def arrToDict(a):
    return {i + 1: v for i, v in enumerate(a)}


def getNumbers(s):
    return map(re.findall("\d+", s), int)


def getUntil(items, checkpoint):
    store = []
    for item in items:
        if checkpoint(item):
            store.append(item)
        else:
            break
    return store


env.basepyref["wm"] = "watchMovie"


env.basepyref["rlcf"] = "renameLocalClipFile"


def check(x):
    prompt(x)
    return x


def removeLastFile(dir=dldir):
    file = glf(dirgetter(dir))
    prompt("is this file correct?", file)
    rfile(file)


def removeDateString(s):
    return re.sub(" *\d+[-/]\d+[-/]\d+ *$", "", s)


env.basepyref["rlf"] = "removeLastFile"


def dsearch(s, dict, template=""):
    r = reWrap(dict, template)
    m = search(r, s)
    return dict[m] if m else None


env.basepyref["o"] = "ofile"


def removeComments(s):
    return re.sub("^[#/].+\n*", "", s, flags=re.M)


def renameFile(input, output):
    outpath = changeFileName(input, output)
    mfile(input, outpath)
    ofile(outpath)


def numbered(items, title=""):
    if title:
        title = "  " + title + "\n"
    s = "\n" + title + "\n"
    for i, item in enumerate(items):
        spaces = "  " if i < 9 else " "
        s += (
            "  "
            + str(i + 1)
            + "."
            + spaces
            + stringify(item)
            + "\n"
        )
    return s


def dlf():
    rfile(glf())


env.basepyref["dep"] = "deprecateFile"

env.basepyref["ff"] = "ffApp"


def configString(kwargs):
    s = ""
    for k, v in kwargs.items():
        s += k + " = " + v + " "
    return s.strip()


def deleteKey(item, key):
    if isObject(item):
        item.pop(key)
    return item


def getYearNumber():
    return datetime.now().year


def hasKey(x, key):
    return isObject(x) and x.get(key)


def indent(items):
    return join(map(items, lambda x: "    " + x))


def getBindingNames(s):
    r = "^(?:class|const|var|(?:async )?function) (\w+)"
    return re.findall(r, s, flags=re.M)


def isChinese(s):
    return test("[\u4e00-\u9fa5]", s)


def isEnglish(s):
    return test("[a-zA-Z]", s)


def copydir(src, to):
    newDir = npath(to, src)
    assert not isdir(newDir) and isdir(to)
    prompt(f"copying {src} to {newDir}")
    shutil.copytree(src, newDir)
    print(f"copying directory: {newDir}")


def get_usb_dir():
    if isdir(usbdrivedir):
        return usbdrivedir
    elif isdir(sandir):
        return sandir
    else:
        raise Exception("no usb dir")


def saturdate():
    return upcomingDate("saturday", strife="-")


def getSaturdayDir(dir):
    return os.path.join(dir, saturdate())


def swapFiles(a, b):
    a = addExtension(a, "js")
    b = addExtension(b, "js")
    s = read(a)
    cfile(b, a)
    write(b, s)


def sayhi(s):
    return "Hello from " + s + "!"


def coerceArray(x):
    if isArray(x):
        return x
    if x == None:
        return []
    return [x]


def save(**kwargs):
    for k, v in kwargs.items():
        appendVariable(v, name=k)
        break


def checkpoint_factory(schema):
    def c2(**kwargs):
        # print(kwargs)
        def transform(a, b):
            # print(a, b)
            if b == str:
                return lambda x: test(a, x, flags=re.I)

            if b == bool:
                print(a, b)
                return lambda x: x == a

            if b == int:
                return lambda x: x > a

        store = []
        for k, v in schema.items():
            arg = kwargs.get(k)
            if arg != None:
                store.append([k, transform(arg, v)])

        def checkpoint(item):
            for k, v in store:
                arg = item.get(k)
                if arg and not v(arg):
                    return False

            return True

        return checkpoint

    return c2


def obj_filter(items, **kwargs):
    schema = {
        "title": str,
        "owner": str,
        0: int,
        "delete": bool,
    }

    getter = getterf(kwargs.get("get"))
    c1 = checkpoint_factory(schema)
    f = c1(**kwargs)

    values = [getter(item) for item in items if f(item)]
    return values


def small(x):
    return x[0:3]


def getterf(*args):
    args = flat(
        map(args, lambda x: split(x, "[, ]+") if x else [])
    )
    if not args:
        return identity

    def fn(item):
        store = {}
        for arg in args:
            if arg in item:
                store[arg] = item[arg]
        return store

    return fn


def googleDocsJson():
    if prompt("would you like to see what it looks like?"):
        return tempGoogleDocJson
    return read(drivedir + "allGoogleDocs.json")


def comment(s):
    return "# " + s


def dprompt(*variables, **kwargs):

    import inspect

    strings = []
    caller = getCaller()
    from collections import OrderedDict

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


def get_file_name(s):
    return removeExtension(tail(s))


def is_js(f):
    return getExtension(f) == "js"


def is_json(f):
    return getExtension(f) == "json"


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


# smart_path('a.js', 'b.py')

# targets lf
# open
# move
# copy
# swap


def super(x):
    appendVariable(x)


temp = [
    "/home/kdog3682/.viminfo.tmp",
    "/home/kdog3682/.viminfz.tmp",
    "/home/kdog3682/.viminfy.tmp",
    "/home/kdog3682/.viminfx.tmp",
    "/home/kdog3682/.viminfw.tmp",
    "/home/kdog3682/.viminfu.tmp",
    "/home/kdog3682/.viminft.tmp",
    "/home/kdog3682/.viminfv.tmp",
    "/home/kdog3682/.viminfs.tmp",
    "/home/kdog3682/.viminfq.tmp",
    "/home/kdog3682/.viminfr.tmp",
    "/home/kdog3682/.viminfp.tmp",
    "/home/kdog3682/.viminfn.tmp",
    "/home/kdog3682/.viminfm.tmp",
    "/home/kdog3682/.viminfl.tmp",
    "/home/kdog3682/.viminfk.tmp",
    "/home/kdog3682/.viminfj.tmp",
    "/home/kdog3682/.viminfi.tmp",
    "/home/kdog3682/.viminfh.tmp",
    "/home/kdog3682/.viminfg.tmp",
    "/home/kdog3682/.viminff.tmp",
    "/home/kdog3682/.viminfe.tmp",
    "/home/kdog3682/.viminfd.tmp",
    "/home/kdog3682/.viminfc.tmp",
    "/home/kdog3682/.viminfb.tmp",
    "/home/kdog3682/.viminfa.tmp",
    # "/home/kdog3682/.viminfo",
]


def get_item_info(item):
    try:
        item_type = type(item).__name__
        item_length = len(item)
        item_constructor = item.__class__.__name__
        item_parent = item.__class__.__base__.__name__
        item_child_types = [
            child.__name__
            for child in item.__class__.__subclasses__()
        ]

        info = f"Type: {item_type}\nLength: {item_length}\nConstructor: {item_constructor}\nParent: {item_parent}\nChild Types: {item_child_types}"
        return info

    except Exception as e:
        return f"Error: {str(e)}"


def save(x):
    assert x
    clip(x)
    return
    info = get_item_info(x)
    name = prompt(
        name="write a name for this file", info=info
    )
    tag = "json" if not isPrimitive(x) else "js"
    name = addExtension(name, tag)
    name = "clip." + name
    write(name, x)


def count_function_params(fn):
    return len(inspect.signature(fn).parameters)


# save(reduce(temp, read))

# super(ff('~/', name='viminf[a-z].tmp'))


temp = [
    "/home/kdog3682/.viminfo.tmp",
    "/home/kdog3682/.viminfz.tmp",
    "/home/kdog3682/.viminfy.tmp",
    "/home/kdog3682/.viminfx.tmp",
    "/home/kdog3682/.viminfw.tmp",
    "/home/kdog3682/.viminfu.tmp",
    "/home/kdog3682/.viminft.tmp",
    "/home/kdog3682/.viminfv.tmp",
    "/home/kdog3682/.viminfs.tmp",
    "/home/kdog3682/.viminfq.tmp",
    "/home/kdog3682/.viminfr.tmp",
    "/home/kdog3682/.viminfp.tmp",
    "/home/kdog3682/.viminfn.tmp",
    "/home/kdog3682/.viminfm.tmp",
    "/home/kdog3682/.viminfl.tmp",
    "/home/kdog3682/.viminfk.tmp",
    "/home/kdog3682/.viminfj.tmp",
    "/home/kdog3682/.viminfi.tmp",
    "/home/kdog3682/.viminfh.tmp",
    "/home/kdog3682/.viminfg.tmp",
    "/home/kdog3682/.viminff.tmp",
    "/home/kdog3682/.viminfe.tmp",
    "/home/kdog3682/.viminfd.tmp",
    "/home/kdog3682/.viminfc.tmp",
    "/home/kdog3682/.viminfb.tmp",
    "/home/kdog3682/.viminfa.tmp",
]


class FileManager:
    def __init__(self, files):
        self.files = files

    def delete(self):
        prompt(
            files=self.files,
            message="Do you wish to delete these files?",
        )
        self.map(rfile)

    def info(self):
        pprint(self.map(get_file_info))

    def open(self):
        ofile(self.files[0:5])

    def map(self, fn):
        map(self.files, fn)


def get_file_info(f):
    strife = "%A %B %d %Y, %-I:%M:%S%p"
    name = tail(f)
    date = datestamp(f, strife)
    size = fsize(f)
    return {
        "name": tail(f),
        "size": fsize(f),
        "date": date,
    }



# man(temp).delete()



def push_js():
    dir = dir2023
    cleandir(dir)
    #data = parseDiff()
    #prompt(data=data)

    mainCommand = f"""
        cd {dir}
        git status --short
        echo 'linebreak'
        git diff --word-diff
        echo 'linebreak'
        git add .
        git commit -m "'push'"
        git push
    """

    print('this works')
    s = SystemCommand(mainCommand)
    clip(s.success + '\n' + s.error)

    #append('git-logs.json', data)
    "diff.txt"



def man(x=dir2023, **kwargs):
    x = ff(x, **kwargs)
    assert x
    fm = FileManager(x)
    return fm

cover_letter_kwargs = dict(dir=dldir, name='cover|resume', minutes=10)
#man(**cover_letter_kwargs).

#ff(cover_letter_kwargs)


cvfile = "Kevin Lee Cover Letter.pdf"
resumefile = "Kevin Lee Resume.pdf"

#mlf
