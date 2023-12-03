from base import *
from next import *
import time
import zipfile


def getZipFiles(inpath, outpath):
    with zipfile.ZipFile(inpath, "r") as z:
        f = lambda x: npath(outpath, x.filename)
        return map(z.filelist, f)

def unzip(inpath, outpath = None, preview = None):
    if not outpath:
        outpath = head(inpath)

    with zipfile.ZipFile(inpath, "r") as z:

        f = lambda x: npath(outpath, x.filename)
        files = map(z.filelist, f)

        if preview:
            prompt3(items = files)

        z.extractall(outpath)
        return files

def readzip(inpath=None, outpath=None, flatten=0):
    if not inpath:
        inpath = choose(absdir(zipdir), mode=1)
    if not outpath:
        outpath = abspath(
            pubdir
            + removeDateStamp(removeExtension(tail(inpath)))
        )

    assert getExtension(inpath) == "zip"
    dprompt(inpath, outpath)

    with zipfile.ZipFile(inpath, "r") as z:
        z.extractall(outpath)

        files = map(z.filelist, lambda x: x.filename)
        pprint(files)
        print("number files extracted", len(files))

        if flatten:
            flatdir(outpath)
        return 1


def usbz(files):
    compression = zipfile.ZIP_DEFLATED
    assert isArray(files)

    name = datestamp() + ".zip"
    dir = get_usb_dir()
    outpath = os.path.join(dir, str(getYearNumber()), name)

    prompt(
        message="starting zip process",
        numOfFiles=len(files),
        outpath=outpath,
        proceed="proceed?",
    )

    with zipfile.ZipFile(outpath, "w") as z:

        for file in files:
            if not isfile(file):
                print("not a file", file)
                continue
            if fsize(file) < 100:
                print("too small", file)
                continue

            name = tail(file)
            z.write(
                file, arcname=name, compress_type=compression
            )


def writezip(
    x, outpath=zipdir, name="backup", date=1, delete=0
):

    if not x:
        return print("empty x", x)

    if isArray(x):
        if not name:
            name = tail(head(abspath(x[0])))
        files = x
    elif isdir(x):
        if not name:
            name = tail(x)
        files = absdir(x)

    removeFiles(files, small=1)

    name = name.upper()
    if date:
        date = "-" + datestamp(str)
    else:
        date = ""
    name = os.path.join(outpath, name + date)
    outpath = addExtension(name, "zip")
    files.sort(key=mdate)

    prompt(
        {
            "files": files,
            "file count": len(files),
            "outpath": outpath,
            "dir": dir,
        },
        "proceed to write? (ctrl + c to cancel)",
    )

    zipWriteAll(outpath, files)

    if delete:
        dest = "zip-files.log.txt"
        deleteFiles(files, save=dest, title=outpath)

    print("success!\nWrote files to", outpath)


def zipWriteAll(outpath, files):
    errors = []
    with zipfile.ZipFile(outpath, "w") as z:
        for file in files:
            if zipWrite(z, file):
                errors.append(tail(file))
        if len(errors) > 10:
            clip(errors)
            raise Exception("to many errors")


def zipWrite(z, f):
    if not f:
        return 1
    try:
        name = re.sub("^\.", "", tail(f))
        compression = zipfile.ZIP_DEFLATED
        z.write(f, arcname=name, compress_type=compression)
        return 0
    except Exception as e:
        print(f, " -- ", "ERROR:", str(e))
        return 1

def zip(files, outpath):
    compress_type = zipfile.ZIP_DEFLATED
    with zipfile.ZipFile(outpath, "w") as z:
        for file in files:
            name = tail(file)
            z.write(file, arcname=name, compress_type=compress_type)


