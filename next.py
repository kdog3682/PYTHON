import env
from base import *

def removeJavascriptStuff(s):
    s = re.sub(
        "^(console|module|exports).+", "", s, flags=re.M
    )
    s = re.sub(
        "^(class|if) [\w\W]+?\n}\n", "", s, flags=re.M
    )
    return s


def appScript(f, data=None, use=""):
    namer = lambda f: normDirPath(addExtension(f, "js"))
    files = map(split(use, ",? +"), namer)
    files.append(env.appscriptfile)
    s = ""
    if use:
        s += removeJavascriptStuff(normRead("utils.js"))
    s += mergefiles(files)
    s += "\n\n"
    s += toCallable(f, data)
    google_request(s)
    print("called google")


def appScript(f, data=None):
    s = read(env.appscriptfile) + "\n\n"
    s += toCallable(f, data)
    google_request(s)


def googlePrint(s):
    clip(s)


def googleOpen(o):
    webbrowser.open(o)

def googleValue(s):
    pprint(s)


def googleLogs(s):
    for item in toArray(s):
        print(smallify(item))


def googleWrite(obj):
    file = obj.get("file")
    value = obj.get("value")
    normWrite(file, value, open=1)


def googleCreateVariable(obj):
    file = obj.get("file")
    value = obj.get("value")
    name = obj.get("name")
    lang = getExtension(file)
    if isObject(value):
        payload = join(
            [
                createVariable(k, v, lang)
                for k, v in value.items()
            ]
        )
    else:
        payload = createVariable(name, value, lang)

    prompt(abspath(file), payload, 'appendVargoogle?')
    append(file, payload)


def googleAppScript(f="", *args):
    s = read(env.GOOGLE_APPSCRIPT_FILE).strip()
    r = "^(?:(?:// *|import).+)(?:\n+(?:// *|import).+)*"
    s, imports = mget(r, s, flags=re.M, mode=str)
    # gas
    store = []
    if imports:
        imports = re.findall(
            "^import (\S+)", imports, flags=re.M
        )
        for i in imports:
            if i == "clip":
                print("adding clip import")
                store.append(
                    createVariable("clip", clip(), "js")
                )
            elif i == "clip2":
                store.append(
                    createVariable("clip2", clip(2), "js")
                )
            elif getExtension(i) == "js":
                store.append(normRead(i))
            else:
                file = normRead(i + ".temp.json")
                data = createVariable(
                    camelCase(i), file, "js"
                )
                store.append(data)

        s = join(store) + "\n\n" + s

    callable = f if '\n' in f else toCallable(f, *args)
    s += "\n\n" + callable
    ref = {
        "print": googlePrint,
        "open": googleOpen,
        "write": googleWrite,
        "clip": googlePrint,
        "clip": googlePrint,
        "value": googleValue,
        "vim": googleVim,
        "logs": googleLogs,
        "error": lambda x: print(x),
        "createVariable": googleCreateVariable,
        "appendVariable": googleCreateVariable,
    }

    data = google_request(s)
    try:

        pprint(data)
        print("starting google appscript function series")
        for k, v in data.items():
            if v and ref[k]:
                print('::' + k + '::\n')
                ref[k](v)
    
        print(linebreak)
        print('done with google appscript')
    except Exception as e:
        print(data)
    


def googleVim(s):
    appendVim("filedict", s)


def googleTranslate(x, lang="chinese"):
    dict = {"chinese": "Chinese", "spanish": "Spanish"}
    s = f"{read(appscriptfile)}\n\nlanguageString = `\n{textgetter(x)}\n`.trim()\n\n"
    s += f"translate{dict.get(lang, 'chinese')}(languageString)"

    def spanish(x):
        return {
            "input": x.get("input"),
            "value": x.get("value"),
            "lang": "spanish",
        }

    def chinese(x):
        value = x.get("value")
        original = x.get("input")
        data = read(chifile)
        data = map(list(value), lambda x: data.get(x, x))
        data = "".join(data)
        return {
            "input": original,
            "value": value,
            "pinyin": data,
            "lang": "chinese",
        }

    value = google_request(s, locals().get(lang))
    return value.get("value")
    return value
    pprint(value)


def google_request(data):
    from requests import post

    response = post(env.appscripturl, stringify(data))
    try:
        value = json.loads(response.text)
    except:
        value = response.text

    #print("--------------------------------------")
    #pprint(value)
    #print("--------------------------------------")
    return value


def _dropbox(files, push=1, pull=0):
    from dropbox import Dropbox
    from dropbox.files import WriteMode

    def _pull(file):
        with open(file, "rb") as f:
            dbx.files_upload(
                f.read(),
                "/" + file,
                mode=WriteMode("overwrite"),
            )

    def _push(file):
        with open(file, "rb") as f:
            dbx.files_upload(
                f.read(),
                "/" + file,
                mode=WriteMode("overwrite"),
            )

    with Dropbox(env.dropboxtoken) as dbx:
        dbx.users_get_current_account()
        return
        if pull:
            map(files, _pull)
            print("Done at Pulling from Dropbox")
        elif push:
            print("Starting push")
            return
            map(files, _push)
            print("Done at Posting to Dropbox")


def _drive(files):
    map(files, cfile, drivedir)


def _cleandir(dir="."):
    def f(file):
        if isRemovableFile(file):
            rfile(file)
        else:
            return 1

    return filter(absdir(dir), f)


def runMacbook():
    kwargs = toKwargs()
    printer(**kwargs)


def _sweep(items):
    partitioner = Partitioner(items)

    store = partitioner.storage.store
    tempest(store, "sweep.json")
    log("partitioner-inputs", partitioner.inputs)


def _cleanup():
    ref = read("sweep.json")
    chdir(drivedir)
    files = os.listdir(drivedir)
    ref = edit(ref, lambda k, v: filter(v, includef(files)))
    pprint(ref)
    return

    for k, v in ref.items():
        if k == "trash" or k == "pdf":
            map(v, rfile)
        elif k == "gsheet":
            continue
        else:
            dir = drivedir + k.upper()
            mkdir(dir)
            map(v, mfile, dir)