def backup(key):

    if isObject(key):
        chdir(pubdir)
        files = list(key.keys())
        return writezip(
            files, name="oldjs", date=1, delete=1
        )

    if isdir(key):
        files = absdir(key)
        return writezip(files, name=tail(key))

    if key == "js":
        files = ff("js")
        return writezip(files, name="javascript")

    if key == "test":
        files = ["v.js"]
        return writezip(files, name="test", delete=1)

    if key == "oldpy":
        files = ff("cwf py old")
        return writezip(files, name="oldpy", delete=1)

    if key == "oldjs":
        files = ff("pub js old")
        return writezip(files, name="oldjs", delete=1)

    if key == "recent":
        files = recentFiles()
        return writezip(files, name="recent")

    e = getExtension(key)

    if e == "html":
        files = getFileDependencies(key)
        return writezip(files, name=key)


def fixZipAccident():
    raise Exception("need to fix file path here")
    f = "/home/kdog3682/zip-files.log.txt"
    files = re.findall("file: (\S+)", read(f))
    files = map(files, lambda f: normpath(trashdir, f))
    files = filter(files, isfile)
    chdir(pubdir)
    files = key
    return writezip(files, name="oldjs")


def unzipSpecificFile(s):
    inpath = drivedir + "ZIP/JSONS-09-21-2022.zip"
    with zipfile.ZipFile(inpath, "r") as z:
        z.extract("known.json", path=dldir)




files = [
    "/home/kdog3682/PRODUCTIONS",
    "/home/kdog3682/SVG",
    "/home/kdog3682/EXAMS",
    "/home/kdog3682/TEACHING",
    "/home/kdog3682/PDFS",
    "/home/kdog3682/PICS",
    "/home/kdog3682/CLIPS",
    "/home/kdog3682/JSONS",
    "/home/kdog3682/PYTHON/",
    "/home/kdog3682/TEXTS",
    "/home/kdog3682/MATH",
]


def check(outpath):
    import zipfile

    with zipfile.ZipFile(outpath, "r") as z:
        return map(z.filelist, lambda x: x.filename)

# pprint(unzip(glf()))
#name='COLORING'
#zip(absdir(colordir), outpath=drivedir + name + ' ' + datestamp() + '.zip')
#rmdir('/home/kdog3682/COLORING/', force=1)
# inoremap <buffer> <expr> 9 SmartNine('(')
# inoremap <buffer> qp (<c-o>A)<LEFT>


# /home/kdog3682/2024/codepens
# /home/kdog3682/2024/.gitignore
# files = mostRecentFileGroups(minutes = 5)
# files = mostRecent(dldir, minutes = 10)
# prompt(files)
# outpath = '/home/kdog3682/2024/codepens'
# for file in files:
    # shutil.move(file, outpath)

# mfiles(files, outpath)
# mkdir(outpath)
# names = flat(map2(files, unzip, outpath = outpath))
# append('/home/kdog3682/RESOURCES/file-table.txt', names)

def mostRecentZipFile():
    f = glf()
    ge = getExtension
    assert ge(f) == 'zip'
    return f

def getCodepen(target = 'style.stylus'):
    a = mostRecentZipFile()
    files = unzip(a, trashdir)
    loc = npath(trashdir, removeExtension(tail(a)))
    file = os.path.join(loc, 'src', target)
    outpath = smartnpath(target)
    assert isfile(outpath)
    append(outpath, read(file))

def codepenToMyCodePlayground():
    # a = mostRecentZipFile()
    # unzip(a, trashdir)
    # loc = npath(trashdir, removeExtension(tail(a)))

    loc = npath(trashdir, 'arc-example-from-stackoverflow')
    sourceFiles = absdir(os.path.join(loc, 'src'))
    log_files(sourceFiles)

    store = reduce(sourceFiles, lambda x: [getExtension(x), read(x)])
    html = store.get('html', '')
    css = store.get('css', '')
    js = store.get('js', '')
    stylus = store.get('stylus', '')

    s = ''

    if css: s += '\n' + 'css:\n' + css + '\n'
    if html: s += '\n' + 'html:\n' + html + '\n'
    if js: s += '\n' + 'javascript:\n' + js + '\n'
    append('/home/kdog3682/2023/codePlaygroundString.js', s)


# codepenToMyCodePlayground()