def downloadGithubFile(
    file, user="kdog3682", repo="codemirror"

def downloadIt(f):
    if isUrl(f):
        name = tail(f)
        if isfile(name):
            return name
        write(name, request(f))
        return name
    return f


def tempest(data=0, name=0):
    f = "temp.json"
    if not data:
        print("no data")
        return
    write(f, data)
    ofile(f)
    return
    if not data:
        return

    if not name:
        name = addExtension(
            tail(sys.argv[0]), "json", force=1
        )

    if isRecent(name, minutes=5):
        prev = read(name)
        if deepEqual(data, prev):
            return prev

    if not data:
        lib = globals()
        if lib.get("store"):
            data = lib.get("store")
    if not data:
        print("no data")
        return

    write(name, data)
    ofile(name)
    return ""


def getFileDependencies(file):
    e = getExtension(file)
    if e == "js":
        regex = "require\(['\"]?\.?/?([\w.]+)"
    if e == "py":
        regex = "(?:\n|^)from ([\w]+) import"
    if e == "html":
        regex = (
            "['\"]"
            + "(\S+\.(?:js|css|jpeg|png|svg|jpg))"
            + "['\"]"
        )

    files = unique(
        re.findall(regex, removeComments(read(file)))
    )
    if e == "html":
        files.append(file)
    elif e == "py":
        files = map(files, lambda x: addExtension(x, "py"))
    return files

def getFileDependencies(file):
    e = getExtension(file)
    if e == "js":
        regex = "require\(['\"]?\.?/?([\w.]+)"
    if e == "py":
        regex = "(?:\n|^)from ([\w]+) import"
    if e == "html":
        regex = (
            "['\"]"
            + "(\S+\.(?:js|css|jpeg|png|svg|jpg))"
            + "['\"]"
        )

    files = unique(
        re.findall(regex, removeComments(read(file)))
    )
    if e == "html":
        files.append(file)
    elif e == "py":
        files = map(files, lambda x: addExtension(x, "py"))
    return files


def queryString(base="quotable.io", root="quotes", ref={}):
    def runner(ref):
        s = ""
        for k, v in ref.items():
            s += k + "=" + str(v) + "&"
        return s[:-1]

    return (
        "https://" + base + "/" + root + "?" + runner(ref)
    )


def _gzip(file):
    import gzip

    with gzip.open(file, mode="rb") as f:
        data = json.loads(f.read().decode("utf-8"))
        return data


def log(key=0, files=0, file=0):
    if files:
        files.sort()
        data = map(
            files,
            lambda x: datestamp() + " " + key + " " + x,
        )
        pprint(data)
        input()

    elif file:
        data = datestamp() + " " + file

    append("/home/kdog3682/logs.txt", join(data))


def getJspy():
    import inspect

    locals = inspect.currentframe().f_back.f_locals
    indexes = ["js", "py", "vim", "bash", "css", "html"]
    #ref = locals()
    pprint(locals)


def worwo(fn, args):
    return fn(*args) if exists(args) else fn()


def sendToOutboundDrive(file=None):
    return cfile(file, outdir)


def sendEmail():
    s = read("letters.txt")
    subject, body = splitonce(s, "\n")
    to = "nadiranarine@gmail.com"
    to = "kdog3682@gmail.com"

    callable = f"""
        email2({{
            'subject': '{subject}',
            'body': `{body}`,
            'to': '{to}',
        }})
    """
    googleAppScript(callable)


def fixChromebookFilePath(s):
    if "penguin" in s:
        s = re.sub(
            ".*?penguin", "/home/kdog3682", s, count=1
        )
        s = re.sub("%20", " ", s)
    return s



def lastFile(key):
    f = mostRecent(dirgetter(key))
    assert isfile(f)
    return f


def macPrint():
    url = macdirdict.get("drive")
    cmd = "lp -o sides=two-sided-long-edge " + url
    os.system(cmd)



def printer(
    file=None, doubleSided=1, copies=1, landscape=0
):
    command = "lpr"
    if not file:
        file = lastFile("outbound")
    if doubleSided:
        command += " -o sides=two-sided-long-edge"
    if copies:
        command += f" -n {copies}"
    if landscape:
        command += " -o landscape"
    command += " " + file
    print(command)
    os.system(command)


def foo():
    f = "/home/kdog3682/CWF.files.json"
    data = read(f)
    store = []
    for k, v in data.items():
        chdir(k)
        a = choose(v)
        store.append(map(a, abspath))


def foo1():
    # files  =  temp()
    # y  =  files.get('y')
    b = read("/home/kdog3682/CWF.files.json")

    def p(v):
        partitioner = Partitioner(v)
        return partitioner.storage.store

    files = {
        k: p(v)
        for k, v in b.items()
        if not "vosk" in k and isdir(k)
    }
    tempest(files)
    return
    store = []
    trash = []
    folders = ff(onlyFolders=1, dir="cwf", public=1)
    _sweep(folders)
    # prompt(folders)
    # map(folders, rmdir, 1)
    # log('removing', folders)
    # return

    for f in folders:
        if f == "public":
            input("skipping public")
            continue
        files = os.listdir(f)
        a = choose(files)
        if len(a) == len(files):
            a = None
        if a:
            store += map(a, lambda x: os.path.join(f, x))
        if input("delete dir? " + f):
            trash.append(f)

    write("files.json", store)
    prompt(store)
    ofile("files.json")
    dirs = choose(trash)
    map(dirs, rmdir)


def rmdirs(dirs):
    log("rmdir", dirs)
    map(dirs, lambda x: rmdir(x, 1))


def happend(file, data, open=0):
    if not data:
        return
    file = toRoot(file)
    append(file, data)
    ofile(file)


def hwrite(file, data, open=0):
    if not data:
        return
    file = toRoot(file)
    write(file, data)
    if open:
        ofile(file)


def hread(file):
    return ofile(toRoot(file))
    return read(toRoot(file))


def hjson(key, *args):
    data = key if isObject(key) else {key: args}
    prev = read("jspy.json") or {}
    prev.update(data)
    hwrite("jspy.json", data, open=1)


def jspydata(lang="js"):
    ref = {"python": {}}
    # try:
    # parent = getCaller()
    # ref = hread('jspy.json')
    # indexes = ['js', 'py', 'vim', 'bash', 'css', 'html']
    # data = ref[parent][indexes.index(lang)]
    # return data
    # except Exception as e:
    # return


def build_my_functions(lang):
    path = lang + ".functions.json"
    files = ff(lang)
    data = {tail(f): getFunctionNames(f) for f in files}
    hwrite(path, data)

    # "leftovers.py",
    # "ignore.py",
    # "combine.py",
    # "websterdictionary.json",
    # "wordlist.json",
    # "googlewordlist.txt",
    # "commonwords.json",
    # "top3000words.json",
    # "paction.js",
    # "twil.js",


temp = [
    "/home/kdog3682/CWF/08-22-2021/library.json",
    "/home/kdog3682/CWF/08-22-2021/pylibrary.json",
    "/home/kdog3682/CWF/08-22-2021/pyscrap.json",
    "/home/kdog3682/CWF/08-22-2021/githubgists.json",
    "/home/kdog3682/CWF/08-22-2021/corpus.json",
    "/home/kdog3682/CWF/08-22-2021/database.rules.json",
    "/home/kdog3682/CWF/08-22-2021/firebase.json",
    "/home/kdog3682/CWF/08-22-2021/sandisk.json",
    "/home/kdog3682/CWF/08-22-2021/oldconfig.json",
    "/home/kdog3682/CWF/08-22-2021/config.json",
    "/home/kdog3682/CWF/08-22-2021/topposts_passtimemath.json",
    "/home/kdog3682/CWF/08-22-2021/topposts_eli5.json",
    "/home/kdog3682/CWF/08-22-2021/topposts_explainlikeimfive.json",
    "/home/kdog3682/CWF/08-22-2021/pylib.json",
    "/home/kdog3682/CWF/08-22-2021/gmat.json",
    "/home/kdog3682/CWF/08-22-2021/raw.json",
    "/home/kdog3682/CWF/08-22-2021/code.log.json",
    "/home/kdog3682/CWF/08-22-2021/asd.json",
    "/home/kdog3682/CWF/08-22-2021/master.json",
    "/home/kdog3682/CWF/08-22-2021/links.json",
    "/home/kdog3682/CWF/08-22-2021/aops-raw-links.json",
    "/home/kdog3682/CWF/08-22-2021/ml.json",
    "/home/kdog3682/CWF/08-22-2021/mathcounts.json",
    "/home/kdog3682/CWF/08-22-2021/mlx.json",
    "/home/kdog3682/CWF/08-22-2021/mlx2.json",
    "/home/kdog3682/CWF/08-22-2021/docnotes.json",
    "/home/kdog3682/CWF/08-22-2021/raw_reddit_photoshopbattles.json",
    "/home/kdog3682/CWF/08-22-2021/raw_reddit_mementomoriok.json",
    "/home/kdog3682/CWF/08-22-2021/explainlikeimfive.json",
    "/home/kdog3682/CWF/08-22-2021/passtimemath.json",
    "/home/kdog3682/CWF/08-22-2021/eli5.json",
    "/home/kdog3682/CWF/08-22-2021/config (1).json",
    "/home/kdog3682/CWF/08-22-2021/Redirector.json",
    "/home/kdog3682/CWF/08-22-2021/ml2.json",
    "/home/kdog3682/CWF/08-22-2021/explanations.json",
    "/home/kdog3682/CWF/08-22-2021/explanations2.json",
    "/home/kdog3682/CWF/08-22-2021/euismod.json",
    "/home/kdog3682/CWF/08-22-2021/pmwb.json",
    "/home/kdog3682/CWF/08-22-2021/token.json",
    "/home/kdog3682/CWF/08-22-2021/credentials.json",
    "/home/kdog3682/CWF/08-22-2021/stats.json",
    "/home/kdog3682/CWF/08-22-2021/keys.json",
    "/home/kdog3682/CWF/08-22-2021/mywords.json",
    "/home/kdog3682/CWF/08-22-2021/gmail-draft-ids.json",
    "/home/kdog3682/CWF/08-22-2021/gmail-message-ids.json",
    "/home/kdog3682/CWF/08-22-2021/gmail-draft-messages.json",
    "/home/kdog3682/CWF/08-22-2021/letternotes.json",
    "/home/kdog3682/CWF/08-22-2021/gmail-messages-cleaned.json",
    "/home/kdog3682/CWF/08-22-2021/savestore.json",
    "/home/kdog3682/CWF/08-22-2021/leftovers.js.json",
    "/home/kdog3682/CWF/08-22-2021/websterdictionary.json",
    "/home/kdog3682/CWF/08-22-2021/wordlist.json",
    "/home/kdog3682/CWF/08-22-2021/commonwords.json",
    "/home/kdog3682/CWF/08-22-2021/top3000words.json",
    "/home/kdog3682/CWF/08-22-2021/myshortcuts.json",
    "/home/kdog3682/CWF/08-22-2021/deps.json",
    "/home/kdog3682/CWF/08-22-2021/mybookmarks.json",
    "/home/kdog3682/CWF/08-22-2021/vimbookmarks.json",
    "/home/kdog3682/CWF/08-22-2021/leftovers.py.json",
    "/home/kdog3682/CWF/08-22-2021/temp2.json",
    "/home/kdog3682/CWF/08-22-2021/temp3.json",
    "/home/kdog3682/CWF/08-22-2021/answers.json",
    "/home/kdog3682/CWF/08-22-2021/errors.json",
    "/home/kdog3682/CWF/08-22-2021/success.json",
    "/home/kdog3682/CWF/08-22-2021/scraperun.json",
    "/home/kdog3682/CWF/08-22-2021/storageinfo.json",
    "/home/kdog3682/CWF/08-22-2021/amc8answers.json",
    "/home/kdog3682/CWF/08-22-2021/amc8.json",
    "/home/kdog3682/CWF/08-22-2021/amc8errors.json",
    "/home/kdog3682/CWF/08-22-2021/success1.json",
    "/home/kdog3682/CWF/08-22-2021/aopsAMC_10answers.json",
    "/home/kdog3682/CWF/08-22-2021/aopsAMC_10problems.json",
    "/home/kdog3682/CWF/08-22-2021/aopsAMC_12answers.json",
    "/home/kdog3682/CWF/08-22-2021/aopsAMC_12problems.json",
    "/home/kdog3682/CWF/08-22-2021/aopsAHSMEanswers.json",
    "/home/kdog3682/CWF/08-22-2021/aopsAHSMEproblems.json",
    "/home/kdog3682/CWF/08-22-2021/aopserrors.json",
    "/home/kdog3682/CWF/08-22-2021/dictarrays.json",
    "/home/kdog3682/CWF/08-22-2021/info.json",
    "/home/kdog3682/CWF/08-22-2021/1a.json",
    "/home/kdog3682/CWF/08-22-2021/1b.json",
    "/home/kdog3682/CWF/08-22-2021/1c.json",
    "/home/kdog3682/CWF/08-22-2021/aopsfixed.json",
    "/home/kdog3682/CWF/08-22-2021/z.json",
    "/home/kdog3682/CWF/08-22-2021/x.json",
    "/home/kdog3682/CWF/08-22-2021/aops-product.json",
    "/home/kdog3682/CWF/08-22-2021/aopsfixeddictionary.json",
    "/home/kdog3682/CWF/08-22-2021/10958.json",
    "/home/kdog3682/CWF/08-22-2021/aopsamc8master.json",
    "/home/kdog3682/CWF/08-22-2021/lengths.json",
    "/home/kdog3682/CWF/08-22-2021/plot.vegalite.json",
    "/home/kdog3682/CWF/08-22-2021/defaultcss.json",
    "/home/kdog3682/CWF/08-22-2021/pages.json",
    "/home/kdog3682/CWF/08-22-2021/value.json",
    "/home/kdog3682/CWF/08-22-2021/indexfileinfo.json",
    "/home/kdog3682/CWF/08-22-2021/maclookbehinderrorlines.json",
    "/home/kdog3682/CWF/08-22-2021/tempx.json",
    "/home/kdog3682/CWF/08-22-2021/mathwords.json",
    "/home/kdog3682/CWF/08-22-2021/gmat-math.json",
    "/home/kdog3682/CWF/08-22-2021/css-abre.json",
    "/home/kdog3682/CWF/08-22-2021/css-abrev.json",
    "/home/kdog3682/CWF/08-22-2021/tach.json",
]

def _gr(inpath, r, outpath, flags=0):
    if isNumber(r):
        r = f"\\b[a-z]{{{r}}}\\b"
    s = textgetter(inpath)
    m = sort(
        filter(unique(re.findall(r, s, flags)), ignoreWords)
    )
    print(len(m))
    write(outpath, m, open=1)
    return m


def clipf(fn):
    def decorator(self, *args, **kwargs):
        value = fn(self, *args, **kwargs)
        clip(value)

    return decorator


def earlyReturn(fn):
    def decorator(self, *args, **kwargs):
        value = fn(self, *args, **kwargs)
        self.value = value
        return value

    return decorator


def stateCache(fn):
    def decorator(self, *args, **kwargs):
        value = fn(self, *args, **kwargs)
        self.value = value
        return value

    return decorator


def getsetf(file, prepend=0, name=0, append=0):
    def wrapper(fn):
        def decorator():
            data = parseJSON(read(file))
            value = fn(data)
            if name:
                if isNestedArray(value):
                    value = dict(value)
                value = createVariable(name, value, "")
            if prepend:
                write(
                    prepend, value + "\n\n" + read(prepend)
                )

            elif append:
                write(append, read(append) + "\n\n" + value)
            else:
                write(file, value, open=1)

        return decorator

    return wrapper


def stateAction(f=0):
    def wrapper(fn):
        def decorator(self, *args, **kwargs):
            value = fn(self, *args, **kwargs)
            clip()

        return decorator

    return wrapper


def logf(fn):
    def decorator(*args, **kwargs):
        value = fn(*args, **kwargs)
        return value

    return decorator


def find_file(q, dir=dldir):
    with CD(dir):
        files = sorted(os.listdir(dir), key=mdate)
        for file in files:
            if test(q, file):
                return abspath(file)


def glf(dir=dldir, **kwargs):
    if kwargs.get('q'):
        return find_file(dir=dir, q=kwargs.get('q'))
    file = mostRecent(dir, **kwargs)
    return file


def p(k, v):
    if v < 10000:
        return
    return v
    if test("[^'\w]", k):
        return
    if v < 1000:
        return 1000
    if v < 10000:
        return 10000
    if v < 100_000:
        return 100_000
    if v < 1_000_000:
        return 1_000_000


def A1(dir):
    path = (
        f"/home/kdog3682/CWF/public/{dir}.functions.json.js"
    )
    prompt(path)

    def runner(f):
        store = []
        file = tail(f)
        date = mdate(f)
        lib = functiongetter(read(f), f)
        for name, value in lib.items():
            store.append(
                {
                    "file": file,
                    "date": date,
                    "name": name,
                    "value": value,
                }
            )
        return store

    data = ff(dir=dir, fn=runner, js=1)
    write(path, data, open=1)


def A1(dir):
    path = (
        f"/home/kdog3682/CWF/public/{dir}.functions.json.js"
    )
    prompt(path)

    def runner(f):
        store = []
        file = tail(f)
        date = mdate(f)
        lib = functiongetter(read(f), f)
        for name, value in lib.items():
            store.append(
                {
                    "file": file,
                    "date": date,
                    "name": name,
                    "value": value,
                }
            )
        return store

    data = ff(dir=dir, fn=runner, js=1)
    write(path, data, open=1)


def scrapeEmojis():
    chdir("cwf")
    request = RequestLimiter()

    u = "https://emojipedia.org/noto-emoji/"
    r = 'href="([\w-]{3,})"'
    r2 = 'value="(.*?)"'
    store = {}

    def f(x):
        url = u + x
        m = search(r2, request.get(url))
        if m:
            store[x] = m

    data = gr(r)
    map(data, f)
    write("emojis.json", store, open=1)


def gr():
    # s = map(re.findall(r, globalconfig.strip(), flags = re.M), filter)
    last = re.split(
        "\n+", globalconfig.strip(), flags=re.M
    )[-1]
    r = "^(\S+) (.*?) (\S+) *$|^(\S+) *\n(\S.+) *\n(\S+)$"
    s = filter(search(r, last))
    if s:
        if "finder" in s[0] and "http" in s[1]:
            fn, *args = s
            print(args)
            return globals().get(fn)(*args)
        if "\\" in s[1]:
            inpath, regex, outpath = s
            outpath = addExtension(outpath, "json")
            _gr(inpath, regex, outpath)
            return

    r = "^(\S+) (\S.+)$"
    s = search(r, last)
    if s:
        a, b = s
        if a == "read":
            value = read(b)
            pprint(value)
            return value


def saveas(inpath, outpath):
    if isfile(outpath) and not prompt(
        "overrwrite?", outpath
    ):
        return

    outpath = normpath(inpath, outpath)
    outpath = addExtension(outpath, getExtension(inpath))
    prompt("move it?", inpath, outpath)
    write(outpath, read(inpath))
    clear(inpath)


def rf(r, s, flags=0):
    m = re.findall(r, s, flags)
    if not m:
        return []
    f = lambda x: x not in env.ignoreWords and len(x) > 2
    return sort(filter(unique(m), f))


def isf(file):
    a = pubdir + file
    if isfile(a):
        print(a)
        return

    a = cwfdir + file
    if isfile(a):
        print(a)
        return
    print("not a file")


def boo():
    """
    the rootdir always refers to ~/
    this may not be active
    it is not active
    todo
    """

    files = ff(txt=1, dir="root", ignore="logs|questions")
    data = split(join(map(files, read)), "\n\n+")
    write("data.json.js", data)
    prompt(files)
    map(files, rfile)


def incorporateCss(outpath=None):
    file = mostRecent(dldir, css=1)
    # raise Exception(file)
    s = read(file)
    append(
        "/home/kdog3682/CWF/public/" + outpath + ".css", s
    )


def temp():
    return read(tempfile)


def _addcss(file=None):
    last = mostRecent(dldir)
    if getExtension(last) == "css":
        append(
            "/home/kdog3682/CWF/public/new.css", read(last)
        )


def ldf(x):
    dir = drivedir
    e = None
    if isdir(x):
        dir = x
    else:
        e = [x]
    files = filter(absdir(dir), checkpointf(extensions=e))
    recent = mostRecent(files, hours=10)
    pprint(recent)
    return recent



def namer(x):
    print(getCaller(-1) + ":", x)


def _asset(name, data):
    append(
        "/home/kdog3682/CWF/public/" + name,
        createVariable(
            removeExtension(name), data, lang="js"
        ),
    )



def sendTextMessages(f):
    s = textgetter(f)
    r = "^ *(?:// *)?" + datestamp()
    s = re.split(r, s, flags=re.M)
    s = s[-1]
    s = removeComments(s, f)
    s = split(s, "^--+", flags=re.M)

    def fn(s):
        print(s)
        lang = search("hi|hola|hello|nihao", s, flags=re.I)
        ref = {
            "hi": "english",
            "hola": "spanish",
            "hello": "english",
            "nihao": "chinese",
        }
        lang = ref.get(lang.lower(), "english")
        if lang == "english":
            return s

        return googleTranslate(s, lang)

    return map(map(s, fn), _twilio)


def writeAllFunctions(key="pub", query=0):
    ref = {
        "pub": {"js": 1, "dir": "pub"},
        "jch": {"js": 1, "dir": "jch"},
    }

    lang = "js" if ref[key].get("js") else "py"
    name = join(
        "functions", key, lang, "json", delimiter="."
    )
    kwargs = ref[key]
    if query:
        data = read(name)
        data = filter(data, lambda k, v: some(v, query))
        files = 0
        with CD(dirgetter(kwargs.get("dir"))):
            files = map(list(data.keys()), abspath)
        print(files)
        write("temp-bookmarks.files.txt", files)
        return
    return

    files = ff(**kwargs)

    def f(f):
        return [tail(f), sort(getFunctionNames(read(f)))]

    append("bookmarks.files.txt", name)
    write(name, reduce(files, f), open=1)


def writeStringToCurrentFile(s):
    frame = inspect.currentframe()
    frame = inspect.getouterframes(frame)[1]
    s = (
        inspect.getframeinfo(frame[0])
        .code_context[0]
        .strip()
    )
    args = s[s.find("(") + 1 : -1].split(",")

    names = []
    for i in args:
        if i.find("=") != -1:
            names.append(i.split("=")[1].strip())
        else:
            names.append(i)

    argName = names[0]


def currentify():
    file = glf()
    dest = "/home/kdog3682/CWF/public/current.txt"
    if test("^\w+\.\w+$", tail(file)):
        dest = tail(file)
    cfile(file, pubdir + dest)


def mainScrape():

    r = regexjoin(
        regexdiv("pre"),
        regexdiv("code"),
        regexdiv("div", attrs='class="highlight'),
    )
    url, regex = splitonce(prompt("url and regex*"))
    text = request(url)
    if regex:
        regex = RegexLib.get(regex, regex)
        m = sorted(unique(findall(regex, text)))
        write(
            "scrape.js", createVariable("temp", m), open=1
        )
    else:
        m = findall(r, text)
        m = filter(m, lambda x: len(x) > 100)
        m = map(m, getPureHtml)
        s = "\n\n".join(m)
        s = removeComments(s)
        write("scrape.js", s, open=1)


def super(s):
    # input('starting super!!!')
    arg = search(".+$", s.strip()).strip()
    a, b = splitonce(arg)
    myFunctions = globals()
    if a in myFunctions:
        f = myFunctions[a]
        f(b) if b else f()
        return

    else:
        r = regexdiv("table")
        m = re.findall(r, request(arg))
        # write('scrape.json', m)


def createGoogleSecret():
    data = {
        "web": {
            "client_id": env.google_client_id,
            "client_secret": env.google_client_secret,
            "redirect_uris": [],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://accounts.google.com/o/oauth2/token",
        }
    }
    write("client_secrets.json", data)


todo = {
    "google-webscript-app.js": "d",
    "index2.js": "fn",
    "runpy.js": "fn",
    "i3.js": "yes",
    "sock.js": "d",
    "index.js": "io",
    "allowed-words.js": "md",
    "test.js": "d",
    "t7.js": "d",
    "apps.js": "d",
    "appendself.js": "d",
    "sr.js": "k",
    "htmlparser.js": "d",
    "comments.js": "",
    "lrt.js": "",
    "anime-utils.js": "",
    "nerd-utils.js": "skip small",
    "th.js": "",
    "graph.js": "",
    "go.js": "fn",
    "math-transform.js": "some useful stuff in it",
    "prosemirror-renderer.js": "d",
    "cmd.js": "d",
    "pm-helpers.js": "d",
    "px.js": "d",
    "prosemirror-utils.js": "d",
    "t.drafts.js": "d",
    "recursive.drafts.js": "was useful once but not anymore",
    "re.js": "slot example",
    "recursive.js": "itneresting has some vue stuff for recursive components",
    "recursive-helpers.js": "some interesting vue stuff",
    "randomColor.js": "color lib",
    "debug.js": "d",
    "filebins.js": "d",
    "jshint-messages.js": "kl",
    "lrcss.js": "",
    "lr.js": "",
    "cl.js": "fn",
    "cf.js": "",
    "file-builder.js": "useful",
    "codemirror-utils.js": "skip small",
    "file-loader.js": "d",
    "vue-file-loader.js": "vuec",
    "vue-file-reader.js": "d",
    ".js": "fn",
    "browser-text-editor.js": "d",
    "keyrefs.js": "seems kinda useful",
    "demo.js": "d",
    "todo.js": "another parser of some sort",
    "aa.js": "d",
    "cm3.js": "kinda uf",
    "jsparser.js": "the parser object for js codemirror",
    "lezer-terms.js": "",
    "tokens.js": "",
    "cmparser.js": "a",
    "calender.js": "interesting",
    "dunno.js": "d",
    "x.js": "vuestorage and other fns",
    "xxx.js": "d",
    "z.js": "an aggregator of some sort",
    "z2.js": "skip small",
    "xx.js": "js input handler for cm",
    "cmt.js": "d",
    "todo2.js": "uh ... has a dumb vpa function in it",
    "cmtxt.js": "cm archive",
    "cm.draft.js": "d",
    "school-utils.js": "fn",
    "codemirror-component.js": "cma",
    "xxxx.js": "",
    "basic.js": "",
    "scraped.js": "",
    "socket-action.js": "pretty nice",
    "key-listener.js": "d",
    "r3.js": "spent alot of time on this",
    "r2.js": "not too sure what this is",
    "math-assets.js": "skip small",
    "r4leftovers.js": "",
    "shortcuts.js": "skip small",
    "voice-recorder.js": "voice recorder vue component and class",
    "ju3.js": "jxg init extract maybe",
    "vvv.js": "",
    "words.js": "d",
    "svg-microphone.js": "d",
    "dark-theme.js": "d",
    "ttt.js": "d",
    "light-theme.js": "d",
    "vv.js": "d",
    "t6components.js": "i think it is done because math-components ate it",
    "depot.js": "more vue stuff",
    "recursive.backup.js": "i think all the recursive stuff is done",
    "r5.js": "spent a lot of time on this ... also has a generatorplugin class",
    "target.js": "d",
    "example.js": "it is another prosemirror thing d",
    "prosemirror-setup.js": "d",
    "html-parser.js": "fn",
    "voice-utils.js": "more callbacks for the voice app",
    "cm2.js": "skip small",
    "chatbot.js": "a project for coding a voice chat box",
    "voice-to-command.js": "official",
    "story.js": "rn coding-story-for-kids.txt",
    "r7.js": "d",
    "game.js": "math game one day",
    "refs.js": "might be useful but not sure",
    "css-extra.js": "try it out for animation of css",
    "tile-match.js": "tilematch comp",
    "t6.js": "this is actually kind of legit. i spent about a month on it. dont throw it away. it does the layering of components one at a time.",
    "mathquill.js": "has mathquill component. all by itself. but i think math-components.js has eaten it",
    "html-edit.js": "i feel like it is simlar to html-parser.js...",
    "post.js": "fn",
    "nerdcheck.js": "d",
    "input-handlers.js": "codemirror stuff",
    "foo.js": "skip small",
    "voice-callbacks.js": "some sort of vtc thing",
    "vue-transitions.js": "review this has another parser",
    "anime.js": "skip small",
    "animations.js": "skip small",
    "v.js": "i think this represents the old math.js",
    "snippet-manager.js": "cm snippet stuff",
    "edit.js": "skip small",
    "base.js": "skip small",
    "temp.js": "a super long file with htmlparser and vuelineparser in it",
    "cmath.js": "skip small",
    "annyang.js": "official",
    "waterfall.js": "fn",
    "advanced-utils.js": "fn",
    "math-packages.js": "boookkeeper??? and some interesting fns",
    "old-lego.js": "i think this is lego",
    "more-refs.js": "i think this is a super ref which gets transformed",
    "launch.js": "d",
    "string-utils.js": "i feel llike this file should be combined elsewhere",
    "code-runner.js": "vue cm coderunner",
    "fuzzy.js": "d",
    "element-controller.js": "official",
    "letter.js": "edit",
    "audio-player.js": "official",
    "m1.js": "d",
    "m3.js": "d",
    "cm.js": "cm.js",
    "mc.js": "skip small",
    "cu.js": "skip small",
    "r4c.js": "skip small",
    "r3c.js": "r3c.js",
    "m3c.js": "skip small",
    "render.js": "edit",
    "svg.js": "d",
    "fpdf.js": "skip small",
    "server.js": "another server",
    "prose.js": "d",
    "speaker.js": "speakers or smth",
    "bb.js": "d",
    "trash.js": "skip small",
    "math-games.js": "one day?",
    "100colors.js": "d",
    "base-icon.js": "ok",
    "colors.js": "ok it is an asset of nested colors",
    "traash.js": "fn",
    "vuetify.js": "some sort of vuetify thing ",
    "math-levels.js": "driller levels array",
    "driller-methods.js": "ok",
    "store.js": "const",
    "lezer-utils.js": "skip small",
    "lezer-js.js": "ok",
    "lud.js": "ok",
    "geometry.js": "geo stuff",
    "r4.js": "skip small",
    "app.js": "skip small",
    "api-weather.js": "weather stufff",
    "asciiLetters.js": "",
    "github.js": "d",
    "html-transform.js": "another html transformer....",
    "lego-utils.js": "skip small",
    "r6.js": "d",
    "node-css-html.js": "d",
    "aggregate.js": "another aggregator",
    "lrgen.js": "ok",
    "w.js": "skip small",
    "foobar.js": "",
    "cm-utils.js": "pl",
    "app-fastmath.js": "skip small",
    "prepare-reddit.js": "prepare reddit and some spellcheck stuff it seems",
    "reddit-parser.js": "skip small",
    "trie.js": "",
    "lex.js": "edit",
    "asd.js": "coding-assignment future",
    "r6a.js": "this was def used somewhere. it has a new style() which is like divify()",
    "run.js": "d new fileloader ... nah i dont think so",
    "jsxgraph-utils.js": "off",
    "ju2.js": "jxg stuff",
    "xcv.js": "skip small",
    "sdf.js": "const",
    "gg.js": "skip small",
    "g.js": "another lezer thing",
    "quill.js": "the std quill",
    "text-builders.js": "off",
    "prosemirror-math-index.js": "d",
    "quill-component.js": "fn",
    "exponents1.math.js": "d",
    "adfg.js": "d",
    "browser-file-editor.js": "line editors kinda like rpw.js",
    "sdfg.js": "skip small",
    "clip.temp.js": "d",
    "nerdamer-utils.js": "edit",
    "math.js": "d",
    "cleanup-notes.js": "edit",
    "useful.js": "skip small",
    "math-prose.js": "skip small",
    "abc.js": "d",
    "sudoku.js": "d",
    "4nums.js": "the javascript game of 24",
    "dialogue.js": "edit",
    "utility-components.js": "more components ... should be merged into smth",
    "vue-components.js": "skip small",
    "vue-base.js": "skip small",
    "my-strings.js": "has some math text in it",
    "master-utils.js": "d",
    "hi.js": "d",
    "new.js": "vue math game stuff and a fn",
    "today.js": "d",
    "divify.js": "divify stuff prly delete it",
    "h.js": "another vue function for rendering data mathlevels levelupatmath and fourcorners",
    "e.js": "svg artist ... shud be useful somewhere",
    "q.js": "d",
    "class1.js": "skip small",
    "html-utils.js": "another html edit lol ............... not sure",
    "question-generator.js": "d because the new worksheet kind of supercedes it",
    "qgold.js": "off",
    "t5.js": "old math components",
    "stylesheet.js": "might be in ec.js... dunno",
    "output.js": "skip small",
    "raw.js": "d",
    "scratchpad.js": "d",
    "math-input.js": "displayer for division",
    "examples.js": "slot example",
    "prettier.js": "skip small",
    "learning.js": "off",
    "a.js": "edit",
    "b.js": "skip small",
    "c.js": "combine into a.js",
    "d.js": "edit",
    "pug.js": "off",
    "sdfsdfs.js": "skip small",
    "classroom.js": "skip small",
    "class2.js": "keep for now i think it is class2 and review it edit",
    "asadsd.js": "d",
    "assets.js": "off",
    "a2.js": "fn",
    "css-utils.js": "off",
    "puppet.js": "off",
    "env.js": "off",
    "a1.js": "edit it has proliferateClassNames which is pretty useful as well as a divfactory() which abstrcts vue even further",
    "ec.js": "off",
    "lego.js": "off",
    "pretty.js": "edit it",
    "run-node.js": "what is this file",
    "browser.js": "off",
    "editor.temp.js": "rn na-xie-nian.subtitles.txt",
    "math-utils.js": "off",
    "print.js": "off",
    "scrape2.js": "d",
    "scrape.js": "d",
    "vue-utils.js": "off",
    "node-utils.js": "off",
    "kenken.js": "edit",
    "color-utils.js": "off",
    "chart-utils.js": "off",
    "s4.js": "d",
    "s3.js": "d",
    "f.js": "vue stuff and colors",
    "s.js": "skip small",
    "c2.js": "d",
    "rpw.js": "off",
    "prose-utils.js": "off",
    "utils.js": "off",
    "nerdstep.js": "d",
    "asdf.js": "edit",
    "math-components.js": "off",
    "doc.js": "cur",
    ".clip.js": "d",
    "class.js": "off",
    "TextEditor.js": "off",
}

def sendToDrive(file=None, n=1):
    cfile(mostRecent(dldir, n), drivedir)


def recentPdfs(dir=dldir):
    return ff("dl pdf")


def sortfiles(files):
    data = map(files, lambda f: (tail(f), datestamp(f)))


def outboundData():
    chdir("pub")
    f = prompt("choose file name")
    f = addExtension(f, "json")
    data = createVariable(
        "outboundData", read(f), lang=None
    )
    write("outbound-data.js", data)


def inboundData():
    data = read(glf())
    store = dataFile()
    savedIndexes = data.get("saved")
    values = [store[i] for i in savedIndexes]
    tempest(values)
    return values


def dataFile():
    return mostRecent(dldir, name="pdf.json$")


def pdf0901():
    file = "/mnt/chromeos/MyFiles/Downloads/Acing the New SAT Math PDF Book.pdf.json"
    pages = read(file)
    tests = []
    exercises = []

    for i, page in enumerate(pages):
        i = i + 1
        if itest("exercises? (?:-|\\\\u|\u2013)", page):
            exercises.append(i)
        elif itest("chapter\s+\d+\s+practice\s+test", page):
            tests.append(i)

    tests = tests[5:]
    store = []
    count = 0
    length = len(tests)
    i = -1
    answers = []

    while count < length:
        i += 1
        count += 1
        if count == 3:
            count = 0
            try:
                a = tests[i - 2]
                b = tests[i - 1]
                store.extend(list(range(a, b)))
                answers.append(b + 1)
            except Exception as e:
                break

    write(
        "pages.json",
        {
            "exercises": exercises,
            "answers": answers,
            "tests": store,
        },
        open=1,
    )


def earlyExit(*args):
    for arg in args:
        print(arg)
    a = input("")
    if a:
        raise Exception("early exit")


def saveClip():
    name = prompt("choose a save clip destination")
    earlyExit(
        name, "are you sure? type any input to cancel"
    )
    dest1 = normpath(drivedir, name)
    dest2 = normpath(pubdir, name)
    cfile("/home/kdog3682/CWF/public/.clip.js", dest1)
    cfile("/home/kdog3682/CWF/public/.clip.js", dest2)


def openLastFile():
    ofile(glf(dldir))


def readClip():
    v = parseJSON(
        read("/home/kdog3682/CWF/public/.clip.js")
    )
    return v


def fixFileNameFactory(dir):
    chdir(dir)
    files = os.listdir(dldir)

    def fixFileName(file):
        if not isfile(file):
            r = "^" + search("\w+", file)
            f = testf(r, flags=re.I)
            file = find(files, f)
            if not file:
                raise Exception("no file", item.get("file"))
        return file

    return fixFileName


def sortByNumber(arr):
    def f(s):
        return int(search("\d+", s))

    return sort(arr, f)


def divify(tag, content):
    if not isString(content):
        content = newlineIndent(content)

    return f"<{tag}>{content}</{tag}>"


def text(*args):
    args = flat(args)
    s = join(args)
    f = "text.txt"
    write(f, s)
    ofile(f)
    raise Exception()


def delagoogleEmail(obj):
    googleAppScript(toCallable("email4", obj))


def listdir(x):
    return os.listdir(x)


def python3(*args):
    system("python", *args)


def emptydir(dir):
    if isdir(dir):
        files = absdir(dir)
        if len(files) == 0:
            print("directory already empty")
        else:
            map(files, os.remove)


def downloadYoutube(urls):
    import youtube_dl

    outpath = (
        "/home/kdog3682/CWF/public/music/%(title)s.%(ext)s"
    )
    urls = toArray(urls)
    if isObject(urls[0]):
        urls = [url.get("url") for url in urls]

    options = {
        "format": "bestaudio/best",
        "outtmpl": outpath,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download(urls)


def consolidate(file):
    lang = getExtension(file)
    comment = jspy(lang, "superComment") + file + "\n\n"
    append(
        "/home/kdog3682/consolidate." + lang,
        comment + read(file) + "\n",
    )
    print("consolidated", file)


def review(key, move=0, mode=0, **kwargs):
    files = ff(key, **kwargs)
    if not files:
        return 

    removed = []
    moved = []
    os.system("clear")

    for file in files:
        if alwaysDelete(file):
            rfile(file)
            removed.append(files)
            continue

        if mode == 'open':
            if isUtf(file):
                ofile(file)

        elif isImage(file):
            ofile(file)

        a = prompt(tail(file), "d=delete, c=consolidate\n\n")
        if a == "d":
            rfile(file)
            removed.append(files)
        elif a == "c":
            consolidate(file)
            rfile(file)
        elif a == "m":
            if move:
                mfile(file, move)
                moved.append(file)
        elif a:
            if move:
                mfile(file, changeFileName(file, a, move))
        elif mode == 'delete':
            pass
            #print('delete mode')
            
    pprint(removed)


def unmove():
    mfile(getLast(absdir(trashdir)), cwfdir)
    # print(glf(trashdir))
    # mfile(glf(trashdir), cwfdir)


def dostufff(todo):

    chdir(pubdir)
    store = {}
    for k, v in todo.items():
        if v.startswith("off"):
            continue
        elif v == "d" or v == "" or isRemovableFile(k):
            try:
                rfile(k)
            except Exception as e:
                continue
        elif v == "fn" or v == "c":
            consolidate(k)
            rfile(k)
        else:
            store[k] = v

    clip(store)



def mlf():
    f = glf()
    if True or is_json(f) and dprompt(f, 'is a json file. do you want to javascriptify it?'):
        return write(npath(dir2023, changeExtension(f, 'js')), createVariable(file_name(f), read(f), 'js'))
    return mfile(f, dirFromFile2(f))


def moveback():
    f = getLast(absdir(trashdir))
    d = dirFromFile(f)
    prompt(d, f)
    mfile(f, d)


def renameQuizzes():
    chdir(dldir)
    ref = {
        "g4 quiz.pdf": "Grade 4 Quiz.pdf",
        "g5quiz.pdf": "Grade 5 Quiz.pdf",
    }
    for k, v in ref.items():
        if isfile(k):
            mfile(k, v)


def autodir(file):
    dir = dirFromFile(file)
    chdir(dir)
    return dir


def recentFiles():
    dirs = [rootdir, pubdir, cwfdir]
    store = []
    for dir in dirs:
        store.extend(ff(dir=dir, days=1))
    return store


def fs1(s):

    def allFiles(**kwargs):
        dirs = [rootdir, pubdir, cwfdir]
        store = []
        for dir in dirs:
            store.extend(ff(dir=dir, **kwargs))
        return store

    """
    1. grab all pdf json txt files
    2. make directories for pdf json and text
    3. iterate thru files and move them to the dir
    """
    files = allFiles(pdf=1, json=1, txt=1)

    ref = {"pdf": pdfdir, "json": jsondir, "txt": txtdir}
    for dir in ref.values():
        if not isdir(dir):
            mkdir(dir)

    for file in files:
        e = getExtension(file)
        if e == "json":
            if review11(file):
                continue
        d = ref.get(e, "")
        if d:
            mfile(file, d)


def uploadResumeAndCoverLetter():
    files = mostRecent(dldir, n=5, minutes=10)
    donecv = 0
    doneres = 0
    for file in files:
        if test("cv|cover|letter", file, flags=re.I):
            if donecv:
                continue
            donecv = 1
            mfile(file, normpath(dldir, cvfile))
        else:
            if doneres:
                continue
            doneres = 1
            mfile(file, normpath(dldir, resumefile))


def cleanupfiles(dir, f):
    files = filter(absdir(dir), f)
    deleteFiles(files, save="deleted-files.log.txt")


def ase(f):
    s = parseJSON(read(clipfile))
    if isArray(s):
        s = map(unique(s), f)
    else:
        s = f(s)

    append(currentFile(), createVariable("temp", s))


def toLocalFile(key):
    name = localfiledict.get(key, key)
    dir = "CWF/public"
    return os.path.join(
        "file:///media/fuse/crostini_25bd1ae3ef71bac8d459747ce670faa67d509f14_termina_penguin/",
        dir,
        name,
    )
def noDots(x):
    def runner(x):
        return re.sub("(?<=/)\.(?=[^/]+$)", "", x)

    if isString(x):
        return runner(x)
    return map(x, runner)


def deleteFiles(files, save=0, title=0):
    map(files, mfile, trashdir)
    if save:

        def infoRunner(f):
            return [tail(f), datestamp(f)]

        info = map(files, infoRunner)
        payload = prettyTable(info, title=title)
        happend(save, payload)
        print("Finished deleting files")







def rnl():  # name: renameLastFile
    f = glf()
    print(f)
    s = input("new name: ")
    mfile(f, changeFileName(f, s))





def smartRead(file):
    dirs = unique(list(dirdict.values()))
    for dir in dirs:
        f = os.path.join(dir, file)
        if isfile(f):
            return pprint(read(f))



def getFilesByTimeStamp():
    files = mostRecent(dldir, 10, js=1, css=1)
    files.reverse()

    last = 0
    store = []

    for file in files:
        date = mdate(file)
        if last == 0 or delta(date, last) < ONE_MINUTE:
            store.append(file)
            last = date
        else:
            return store


def moveFilesByTimeStamp():
    return map(getFilesByTimeStamp(), mfile, jsdir)


def filePicker(dir, key="open"):
    items = (
        dir
        if isArray(dir)
        else sorted(absdir(dirdict.get(dir)), key=mdate)
    )
    files = choose(items)

    if key == "open":
        map(files, ofile)
    elif key == "rename":
        for file in files:
            mfile(
                file,
                changeFileName(
                    file, input(file + "\nnew name? ")
                ),
            )

    else:
        print(files[0])
        return files[0]


def h(data=0):
    hfile = normpath(jsondir, "temp.json")
    if data:
        write(hfile, data, open=1)
    else:
        return read(hfile)


def ranger(a):
    return list(range(a[0], a[1] + 1))



def prompt2(x):
    os.system("clear")
    number(x)
    a = input("choose 1 based indexes or regex\n\n")
    return a


def findFile(f):
    dirs = unique(dirdict.values())
    store = []
    for dir in dirs:
        file = npath(dir, f)
        if isfile(file):
            size = fsize(file)
            if size > 10:
                print('valid')
                print(size)
                print(file)
                return file



def shell(cmd):
    os.system(cmd)



def plf():
    write(".foooooo", glf(), open=1)



def extracter(r):
    store = []
    for item in h():
        name = search(r, item)
        if name:
            store.append(name.strip())
    clip(store)


def vimFileOpener(arg=0, cf=0):
    file = cf
    if arg in urldict:
        file = fixUrl(urldict[arg])
    elif arg in localfiledict:
        file = toLocalFile(arg)
    elif arg in list(localfiledict.values()):
        file = toLocalFile(arg)
    elif isUrl(arg) or getExtension(arg):
        file = arg
    elif arg:
        file = googleSearchQuery(arg)
    openBrowser(file)


def googleSearchQuery(s):
    s = s.replace(" ", "+")
    return f"https://google.com/search?q={s}"


def revertFile(name=None):
    dir = localbackupdir
    print("getting file from dir:", dir)
    file = os.path.join(dir, name) if name else  mostRecent(dir)
    todir = dirFromFile(tail(file))
    newName = prompt(fileInfo(file, r=1), dir=dir, todir=todir)
    if newName:
        todir = npath(todir, addExtension(newName, getExtension(file)))
        prompt(outpath=todir)
    cfile(file, todir)

    return 
    print("getting file from budir", budir)
    file = mostRecent(budir)
    dir = dirFromFile(tail(file))
    prompt(fileInfo(file, r=1), dir)
    cfile(file, dir)


def parseGoogleDate(s):
    return s[5:10] + "-" + s[0:4]



def javascript(file, *args):
    file = npath(jsdir, addExtension(file, "js"))
    response = SystemCommand("node", file, *args)
    if response.error:
        return -1


def changeLastJsonFileToJavascriptAsset():
    name = glf()
    assert isJson(name)
    data = json.dumps(read(name))
    name = camelCase(tail(name))
    s = "var " + name + " = " + data
    normAppend("json.js", s)



def addWordsToDictionaryf(s, corpus=None):
    known = normRead("known.json") or []
    s = textgetter(s)
    words = unique(
        map(re.findall("\\b[a-zA-Z]{2,}\\b", s), lowerCase)
    )
    words = filter(words, known)
    if not corpus:
        corpus = normRead("corpus.json")

    knownWords, unknownWords = filterTwice(words, corpus)

    determined = {}
    undetermined = []

    for word in unknownWords:
        a = prompt(word)
        if a:
            determined[word] = a
        else:
            undetermined.append(word)

    appendjson(normDirPath("known.json"), knownWords)
    appendjson(normDirPath("words.json"), determined)
    appendjson(
        normDirPath("undetermined.json"), undetermined
    )



def dread(name):
    return read(dldir + addExtension(name, "json"))


def dwrite(name, data):
    write(dldir + addExtension(name, "json"), data, open=1)


def getPokemonData():
    store = []
    for i in range(1, 151):
        url = "https://pokeapi.co/api/v2/pokemon/" + str(i)
        data = request(url)
        types = [
            el.get("type").get("name")
            for el in data.get("types")
        ]
        name = data.get("name")
        store.append(
            {
                "name": name,
                "types": types,
            }
        )
        print("okay", i)

    print(len(store))
    dwrite("pokemon", store)


def createPokemonTemplateComponents(amount=1):
    data = dread("pokemon")
    store = []

    def g(x):
        # local attrs
        attr, value = x.groups(1)
        attrs[attr] = {"default": value}
        return ":" + attr + '="' + attr + '"'

    def f(x):
        # local name
        styleString = (
            ' class="'
            + "pokemon"
            + "-icon\" :style=\"{'width': size + 'px', 'height': size + 'px'}\""
        )
        s = x.group(0)
        s = re.sub(
            ' *(xml).*?".*?"', styleString, s, count=1
        )
        s = re.sub(' *(ver).*?".*?"', "", s, count=1)
        # s = re.sub('(width|height|viewbox).*?"(.*?)"', g, s, count=3, flags=re.I)
        return s

    for n in range(1, amount + 1):

        name = data[n - 1].get("name")
        name = camelCase(name)
        attrs = {
            #'name': {'default': name},
            "size": {"default": "100"},
        }
        s = decode(
            read("pokemon-svg/svg/" + str(n) + ".svg")
        )
        # s = re.sub('[\w\W]+?(?=<g)', '', s, count=1)
        s = re.sub("[\w\W]+?(?=<svg)", "", s, count=1)
        s = re.sub("[\w\W]+?>", f, s, count=1)
        # s = re.sub('</svg>\s*$', '', s, count=1)
        #'template': '<template>' + s + '</template>',
        payload = {
            #'name': name,
            "props": attrs,
            "template": s,
        }
        # s = toVariable(name, payload)
        store.append(payload)

    clip(join(store))



def downloadPdfsFromUrl(url=None):
    if not url:
        url = input("url? ")
    s = request(url)
    domain = getDomainName(url)
    r = "href=['\"]?(\S+?(?:\.pdf|view))"
    m = unique(re.findall(r, s))
    for file in m:
        name = tail(file)
        if isfile(examdir + name):
            continue
        try:
            data = request(domain + file)
            if len(data) < 10000:
                print("is small", file)
                continue
            write(examdir + name, data)
        except Exception as e:
            print("error", name)
            pass


def upcomingDateObject(s):
    date = upcomingDate(s, datetime)
    string = datestamp(date, "/")
    array = [date.month, date.day, date.year]
    dueDateObject = date + timedelta(days=8)
    dueDate = {
        "month": dueDateObject.month,
        "day": dueDateObject.day,
        "year": dueDateObject.year,
    }

    dueTime = {
        "hours": 1,  # 9PM
        "minutes": 0,
        "seconds": 0,
    }

    scheduledDate = date.replace(
        hour=9, minute=0, second=0, day=date.day + 0
    )
    currentDate = datetime.now()

    if scheduledDate.day == currentDate.day:
        scheduledTime = None
    else:
        scheduledTime = zulustamp(scheduledDate)

    return {
        "array": array,
        "string": string,
        "dueDate": dueDate,
        "dueTime": dueTime,
        "scheduledTime": scheduledTime,
    }


def nodemon():
    chdir(servedir)
    s = nodedir + "nodemon/bin/nodemon.js"
    runjs(s + " " + "server.js")



def foo():
    chdir(dldir)
    url = "view-source:https://commons.wikimedia.org/wiki/Category:SVG_chess_pieces"
    r = hrefRE("[/\w:_]+", "svg")
    domain = getDomainName(url)
    m = unique(re.findall(r, request(url)))
    links = map(m, lambda x: domain + x)
    prompt(links)
    for link in links:
        name = tail(link)
        try:
            write(name, request(link))
        except Exception as e:
            print("error", name)



class NewYear:
    def __init__(self):
        print("Running Python New Year")
        self.run()

    def run(self):
        self.doDirectories()
        self.doCleanup()

    def doDirectories(self):
        year = datetime.now().year
        for dir in dirs:
            renamedir(dir, appendFileName(dir, "." + year))
            mkdir(dir)


def rnc(s):
    month = datetime.now().strftime("%B").lower()
    s = addExtension(s, "json")
    s = appendFileName(s, "." + month)
    s = clipdir + tail(s)
    cfile(clipfile, s)
    ofile(s)


def clips():
    files = ff(dir=jsondir, name="\.clip")
    chooseAndOpen(files)


def chooseAndOpen(files):
    files = choose(files)
    ofile(files)



def activityLog(name=0, oncePerDay=0):
    data = normRead("activities.log")
    date = datestamp()


def toFactory(lang):
    def runner(x):
        return addExtension(x, lang)

    return runner


path = "/home/kdog3682/CWF/public/notes.txt"

def hrefRE(s, e=0):
    if e:
        s += "\." + e
    r = "href=['\"]?" + parens(s)
    return r

toPdf = toFactory("pdf")
def gitCloner(url):
    chdir(jsdir)
    name = tail(url)
    response = SystemCommand("git clone", url)
    if response.error:
        return

    dir = normpath(jsdir, name)



def temp(s):
    write("temp.js", s, open=1)


def inferKeyFromText(s):
    ref = {
        "pre": 5,
        "li": 50,
    }

    for k, v in ref.items():
        c = len(re.findall("<" + k + "\\b", s))
        if c > v:
            return k

    raise Exception("no key found")


class TextAnalysis:
    def __init__(self, s, key=0):

        self.s = textgetter(s)
        if not key:
            key = inferKeyFromText(self.s)
        self.key = key
        self.get(key)

    def get(self, key):
        ref = env.scrapeRef

        parsers = {
            "li": liParser,
            "tr": liParser,
            "pre": liParser,
            "html": liParser,
        }

        names = {
            "li": "scrape.txt",
            "p": "scrape.txt",
            "pre": "scrape.txt",
            "tr": "scrape.txt",
        }
        postparsers = {
            "pre": prePostParser,
        }

        r = ref.get(key)
        value = unique(re.findall(r, self.s))

        if not value:
            print("didnt get a value", key)
            return
            clip(self.s)
            print("no value")
            return

        if parsers.get(key):
            value = map(value, parsers.get(key))

        if postparsers.get(key):
            return postparsers.get(key)(value)

        if names.get(key):
            return normWrite(
                names.get(key), join(value), open=1
            )

        # pprint(value, key)
        clip(sorted(value))
        return value


def htmlBodyParser(s):
    import bs4
    import html

    body = bs4.BeautifulSoup(s, "html.parser").body
    s = []
    for item in body.find_all(recursive=False):
        text = item.get_text()
        s.append(text)
    return s


def liParser(s):
    import bs4
    import html

    s = bs4.BeautifulSoup(s, "html.parser").get_text()
    s = html.unescape(s)
    s = s.replace(r"\r", "")
    return s


def foo(s):
    return map(
        s,
        lambda x: [getFirstWord(tail(x)), x]
        if getExtension(x)
        else None,
    )



def foo(s):
    return ref



def olf():
    ofile(glf())



def findInDir(dir, key):
    files = printdir(dir)
    return find(files, testf(key))


def doYesterday():
    files = unique(xsplit(textgetter(filelogfile), "\n+"))


def evaljs(s):
    file = "temp.js.txt"
    write(file, s)
    response = SystemCommand("node", file)

    s = """
    console.log(2)
    console.log(3)
    console.log({a:1})
    console.log(JSON.stringify([{a:2}], null, 4))


    """

    s = """
    var x = require("@lezer/html/dist/index.cjs")
    t=`<body><p>hi</p></body>`
    console.log(x.parser.parse(t))

    """
    # evaljs(s)
    # the response is not easy to manage
    # creating a grammar file


def openOrPrint(x, dir=0, r="index.cjs"):
    with CD(dir):
        if isfile(x):
            ofile(x)
        elif isdir(x):
            files = os.listdir(x)
            target = find(files, r)
            if target:
                ofile(os.path.join(x, target))
            else:
                pprint(files)


def makeEmojis():
    items = read(dldir + "emoji.json").get("emojis")
    store = {}
    # for k,v in items.items():
    # store[k] = v.get('skins')[0].get('native')
    # normWrite('emoji.json', store)
    # https://api.github.com/emojis # has all of the emojis as png files which is different from utf...
    # The above is to parse them out.
    ################################################33

    ################################################
    url = "https://openmoji.org/library"
    ta = TextAnalysis(url, "imgsrc")
    normWrite("svg-emoji.json", ta.results)
    # build the links perhaps
    ################################################


def changeFileName2(file, dir=0, newName=0):
    if not newName: newName = prompt(file, "new name?")
    if not dir: dir = head(file)
    return npath(dir, addExtension(newName, getExtension(file)))


def gfn():
    def dateSearch(s):
        return search("^______+ = " + date, s, flags=re.M)

    return getFunctionNames(
        dateSearch(normRead("class.js"))
    )


def mostRecentDirectoryFiles(key, e="pdf", amount=10):
    v = ff(dirgetter(key), sort=1, e=e)[-amount:]
    os.system("clear")
    pprint(v)
    return v


def openLastGoogleDoc():
    return openBrowser(read("google-doc-file.txt").strip())


def editMathcha(f="", fn=0):
    text = fn(byteRead(f))
    byteWrite(f, text)


def byteRead(file):
    with open(file, "rb") as f:
        return f.read()


def byteWrite(file, value):
    with open(file, "wb") as f:
        f.write(value)
        print("successfully wrote byte file!", file)


def mathchaReplace(s):
    prompt(s)
    dict = {
        #'ab': 'AB',
        #'123': 'ONETWOTHREE',
        #'sdf': 'SDF',
        #'12': 'ONETWO',
        #'abc': 'ABC',
        "QRKQRK": "booper"
    }
    return byteReplace(s, dict, "b")


def byteReplace(s, dict, template="b", flags=0):
    regex = str.encode(ncg(template, dict))
    print(regex)

    def parser(x):
        return str.encode(
            dict.get(x.group(1).decode())
            if x.groups()
            else dict.get(x.group(0).decode())
        )

    return re.sub(regex, parser, s, flags=flags)



def isVeryRecentFile(f):
    return isRecentFile(f, minutes=4000)


def printIt(fn):
    def decorator(*args, **kwargs):
        printIt = kwargs.pop("printIt", None)
        if printIt and isVeryRecentFile(clipfile):
            print("returning very recent file")
            return read(clipfile)
        value = fn(*args, **kwargs)
        if printIt:
            clip(value)
        return value

    return decorator



def mdir(f, t):
    assert isdir(f)
    a, b = re.sub("/ *$", "", f).rsplit("/", maxsplit=1)
    dest = os.path.join(a, t)
    prompt("moving", "from", f, "to", dest)
    shutil.move(f, dest)


def getLastPdf(name=""):
    file = glf(name=name, e="pdf")
    return file



def scrapeOrdering():
    def f(s):
        if s == "x" or not s or s == 0:
            return 0
        return int(s)

    s = map(
        split(
            prompt("fix:order = G9, V2, V1, M2, M1"), " "
        ),
        f,
    )
    return list(reversed(s))


def choosefiles(dir=dldir, key="", groups=3):
    files = choose(
        map(
            sorted(absdir(dir), key=mdate, reverse=True),
            tail,
        )
    )
    pprint(files)
    return files



def mergeFirstPageOfEachFile(files):
    f = lambda x: x.pages[0:1]
    return pdfCreate(files, f)


def printDirRecursive(dir, **kwargs):

    checkpoint = checkpointf(**kwargs)

    def runner(dir):
        store = {}
        children = []
        store["dir"] = dir
        store["children"] = children

        files = absdir(dir)
        for file in files:
            name = tail(file)

            if isIgnoredFile(name):
                continue

            elif isfile(file):
                if checkpoint(file):
                    children.append({"file": name})
            elif isdir(file):
                if is_empty_dir(file):
                    print('is empty dir remove it?')
                    rmdir(file)
                else:
                    children.append(runner(file))
        return store

    return runner(dir)


def recentFileCache(fn):
    def decorator(file, *args, **kwargs):
        reset = kwargs.pop("reset", None)
        value = fn(file, *args, **kwargs)
        recentfile = file + ".recent"
        if not reset and isRecentFile(recentfile, hours=2):
            print("returning recent file")
            return parseJSON(read(recentfile))
        else:
            write(recentfile, value, open=1)
            return value

    return decorator


def choosePDFS():
    files = choose(mostRecentDirectoryFiles(dldir))
    return files


def oncef():
    go = True

    def lamb(arg):
        nonlocal go
        if go and arg:
            go = False
            return True

    return lamb


def infof(f):
    def lamb(file, *args):
        value = f(file, *args)
        return {"file": tail(file), "value": value}

    return lamb


def objectClassName(x):
    s = str(type(x))
    return search("<\w+ '(?:__main__\.|base\.)?(\w+)", s)



class PageStorage:
    def __init__(self):
        self.store = []

    def reset(self, key, value=None):
        self.current = [value] if value != None else []
        self.store.append([key, self.current])

    def add(self, item):
        self.current.append(item)

    def __len__(self):
        return len(self.store)


def mostRecentFileGroups(dir=dldir, minutes=3, reverse=True):
    ignore = ['Grade Reports', 'g4q', 'g5q']

    #storage = PageStorage()
    files = ff(dir, sort=1, reverse=reverse)
    store = []

    ignoreRE = "(Class|home)work|^g[45]"
    lastDate = 0

    for i, file in enumerate(files):
        if getFileName(file) in ignore:
            continue
        date = mdate(file)
        name = tail(file)
        if test(ignoreRE, name):
            continue
        d = delta(date, lastDate)
        limit = toSeconds(minutes=minutes)
        passes = d < limit or lastDate == 0
        dprint(name, d, limit, passes)
        if passes:
            store.append(file)
        else:
            return store

        lastDate = date


def promptOutpath(s=0, fallback="", fn=0):
    out = s or prompt("outpath?") or fallback
    if fn:
        out = fn(out)
    return npath(dldir, out)



def getNodeFile(name):
    files = [
        f"{nodedir}{name}/dist/{name}.js",
        f"{nodedir}{name}/dist/index.js",
    ]
    file = find(files, isfile)
    if file:
        return file
    else:
        prompt(printDirRecursive(nodedir + name))



def versionControl(f, revert=0):
    f = normDirPath(f)
    if not isfile(f):
        return

    original = f
    got = 0

    def increment(f, n=1):
        nonlocal got
        v = f + ".version" + str(n)
        if isfile(v):
            if revert:
                got = v
                return
            return increment(f, n + 1)
        else:
            return v

    newFile = increment(npath(budir, original))
    if got:
        prompt(f"revert {got} to {original} original?")
        backup(original)
        shutil.copy(got, original)
        print("successful reversion!")
    else:
        prompt(f"copy original to {newFile}?")
        shutil.copy(original, newFile)
        print("successful control to budir!")



def pickFiles(dir="dldir"):
    a = prompt(f"choose files. directory = {dir}")
    dir = dirdict.get(dir, None)
    assert dir
    return mapdir(xsplit(a), dir)


def STOP():
    raise Exception("STOP!!!")


def findCssFile():
    files = ff(dldir, css=1, text="mult")



def splitOnWord(s, word):
    if test("\\b" + word + "\\b", s):
        s = getLast(re.split(word + ".*", s))
    return s



def tabular(data):
    store = []
    n = 25
    s = (f"{{: >{n}}}" * len(data[0])).strip()
    for row in data:
        store.append(s.format(*row))
    return join(store)



def foo():
    store = {}
    for a, b, c in partition(re.findall("\S+", clip()), 3):
        store[a] = [b, c]
    clip(oneLine(s))


def oneLine(s):
    s = json.dumps(s, indent=4)
    s = re.sub(r'": \[\s+', '": [', s)
    s = re.sub(r'",\s+', '", ', s)
    s = re.sub(r'"\s+\]', '"]', s)
    return s



def finfo(file):
    text = read(file)
    return {
        "file": tail(file),
        "lines": lineCount(text),
        "size": len(text),
    }


def trackProgress():
    # let text = search(r, lastQuarter(read(file)))
    # let data = getBindingNames(text)
    # let stamp = datestamp(date1) + ' - ' + datestamp(date2)
    # let s = join(stamp, data)
    # console.log(s)
    normAppend("daily-code-progress.log", s)


def moveFilesToDriveTodoDir(dir):
    s = mostRecentFileGroups(dldir, minutes=5)[0][1]
    prompt(s, "move these files?")
    dir = prompt("todo sub directory name?").upper()
    dir = tododir + dir
    mkdir(dir)
    map(s, mfile, dir)


def imageToText(img):
    # sudo apt install tesseract-ocr
    # sudo apt install libtesseract-dev
    # sudo apt install libleptonica-dev pkg-config
    from PIL import Image
    import pytesseract

    return pytesseract.image_to_string(Image.open(img))

    # OR

    # sudo apt install tesseract-ocr
    # sudo apt install libtesseract-dev
    # sudo apt install tesseract-ocr-ita

    # pip install pytesseract
    # pip install opencv

    import cv2
    import argparse
    import os
    import pytesseract
    from PIL import Image

    def extract_text(image):
        im = cv2.imread(image)
        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        ret, thresh1 = cv2.threshold(
            imgray, 180, 255, cv2.THRESH_BINARY
        )
        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, thresh1)
        img = Image.open(filename)
        text = pytesseract.image_to_string(img)
        return text


def strType(x):
    return getLastWord(str(type(x)))



def download(url, name=0):
    if not name:
        name = addExtension(
            prompt(url, "outpath name"), "pdf"
        )
    write(dldir + name, request(url))


def stringInfo(*args):
    items = partition(args)
    s = ""
    for a, b in items:
        s += a + ": " + str(b) + "\n"
    return s.strip()


def backup1206(*files):
    date = datestamp()
    name = "CURRENT"
    dir = budir + name
    files = list(files)
    files.append("/home/kdog3682/VIM/functions.vim")
    files.append("/home/kdog3682/VIM/variables.vim")
    files.append("/home/kdog3682/.vimrc")
    files = unique(files)
    cfiles(files, dir)

    info = stringInfo(
        "date",
        date,
        "directory",
        dir,
        "numFiles",
        len(files),
    )
    payload = join(info, files, linebreak)
    normAppend("files.log", payload)


def scrapeHTML(url):
    s = join(
        map(
            re.findall(
                env.scrapeRef.get("pre"), request(url)
            ),
            liParser,
        )
    )
    normWrite("scrape.html", s)


def scrape(url, key=0):
    prompt(url, key)
    TextAnalysis(url, key)


def prePostParser(items):
    s = filter(items, "^\s*<")
    if len(s):
        return normWrite(
            "scrape.html", chooseIndex(s), open=1
        )
    else:
        print(s)
        print("not done yet")


def chooseIndex(items):
    i = len(items)
    if i == 1:
        return items[0]
    a = prompt(
        f"There are {i} items. Choose 1-based indexes."
    )
    return smallify([items[int(i) - 1] for i in a])


def zipToDir(dir):
    # clip(getfiles(dir, recursive=1))
    # return

    name = dirName(dir)
    r = re.sub("\W", ".*?", name)
    file = glf()

    assert itest(r, file)
    assert getExtension(file) == "zip"

    mkdir(dir)
    unzip(file, dir)

    childDir = absdir(dir)[0]
    files = absdir(childDir)
    for file in files:
        mfile(file, dir)
    rmdir(childDir)
    pprint(os.listdir(dir))



def foo():
    dir = swiftdir
    for item in filter(absdir(dir), isdir):
        files = absdir(item)
        for file in files:
            mfile(file, swiftdir)



def craig():
    from craigslist import CraigslistJobs

    # from craigslist import CraigslistServices
    # print(dir(CraigslistServices))
    # return

    x = CraigslistJobs.show_categories()
    print(x)
    return

    kwargs = {
        "site": "newyork",
    }

    jobs = CraigslistJobs(**kwargs)
    for result in jobs.get_results():
        print(result)


temp = [
    "/home/kdog3682/TEACHING/SAT Grammar Test 4.pdf",
    "/home/kdog3682/TEACHING/SAT Grammar Test 1.pdf",
    "/home/kdog3682/TEACHING/SAT Grammar Test 2.pdf",
    "/home/kdog3682/TEACHING/SAT Grammar Test 3.pdf",
    "/home/kdog3682/TEACHING/SAT Grammar Test 4.json",
    "/home/kdog3682/TEACHING/SAT Grammar Test 3.json",
    "/home/kdog3682/TEACHING/SAT Grammar Test 2.json",
    "/home/kdog3682/TEACHING/SAT Grammar Test 1.json",
]

cwdfolderinfo = [
    "/home/kdog3682/CWD/tempest.json",
    "/home/kdog3682/CWD/animations.js",
    "/home/kdog3682/CWD/service.json",
    "/home/kdog3682/CWD/info.json",
    "/home/kdog3682/CWD/vue-messy.js",
    "/home/kdog3682/CWD/functioninfo.json",
    "/home/kdog3682/CWD/stdlib.css",
    "/home/kdog3682/CWD/h.js",
    "/home/kdog3682/CWD/finderror.js",
    "/home/kdog3682/CWD/html3.js",
    "/home/kdog3682/CWD/node.js",
    "/home/kdog3682/CWD/nerdsolver.js",
    "/home/kdog3682/CWD/tempest.js",
    "/home/kdog3682/CWD/katex-question.js",
    "/home/kdog3682/CWD/v3.js",
    "/home/kdog3682/CWD/index.html",
    "/home/kdog3682/CWD/testfile2.js",
    "/home/kdog3682/CWD/generate_multiple_choice.js",
    "/home/kdog3682/CWD/0.js",
    "/home/kdog3682/CWD/apptest.js",
    "/home/kdog3682/CWD/zola",
    "/home/kdog3682/CWD/pdfo.js",
    "/home/kdog3682/CWD/fshelpers.js",
    "/home/kdog3682/CWD/scratchpad.js",
    "/home/kdog3682/CWD/mathstory.txt",
    "/home/kdog3682/CWD/xcnv.js",
    "/home/kdog3682/CWD/normalize.css",
    "/home/kdog3682/CWD/testfile3.js",
    "/home/kdog3682/CWD/slim.py",
    "/home/kdog3682/CWD/apps.js",
    "/home/kdog3682/CWD/template.html",
    "/home/kdog3682/CWD/tuesday.js",
    "/home/kdog3682/CWD/a4.pdf",
    "/home/kdog3682/CWD/graphcalc.js",
    "/home/kdog3682/CWD/html-parser.js",
    "/home/kdog3682/CWD/am8.txt",
    "/home/kdog3682/CWD/gapp.js",
    "/home/kdog3682/CWD/google-emails.json",
    "/home/kdog3682/CWD/zq.json",
    "/home/kdog3682/CWD/ad.txt",
    "/home/kdog3682/CWD/pdfgen-simulate.js",
    "/home/kdog3682/CWD/html.js",
    "/home/kdog3682/CWD/jsc.js",
    "/home/kdog3682/CWD/tempest.txt",
    "/home/kdog3682/CWD/index.js2",
    "/home/kdog3682/CWD/pdfgen.js",
    "/home/kdog3682/CWD/makepdf.js",
    "/home/kdog3682/CWD/runjspdf.js",
    "/home/kdog3682/CWD/fastmath.js",
    "/home/kdog3682/CWD/app-fastmath.js",
    "/home/kdog3682/CWD/LineEdit.js",
    "/home/kdog3682/CWD/package-lock.json",
    "/home/kdog3682/CWD/r2",
    "/home/kdog3682/CWD/todo.js",
    "/home/kdog3682/CWD/raw.js",
    "/home/kdog3682/CWD/gldl.js",
    "/home/kdog3682/CWD/testfile.js",
    "/home/kdog3682/CWD/node-utils.js",
    "/home/kdog3682/CWD/generate-multiple-choice.js",
    "/home/kdog3682/CWD/tempindex.html",
    "/home/kdog3682/CWD/helperfunctions.js",
    "/home/kdog3682/CWD/t5.js",
    "/home/kdog3682/CWD/nerdcheck.js",
    "/home/kdog3682/CWD/math-helpers.js",
    "/home/kdog3682/CWD/math-utils.js",
    "/home/kdog3682/CWD/puppet.js",
    "/home/kdog3682/CWD/html-helpers.js",
    "/home/kdog3682/CWD/jsa.js",
    "/home/kdog3682/CWD/s.js",
    "/home/kdog3682/CWD/jsconnector.js",
    "/home/kdog3682/CWD/pdfgen-make.js",
    "/home/kdog3682/CWD/pdfgen-run.js",
    "/home/kdog3682/CWD/helpers.js",
    "/home/kdog3682/CWD/testfile4.js",
    "/home/kdog3682/CWD/vue-transform.js",
    "/home/kdog3682/CWD/source.js",
    "/home/kdog3682/CWD/pdfgen-state.js",
    "/home/kdog3682/CWD/nodehelpers.js",
]

def undo(dir=trashdir):
    mfiles(ff(dir, minutes=10)[-8:], teachdir)


temp = [
    # "/home/kdog3682/CWF/history_data.csv",
    "/home/kdog3682/CWF/snip.vim",
    "/home/kdog3682/CWF/Session.vim",
    "/home/kdog3682/CWF/trash",
    "/home/kdog3682/CWF/run.sh",
    "/home/kdog3682/CWF/storage.py",
    "/home/kdog3682/CWF/vim-comments.vim",
    "/home/kdog3682/CWF/transfer.sh",
    "/home/kdog3682/CWF/passwords.csv",
    "/home/kdog3682/CWF/macbash.sh",
    "/home/kdog3682/CWF/vim-data.vim",
    # "/home/kdog3682/CWF/cmparser.js",
    # "/home/kdog3682/CWF/cmgen.js",
    "/home/kdog3682/CWF/setup2.sh",
    "/home/kdog3682/CWF/Symbola.otf",
    "/home/kdog3682/CWF/index.js2",
    # "/home/kdog3682/CWF/percents.html",
    "/home/kdog3682/CWF/setup.sh",
    # "/home/kdog3682/CWF/intel.py",
    # "/home/kdog3682/CWF/temp.py",
    # "/home/kdog3682/CWF/g24.py",
    "/home/kdog3682/CWF/utils.py",
    "/home/kdog3682/CWF/helpers.py",
    # "/home/kdog3682/CWF/pike.py",
    "/home/kdog3682/CWF/zipscript.py",
    "/home/kdog3682/CWF/githubscript.py",
    "/home/kdog3682/CWF/voskscript.py",
    "/home/kdog3682/CWF/ga.py",
    "/home/kdog3682/CWF/redditscript.py",
    "/home/kdog3682/CWF/env.py",
    "/home/kdog3682/CWF/iab.vim",
    "/home/kdog3682/CWF/run.py",
    "/home/kdog3682/CWF/helpers2.js",
    "/home/kdog3682/CWF/temp.js.txt",
    "/home/kdog3682/CWF/pdf.py",
    "/home/kdog3682/CWF/apps.py",
    "/home/kdog3682/CWF/pdfservice.py",
    "/home/kdog3682/CWF/.clip.js",
    "/home/kdog3682/CWF/pug.html",
    "/home/kdog3682/CWF/index.html",
    "/home/kdog3682/CWF/a.js",
    "/home/kdog3682/CWF/r7.css",
    "/home/kdog3682/CWF/a.py",
    "/home/kdog3682/CWF/variables.vim",
    "/home/kdog3682/CWF/dicts.vim",
    "/home/kdog3682/CWF/vim-dictionaries.vim",
    "/home/kdog3682/CWF/bkl.py",
    "/home/kdog3682/CWF/base.py",
]

def mover(extensions, dir):
    inpath = pydir
    c = checkpointf(
        extensions=xsplit(extensions), deleteIt=1
    )
    files = filter(absdir(inpath), c)
    dir = rootdir + dir.upper()
    mkdir(dir)
    mfiles(files, dir)


def removeCache():
    rmdir(pydir + "__pycache__", force=1)



temp = [
    # "/home/kdog3682/CWD/tempest.json",
    # "/home/kdog3682/CWD/animations.js",
    # "/home/kdog3682/CWD/service.json",
    "/home/kdog3682/CWD/info.json",
    "/home/kdog3682/CWD/vue-messy.js",
    "/home/kdog3682/CWD/functioninfo.json",
    "/home/kdog3682/CWD/stdlib.css",
    # "/home/kdog3682/CWD/h.js",
    # "/home/kdog3682/CWD/finderror.js",
    # "/home/kdog3682/CWD/html3.js",
    # "/home/kdog3682/CWD/node.js",
    "/home/kdog3682/CWD/nerdsolver.js",
    "/home/kdog3682/CWD/tempest.js",
    "/home/kdog3682/CWD/katex-question.js",
    "/home/kdog3682/CWD/v3.js",
    "/home/kdog3682/CWD/index.html",
    "/home/kdog3682/CWD/testfile2.js",
    "/home/kdog3682/CWD/generate_multiple_choice.js",
    "/home/kdog3682/CWD/0.js",
    "/home/kdog3682/CWD/apptest.js",
    "/home/kdog3682/CWD/zola",
    "/home/kdog3682/CWD/pdfo.js",
    "/home/kdog3682/CWD/fshelpers.js",
    "/home/kdog3682/CWD/scratchpad.js",
    "/home/kdog3682/CWD/mathstory.txt",
    "/home/kdog3682/CWD/xcnv.js",
    "/home/kdog3682/CWD/normalize.css",
    "/home/kdog3682/CWD/testfile3.js",
    "/home/kdog3682/CWD/slim.py",
    "/home/kdog3682/CWD/apps.js",
    "/home/kdog3682/CWD/template.html",
    "/home/kdog3682/CWD/tuesday.js",
    "/home/kdog3682/CWD/a4.pdf",
    "/home/kdog3682/CWD/graphcalc.js",
    "/home/kdog3682/CWD/html-parser.js",
    "/home/kdog3682/CWD/am8.txt",
    "/home/kdog3682/CWD/gapp.js",
    "/home/kdog3682/CWD/google-emails.json",
    "/home/kdog3682/CWD/zq.json",
    "/home/kdog3682/CWD/ad.txt",
    "/home/kdog3682/CWD/pdfgen-simulate.js",
    "/home/kdog3682/CWD/html.js",
    "/home/kdog3682/CWD/jsc.js",
    "/home/kdog3682/CWD/tempest.txt",
    "/home/kdog3682/CWD/index.js2",
    "/home/kdog3682/CWD/pdfgen.js",
    "/home/kdog3682/CWD/makepdf.js",
    "/home/kdog3682/CWD/runjspdf.js",
    "/home/kdog3682/CWD/fastmath.js",
    "/home/kdog3682/CWD/app-fastmath.js",
    "/home/kdog3682/CWD/LineEdit.js",
    "/home/kdog3682/CWD/package-lock.json",
    "/home/kdog3682/CWD/r2",
    "/home/kdog3682/CWD/todo.js",
    "/home/kdog3682/CWD/raw.js",
    "/home/kdog3682/CWD/gldl.js",
    "/home/kdog3682/CWD/testfile.js",
    "/home/kdog3682/CWD/node-utils.js",
    "/home/kdog3682/CWD/generate-multiple-choice.js",
    "/home/kdog3682/CWD/tempindex.html",
    "/home/kdog3682/CWD/helperfunctions.js",
    "/home/kdog3682/CWD/t5.js",
    "/home/kdog3682/CWD/nerdcheck.js",
    "/home/kdog3682/CWD/math-helpers.js",
    "/home/kdog3682/CWD/math-utils.js",
    "/home/kdog3682/CWD/puppet.js",
    "/home/kdog3682/CWD/html-helpers.js",
    "/home/kdog3682/CWD/jsa.js",
    "/home/kdog3682/CWD/s.js",
    "/home/kdog3682/CWD/jsconnector.js",
    "/home/kdog3682/CWD/pdfgen-make.js",
    "/home/kdog3682/CWD/pdfgen-run.js",
    "/home/kdog3682/CWD/helpers.js",
    "/home/kdog3682/CWD/testfile4.js",
    "/home/kdog3682/CWD/vue-transform.js",
    "/home/kdog3682/CWD/source.js",
    "/home/kdog3682/CWD/pdfgen-state.js",
    "/home/kdog3682/CWD/nodehelpers.js",
]

def backupDirectories(directories):
    import shutil

    mkdir(budir + datestamp())
    for dir in toArray(directories):
        outpath = os.path.join(
            budir, datestamp(), dirName(dir)
        )
        print("making zip directory", dir)
        shutil.make_archive(outpath, "zip", dir)


def zipCheck(outpath=0, file=0):
    # outpath = budir / datestamp / SERVER.zip / myFile.js
    # pprint(zipCheck(s, file='token.json'))

    import zipfile
    import io

    with zipfile.ZipFile(outpath, "r") as z:
        if file:
            file = z.open(file)
            with io.TextIOWrapper(
                file, encoding="utf-8"
            ) as f:
                return parseJSON(f.read())
        else:
            return map(z.filelist, lambda x: x.filename)



def testsuite(items):
    return map(items, lambda x: [x, eval(x)])



def choosepdf():
    ofile(choose(mostRecent(dldir, 10, reverse=1)))


def seeRecent():
    e = prompt("extension?")
    kwargs = dict({"dir": dirdict.get(e), e: True})
    ff(**kwargs)



def create_pdfdict_from_pdf_files():
    files = ff(pdfdir, name="^G\d|math")
    d = {
        n2char(i) + n2char(i): f
        for i, f in enumerate(files)
    }
    appendVariable(d, outpath="pdf.py", name="pdfdict")



def move_last_file_and_name_it():
    file = glf()
    out = normFileToDir(file)
    prompt("is this the correct outpath?", out)
    mfile(file, out)


def promptSplit(*args):
    r = "\||\.\.|\\\\|  +"
    a = prompt(*args)
    return re.split(r, a.strip())



def saveToDrive(file):
    cfile(file, tempbudir)



def emptyTrash(dir=trashdir):
    prompt(os.listdir(trashdir))
    assert isdir(dir)
    rmdir(dir, force=1)
    mkdir(dir)
    printdir(dir)


def keepOrDelete(file):
    a = prompt(file)
    if a == "d":
        rfile(file)
    elif a == "k":
        e = getExtension(file)
        if e == "zip":
            unzip(file, to=unzipdir)



def cleanupRawText(s):
    def f(x):
        n = x.group(0)
        if n == "”":
            return '"'
        if n == "“":
            return '"'
        if n == "’":
            return "'"
        raise Exception(x)

    s = re.sub("\t| {2,}", " ", s)
    s = re.sub("[”’“]", f, s)
    return s.strip()


def normMove(src, to):
    outpath = dirFromFile(to) + tail(to)
    mfile(src, outpath)



def backupMostPopular():
    files = [
        "/home/kdog3682/CWF/public/class.js",
        "/home/kdog3682/PYTHON/pdf.py",
        "/home/kdog3682/VIM/functions.vim",
        "/home/kdog3682/VIM/variables.vim",
        "/home/kdog3682/CWF/public/print.js",
    ]
    cfiles(files, bucurdir)


def fixWrongPaths():
    baseFiles = map(files, lambda x: normpath(drivedir, x))
    for i, baseFile in enumerate(baseFiles):
        file = files[i]
        outpath = normpath(bucurdir, baseFile)
        cfile(baseFile, outpath)
        mfile(baseFile, file)



def writeGitIgnore(dir2023):
    s = """
        *.zip
        *.7z
        *.rar
        *.tar.gz
        *.pdf
        .DS_Store
        node_modules
        __pycache__

    """
    write(dir + ".gitignore", smartDedent(s), open=1)



def gitRemote(repo, username="kdog3682", message=0):
    chdir(rootdir + repo)
    if not isdir(".git"):
        response = SystemCommand("git init")

    # for changing from master to main
    s = "git branch -m master main"
    s = "git push -u origin main"
    s = "git push origin --delete master"
    #############################

    # s = 'git diff --name-only --cached'
    # s = 'git status'
    # s = 'git diff --names-only'
    # s = 'git diff --staged'
    # s = 'git add .'
    # response = SystemCommand(s)
    # return
    # s = 'git log'
    # s = 'git push -u origin main'
    # s = 'git remote -v'
    # s = 'ssh -vvv git@github.com'
    # it creates a prompt which may ask something

    mainCommand = f"git add .\ngit commit -a -m \"{message or 'pythonTest'}\"\ngit push"
    response = SystemCommand(mainCommand)

    if response.error == "sdfgsdfg":

        url = f"git@github.com:{username}/{repo}.git"
        s = f"git remote add origin {url}"
        response = SystemCommand(s)

        if response.error == "remote origin already exists":
            s = f"git remote set-url origin {url}"
            response = SystemCommand(s)

    elif response.error == "sdfgsdfg":
        prompt("Creating ssh key gen, press Y for Yes")
        s = 'ssh-keygen -t rsa -C "kdog3682@gmail.com"'
        response = SystemCommand(s)
        ofile(sshfile)
        prompt("copy the opened file to github")
        response = SystemCommand(mainCommand)

    return


def changelog(s=0, mode="add"):
    changelogfile = "/home/kdog3682/2023/changelog.md"
    if not s:
        s = hms()
    payload = "+ " + s
    append(changelogfile, payload)


def writeNpmInit(name):

    data = {
        "name": name,
        "version": "1.0.0",
        "type": "module",
        "description": "",
        "main": "index.js",
        "scripts": {
            "test": 'echo "Error: no test specified" && exit 1'
        },
        "repository": {
            "type": "git",
            "url": f"git+https://github.com/kdog3682/{name}.git",
        },
        "author": "Kevin Lee",
        "license": "ISC",
        "homepage": "https://github.com/kdog3682/2023#changelog",
    }
    write(outpath, data)


def gitUrl(file, repo, user="kdog3682"):
    url = "https://raw.githubusercontent.com/$1/$2/main/$3"
    url = templater(url, [user, repo, file])
    print(url)
    return url



def npmInstall(s):
    dev = test("cors|nodemon|jest|grunt|uglify", s, flags=re.I)
    SystemCommand(
        "npm i " + s + (" --save-dev" if dev else "")
    )



def foo():
    a = linegetter(text(), fn="(^[a-z]\w+)\(", u=1)
    b = linegetter(text(), fn="^[A-Z][a-zA-Z]+$", u=1)
    data = {
        "builtInFunctions": a,
        "builtInClasses": b,
    }


def normClear(file):
    file = normDirPath(file)
    print(file)
    clear(file)



def publishScratchpad():
    with CD(dir2023):
        outpath = addExtension(
            prompt(
                "publishing scratchpad. choose outpath file name: "
            ),
            "js",
        )
        mfile("scratchpad.js", outpath)


def getLinks(folders, q):
    store = []
    for path in toArray(folders):
        matches = ff(path, name=q)
        if matches:
            store.extend(matches)

    files = choose(store)
    map(files, revert, dir=jsdir, increment=1, vim=1)


def appendVim(type, arg):
    b = arg
    s = removeExtension(tail(b))
    a = abrev(s)
    s = f'let g:{type}["{a}"] = "{b}"'
    append("/home/kdog3682/.vimrc", s)



def scrapeLinks(source=0):
    #write('request.temp.txt', request('https://www.nysedregents.org/ei/ei-math.html'))
    #return
    source = "https://www.nysedregents.org/ei/"
    #srequest(source)
    items = filter(
        re.findall(
            env.scrapeRef.get("href"),
            read("/home/kdog3682/2023/request.temp.txt"),
        ),
        "released-items",
    )
    items = choose(items)
    items = fixUrls(source, items)

    def downloader(url):
        #m = search("g\d", url)
        #name = f"{m}cw.pdf"
        name = tail(url)
        return downloadPDF(url, name)

    return map(items, downloader)


def tagdir(dir, history={}):
    items = {}
    store = {"dir": dir, "items": items}
    files = absdir(dir)
    aliases = {
        ".": "private",
        "l": "library",
        "d": "delete",
        "m": "main",
        "i": "ignore",
    }
    for file in files:
        name = tail(file)
        value = history.get(name)
        if value == None:
            a = prompt(fileInfo(file))
            value = history.get(a, a)

        items[name] = value
    appendVariable(store)


tagdirdict = {
    "dir": "/home/kdog3682/2023/",
    "date": "01-11-2023",
    "items": {
        ".git": "private",
        "changelog.md": "",
        "node_modules": "private",
        "package.json": "private",
        "javascript.master.json": "private",
        "package-lock.json": "private",
        "unit-tests.js": "?",
        "ParserConfigs.js": "?",
        "Lezer.js": "main",
        "Interactive.js": "main",
        "regex-utils.js": "not working",
        "notes.txt": "",
        "CSSObject.js": "main",
        "mathgen.js": "main",
        "DateObject.js": "main",
        "scratchpad.js": "delete",
        "request.temp.txt": "i",
        "clip.js": "i",
        "math.txt": "",
        "scratchpad.txt": "",
        "App.js": "main",
        "comments.js": "",
        "StateContext.js": "delete",
        "parser-factories.js": "main",
        "color-utils.js": "delete",
        "css-utils.js": "main",
        "OX3HTML.js": "main",
        "LineEdit.js": "main",
        "asdf.js": "delete",
        "1673385274916.png": "delete",
        ".gitignore": "private",
        "screenshot.png": "i",
        "test.pdf": "i",
        "Prettier.js": "main-done",
        "vue.esm.browser.min.js": "library",
        "CodeOrganizer.js": "main",
        "node-utils.js": "main",
        "Puppeteer.js": "main",
        "variables.js": "main",
        "server.js": "main",
        "main.js": "main-done",
        "index.html": "main",
        "browser-utils.js": "main",
        "utils.js": "main",
        "HTMLBuilder.js": "main",
        "base-components.js": "main",
        "katex.min.js": "library",
        "katex.min.css": "library",
    },
}

def npmResetNode():

    s = """
        npm install -g npm stable
        npm install -g node or npm install -g n
        node --version or node -v
    """

    SystemCommand(
        """
        npm cache clean -f
        npm install -g n
        n stable
        npm version
    """
    )


def readjs(*args):
    dir = jsdir

    def runner(s):
        file = dir + addExtension(s, "js")
        if isfile(file):
            return file

    return filter(map(args, runner))



def uploadDirectoryToExcel(dir='dldir'):
    files = absdir(dirdict[dir])
    data = map(files, finfo)

    googleAction({
        'clear': 1,
        'type': 'gse',
        'data': data,
        'alignLeft': 1,
        'headers': 'name date size comments',
        'open': 1,
        'key': dir,
    })


def resumeIt():
    renameLastFile('Kevin Lee Resume')
    


def downloadDirectoryFromExcel(dir):
    data = googleAction({
        'type': 'gse',
        'get': 1,
        'key': dir,
    })


def makeRootDir(s):
    mkdir(rootdir + s.upper())


def antichoose(items):
    a = prompt2(items)
    indexes = [int(n) - 1 for n in a.strip().split(" ")]

    store = []
    for i, item in enumerate(items):
        if i not in indexes:
            store.append(item)

    return store


pokemonJsonSample = [
  {
    "name": "bulbasaur",
    "types": [
      "grass",
      "poison"
    ]
  },
]

def newdir():
    dir = dir2023 + input('new dir name:')
    assert not isdir(dir)
    mkdir(dir)





class Partitioner2:
    def run(self):
        while True:
            done = self.partition()
            if done:
                return unique(list(self.store.values()))

    def __call__(self):
        return self.run()

    def transformRegex(self, s):
        return self.regexPrefix + s + self.regexSuffix
    
    def __init__(self, items):
        self.items = items
        self.store = {}
        self.resetRegex()

    def resetRegex(self):
        self.regexPrefix = '^'
        self.regexSuffix = ''
        self.regexFlags = 0
    
    def partition(self):
        print(numbered(map(self.items, tail)))
        pprint(self.store)
        a = input('')
        if a == '':
            return True

        if a == 'o':
            return ofile(list(self.store.values()))

        if a == 'd':
            self.store = {}
            return 

        if a == 'reset':
            return self.resetRegex()

        if a == 'pdf':
            items = ff(self.items, pdf=1)
            return self.setItems(items)

        m = search('^(\w*) *= *(.+)', a)
        if m:
            key, val = m
            if key == 'flags' or key == 'f' or key == '':
                if 'b' in val:
                    self.regexSuffix = '\\b'
                if 'B' in val:
                    self.regexSuffix = ''
                if 'S' in val:
                    self.regexPrefix = ''

                if 's' in val:
                    self.regexPrefix = '^'
                if 'i' in val:
                    self.regexFlags -= re.I
                if 'I' in val:
                    self.regexFlags += re.I

        m = search('^o *(\d+)', a)
        if m:
            return ofile(self.items[int(m[0]) - 1])

        m = search('^rn *(\d+) *(.+)', a)
        if m:
            old = self.store[int(m[0]) - 1]
            self.store[int(m[0]) - 1] = changeFileName2(old, newName=m[1])
            return 

        m = search('^d *(.+)', a)
        if m:
            indexes = rangeFromString(m)
            return self.deleteItems(indexes)

        if test('^\d', a):
            indexes = rangeFromString(a)
            self.setItems(indexes)
        else:
            r = self.transformRegex(a)
            items = filter(self.items, lambda x: test(r, tail(str(x)), flags=self.regexFlags))
            self.setItems(items)

    def setItems(self, items):
        for item in items:
            index = len(self.store) + 1
            if isNumber(item):
                item = self.items[item]
            self.store[index] = item
        

    def deleteItems(self, items):
        for item in items:
            if isNumber(item):
                self.store.pop(item + 1)
        


def watchMovie():
    s = prompt('movie name from 123movies?').replace(' ', '+')
    f = f"https://ww1.123moviesfree.net/search-query2/?q={s}"
    ofile(f)



def renameLocalClipFile(a=0):
    name = a or prompt('new name for clip file?')
    mfile('clip.js', addExtension(name, 'js'))

def revertFromTrash():
    file = glf(trashdir)
    ofile(file)
    print(file)
    mfile(file, dldir)

def makeGitIgnore():
    s = """
        */*
        .*
        env.js
        env.py
        env*
    """
    write(".gitignore", smartDedent(s))



def grabGitFiles():
    files = ['codemirror.js', 'codemirror.css', 'cm.js', 'cm.css']
    base = 'https://github.com/kdog3682/codemirror/blob/main/'
    files = map(files, lambda x: npath(base, x))
    map(files, getGithubFile)


def getGithubFile(a):
    def githubUrlToUserContent(s):
        return s.replace("blob/", "").replace(
            "github.com", "raw.githubusercontent.com"
        )

    a = githubUrlToUserContent(a)
    name = tail(a)
    s = request(a)
    if not s:
        dprint(name)
    write(name, s, open=1)


def gitInit(dir=0, user=env.user):
    if not dir:
        #dir = prompt('make a dir inside of dir2023')
        dir = 'code-editor'
        if not isdir(dir):
            dir = npath(dir2023, dir)
            #mkdir(dir)
            #makeGitIgnore()

        #chdir(dir)
        #grabGitFiles()

    assert isdir(dir)
    repo = tail(dir)
    chdir(dir)
    from githubscript import Github
    Github(key=user, repo=repo)

    command = f"""
        git init
        git add .
        git commit -m "push everything"
        git remote add origin git@github.com:{user}/{repo}
        git push -u origin master 
    """

    res = SystemCommand(command, dir=dir)
    if res.success:
        ofile(f"https://github.com/{user}/{repo}")


def resetGit():
    cmd = """
        git rm -r --cached .;
        git add .;
        git commit -m "Untracked files issue resolved to fix .gitignore";
        git push;
        # holy shit this was scary.
        # I thought it deleted everything, but it didnt.
        # Thank goodness. It merely clears everything out.
    """
    SystemCommand(md)


def readLastReversion():
    f = glf(budir)
    print(fileInfo(f))


def isf(f):
    extensions = ['json', 'pdf']
    for e in extensions:
        name = addExtension(f, e)
        dirs = [dldir, dirFromFile(name)]
        for dir in dirs:
            path = npath(dir, name)
            if isfile(path):
                ofile(path)
                return path


def normMove(file):
    mfile(normDirPath(file), currentdir)
    

def mclean(file):
    r = f"^{jspy(file, '//')} *(.*)\n*"

    def runner(s):
       s, items = mget(r, s, flags=re.M, mode=list)
       if not items:
           return 

       logger(items=items, file=file)
       return s

    rpw(smart_path(file), runner)







def pipInstall(s):
    cmd = 'abc ' + s
    print(cmd)


def gitUrl(dir):
    repo = tail(dir)
    return f"https://github.com/{env.githubUser}/{repo}"


def createdir(dir, files, mode='copy'):
   name = dir
   if isdir(dir):
       name = os.path.join(dir, datestamp())
   mkdir(name) 
   if mode == 'move':
        map(files, mfile, name)
   elif mode == 'move':
        map(files, cfile, name)
   printdir(name)




def renameColoringFilesInDir():
    #data = map(absdir(colordir + datestamp()), lambda x: mfile(x, re.sub(' colo.+?(?=\.pdf)', '', x, flags=re.I)))
    printdir(colordir + datestamp())












def snapshotOfDirectory(dir=dldir, amount=10):
   os.chdir(dir)
   items = sorted(os.listdir(dir), key=mdate, reverse=True)[0:amount]
   return numbered(items, title='FILES IN: ' + dir)


def splitInHalf(items):
    import math
    halfPoint = math.floor(len(items) / 2)
    return items[0:halfPoint], items[halfPoint:]






def deprecateFile(file):
    newFile = changeExtension(file, 'deprecated.' + getExtension(file))
    prompt(file, newFile)
    mfile(file, newFile)


def ffApp(s):
    ff(**createKwargs(s))



def JavascriptAppCommand(key, arg='', **kwargs):
    result = SystemCommand('node', 'App.js', key, arg, **kwargs, python=True)
    if not result:
        return 
    if not result.success:
        pprint('error')
        return 

    delimiter = '::CLEARING::'
    s = re.split(delimiter, result.success, maxsplit=1)[1]
    data = parseJSON(s)
    return data


def choose2(items, display=0, anti=0):
    if isObject(items[0]) and not display:
        if items[0].get('title'): display = lambda x: x.get('title')
        elif items[0].get('foo'): display = lambda x: x.get('foo')
        elif items[0].get('subject'): display = lambda x: x.get('subject')

    if anti:
        pprint('choosing which items to keep. The rest will be deleted')
    presentation = map(items, display) if display else items
    print(numbered(presentation))
    indexes = rangeFromString(input())
    if anti:
        store = [el for i, el in enumerate(items) if i not in indexes]
    else:
        store = [el for i, el in enumerate(items) if i in indexes]
    prompt(store)
    return store
        

def getLoggerData(key, childKeys=0, fallback=None):
    data = read(glogfile)
    f = lambda x: x.get('key') == key or x.get('action') == key
    data = filter(data, f)

    if not childKeys:
        return data
    return data
    #for childKey in childKeys:
    #for item in data:
        #f
    #if isArray(fallback):
        #storeType = list
    #for i


    return data


def readRaw(file):
    with open(file, 'r') as f:
        return f.read()


def seeClipKeys():
    s = readRaw('clip.js')
    keys = ['staticClass', 'component']
    r = reWrap(keys, '(?:$1)": "(.*?)"')
    data = unique(re.findall(r, s))
    pprint(data)
    return data










class StepwisePartition:

    def run(self, items):
        assert items
        self.stack = [items]
        while True:
            done = self.prompt()
            if done:
                return unique(self.last)

    @property
    def last(self):
        return getLast(self.stack)

    def prompt(self):
        print(numbered(map(self.last, tail)))
        a = input('')

        if a == '':
            return True

        if a == 'o':
            ofile(self.last)
            return 

        if a == 'd':
            self.stack.pop()
            return 

        if a == 'reset':
            self.resetRegex()
            return 

        if a == 'pdf':
            newItems = ff(self.items, pdf=1)
            self.stack.append(newItems)
            return 

        m = search('^(\w*) *= *(.+)', a)
        if m:
            key, val = m
            if key == 'flags' or key == 'f' or key == '':
                if 'b' in val:
                    self.regexSuffix = '\\b'
                if 'B' in val:
                    self.regexSuffix = ''
                if 'S' in val:
                    self.regexPrefix = ''

                if 's' in val:
                    self.regexPrefix = '^'
                if 'i' in val:
                    self.regexFlags -= re.I
                if 'I' in val:
                    self.regexFlags += re.I

                print("setting flags", self.regexFlags)
            return 

        m = search('^o *(.+)', a)
        if m:
            indexes = rangeFromString(m)
            newItems = [item for i, item in enumerate(self.last) if i in indexes]
            prompt(newItems)
            ofile(newItems)

        m = search('^d *(.+)', a)
        if m:
            indexes = rangeFromString(m)
            newItems = [item for i, item in enumerate(self.last) if i not in indexes]
            self.stack.append(newItems)
            return 

        if test('^\d', a):
            indexes = rangeFromString(a)
            newItems = [item for i, item in enumerate(self.last) if i in indexes]
            self.stack.append(newItems)
            return 

        r = self.transformRegex(a)
        f = lambda x: test(r, tail(str(x)), flags=self.regexFlags)
        newItems = filter(self.last, f)
        if newItems: self.stack.append(newItems)

    def transformRegex(self, s):
        return self.regexPrefix + s + self.regexSuffix
    
    def __init__(self):
        self.resetRegex()

    def resetRegex(self):
        self.regexPrefix = '^'
        self.regexSuffix = ''
        self.regexFlags = 0
    

def partitionMove(dir, to=0, action='move'):
    files = StepwisePartition().run(absdir(dir))
    prompt(files, action=action, message='please confirm')
    if action == 'move':
        mfiles(files, to)
    elif action == 'delete':
        map(files, rfile)



def textlog(**kwargs):
    store = []
    store.append(('date', datestamp()))
    store.append(('getCaller', getCaller()))
    for k,v in kwargs.items():
        store.append((k, v))
    
    s = ''
    for a,b in store:
        if not b:
            continue
        s += a + ': '
        if isArray(b):
            s += '\n' + indent(b) + '\n'
        else:
            s += b 

        s += '\n'

    value = s + linebreak + '\n'
    if s.strip():
        append('log.txt', value)


def WorkSummary(file):
    if getExtension(file) != 'js':
        pprint('only js for worksummary')
        return 

    textlog(
        file=file,
        work=getBindingNames(read(file))
    )


def saveMathFileByFolder(file, gradeLevel=4):
    date = upcomingDate('saturday', strife='-')
    dir = mathdir + date
    f = lambda x: f"G{gradeLevel} {capitalize(x)}"
    originalPath = addExtension(file, 'txt')
    path = npath(dir, changeFileName(originalPath, f))

    def getPath(path):
        if isfile(path):
            if gradeLevel == 4:
                path = path.replace('G4', 'G5')
            else:
                path = path.replace('G5', 'G4')

            if isfile(path):
                return 
            else:
                return path
        else:
            return path

    path = getPath(path)
    assert path
    message = "Do you want to move this file to the mathdir? It will delete the original file"
    prompt(read(originalPath), message=message, outpath=path)


    if not isdir(dir):
        os.makedirs(dir)

    mfile(originalPath, path)






def promptRenameFile(file):
    t = tail(file)
    a, b = re.split(' *\| *', prompt(t), maxsplit=1)
    newFile = file.replace(t, t.replace(a, b))
    mfile(file, newFile)








def getMathDir(next=0):
    dir = mathdir + upcomingDate('saturday', strife='-', next=next)
    assert isdir(dir)
    return dir


def usb(x=0):

    dir = get_usb_dir()

    f = glf(dir=dir2023)
    if tail(f) == 'clip.html' and isRecent(f, minutes=5):
        cfile(f, dir)
        return 

    dir = os.path.join(dir, str(getYearNumber()))
    mkdir(dir)

    files = x or ff(dir2023, hours=10, js=1)
    map(files, cfile, dir)



def saveToSandisk(x=2):
    if not isdir(sandir):
        raise Exception('')
    outdir = os.path.join(sandir, datestamp())
    if isdir(outdir):
        raise Exception('outdir already exists')
    mkdir(outdir)

    if isdir(x):
        copydir(dir, outdir)
    else:
        if isNumber(x):
            x = ff(dir2023, days=2) + ff(pydir, days=2)

        prompt(x, 'save to outdir?', outdir=outdir)
        map(x, cfile, outdir)








temp = [
    "/home/kdog3682/2023/positive-statements.school.txt",
    "/home/kdog3682/2023/classwork.school.txt",
    "/home/kdog3682/2023/comments.school.txt"
]

def writeFiles(*args):
    def runner(arg):
        write(addExtension(arg, 'js'), sayhi(arg))
    map(args, runner)










temp = [
    #"/home/kdog3682/2023/changelog.md",
    #"/home/kdog3682/2023/javascript.dependencies.json",
    #"/home/kdog3682/2023/scratchpad.js",
    #"/home/kdog3682/2023/comments.school.txt",

    "/home/kdog3682/2023/dialogue.js",
    "/home/kdog3682/2023/utils.js",
    "/home/kdog3682/2023/textEdit.js",
    "/home/kdog3682/2023/codeOrganizer.js",
    "/home/kdog3682/2023/compileRE.js",
    "/home/kdog3682/2023/consumableParse.js",
    "/home/kdog3682/2023/dialogue.txt",
    "/home/kdog3682/2023/hammyDialogue.js",
]

def nameAndDate(file):
    name = tail(file)
    date = datestamp(file)
    return [date, name]







def fa(s, r, flags=0, fn=0):
    s = textgetter(s)
    m = re.findall(r, s, flags=flags)
    if fn:
        map(m, fn)
    else:
        pprint(m)


def file_table_cleanup():

    def filetablefn(file, notes):
        r = 'dep|del'
        if not isfile(file):
            print("'not a file'", file)
            return 
        try:
            if test(r, notes) or fsize(file) < 50:
                print('removing', tail(file))
                rfile(file)
        except Exception as e:
            print(e, file)
        

    fa('file-table.txt', '2023 +(\S+)(.*)', fn=filetablefn)







def publish(name):
    dir = publishdir
    inpath = addExtension(name, 'txt')
    outpath = npath(dir, inpath + '.' + saturdate())
    shutil.copy(inpath, outpath)
    clear(inpath)
    printdir(dir)





def openFirstFile(dir):
    ofile(absdir(dir)[0])





    


def addfiles():
    ignoreRE = '''
        component
        scratch
        directive
        state
        config
        ask
        clip
        wrappers
        server
        chalk
        main
        puppeteer
        pretty

        serve
        type
        interactive
        ox3
        hammy
        app

    '''
    ignoreRE = '|'.join(linegetter(ignoreRE))
    return ff(js=1, days=5, sort='date', ignoreRE=ignoreRE, size=2000)





def addTitles():
    def f(item):
        if test('^\w+(?: \w+){1,5} *\n', item):
            title = search('^\w.+', item)
            dprint(title)
            return item
        #if test('^\w+\n\n', item):
            #dprint(title)
            #return item

        else:
            a = prompt(item, 'write a title if you would like:  ')
            if a:
                return a + '\n\n' + item
            return item

    s = read('quiz.txt')
    items = map(split(s, '^---+', flags=re.M), f)
    clip('\n\n---------------------'.join(items))
    #clip(items)
    #s = join(items, '\n\n-------------------')
    #clip(s)






















def downloadImage(url, name, openIt=0):
    from requests import get
    r = get(url)
    if r.status_code == 200:
        with open(name,'wb') as f:
            f.write(r.content)
            if openIt:
                ofile(name)
            print('Image sucessfully Downloaded: ',name)
            return name
    else:
        print('Image Couldn\'t be retreived', name) 








class BeforeAfter:

    def __enter__(self):
        return self
    def __exit__(self, etype, value, traceback):
        if etype:
            print(etype, value)
        else:
            write(self.file, self.parent, open=1)

    def __init__(self, file = 'reddit.json', key = 'mementomoriok'):
        self.file = file
        self.key = key
        self.parent = read(self.file) or {}
        if not key in self.parent:
            self.parent[key] = {}
        self.child = self.parent[key]

        if not 'history' in self.child:
            self.child['history'] = []
        self.history = self.child['history']

    def set(self, k, v):
        if isPrimitive(v):
            self.child[k] = v
        elif isArray(v):
            pass
        else:
            raise Exception('ndy')

    def get(self, k, fallback=None):
        return self.child.get(k, fallback)
    


def archive(inpath=0, outpath=0):
    if not inpath: inpath = 'clip.js'
    if not outpath: 
        outpath = prompt(outpath='need an outpath', inpath=inpath)
    assert outpath

    cfile(inpath, npath(drivedir, outpath))



tempGoogleDocJson = [
    {
        "id": "11PzEB137TPCDX4xr8Hcy3ysJ4FPRwm24jRMhIb7Lb6k",
        "owner": "Kevin Lee",
        "title": "Resume",
        "size": 1478,
        "elapsed": {
            "type": "months",
            "value": 2760
        },
        "date": "01-03-2023",
        "year": 2023
    },
    {
        "id": "17snn0wfBnvGzizd6Ox0ZM_QCq5wJU2ai-L2HX-wuKH4",
        "owner": "Kevin Lee",
        "title": "resume Sunny \u6253\u5370\u8bf4\u660e",
        "size": 931,
        "elapsed": {
            "type": "days",
            "value": 2
        },
        "date": "03-15-2023",
        "year": 2023
    },
    {
        "id": "1COY_z29tbRHH3ZX0pmpmNDn_6UE_KOXRxsIQRcTm1bY",
        "owner": "Kevin Lee",
        "title": "Final Letters Test",
        "size": 9934,
        "elapsed": {
            "type": "minutes",
            "value": 41
        },
        "date": "03-15-2023",
        "year": 2023
    }
]

def makeNodePDF(data = temp, vob_key='resume_toc'):
    fnKey = 'makePDF'
    payload = {'key': vob_key, 'value': data}
    SystemCommand('node', 'App.js', fnKey, payload)


def writejs(s):
    name = prompt('choose a file name')
    name = addExtension(name, 'js')
    if exists(s):
        write(name, s)
        append(self(), comment(abspath(name)))








    









def printDiff(target=''):
    s = SystemCommand(f"git diff --word-diff {target}")
    if target:
        print(s.success)
    else:
        #return print(s.success)
        write('diff.txt', s.success, open=1)



def getNewGitFiles():
    s = SystemCommand('git status --short').success
    r = '^ *\?\?(.+)'
    return re.findall(r, s, flags=re.M)



def parseDiff():
    
    new = getNewGitFiles()
    rfile = '^diff --git a/(.*?) b.*\nindex (\w+)\.\.(\w+)'
    cmd = SystemCommand(f"git diff --word-diff")
    date = datestamp()
    matches = re.split(rfile, cmd.success, flags=re.M)
    items = partition(filter(matches), 4)
    def parse(x):
        a, b, c, d = x
        prefix = "[\[\{][-+]"
        regex = "^\{\+(?:(?:async )?function[!*]?|def|class|const|var) ([\w\$]+)"
        items = re.findall(regex, d, flags=re.M) or []
        if not items:
            return 

        payload = { 'date': date, 'file': a, 'from': b, 'to': c, 'items': items }
        if a in new:
            payload['new'] = True
        return payload

    items = filter([parse(x) for x in items])
    return items

