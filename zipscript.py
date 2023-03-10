from base import *
import time
import zipfile


def readzip(inpath=None, outpath=None, flatten=0):
    if not inpath:
        inpath = choose(absdir(zipdir), mode=1)
    if not outpath:
        outpath = abspath(
            pubdir
            + removeDateStamp(removeExtension(tail(inpath)))
        )

    assert getExtension(inpath) == "zip"
    prompt('prompting', inpath, outpath)

    with zipfile.ZipFile(inpath, "r") as z:
        z.extractall(outpath)

        files = map(z.filelist, lambda x: x.filename)
        pprint(files)
        print("number files extracted", len(files))

        if flatten:
            flatdir(outpath)
        return 1


def writezip(
    x, outpath=zipdir, name="backup", date=1, delete=0
):

    if not x: return print('empty x', x)

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
        date = ''
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

    print('success!\nWrote files to', outpath)


def zipWriteAll(outpath, files):
    errors = []
    with zipfile.ZipFile(outpath, "w") as z:
        for file in files:
            if zipWrite(z, file):
                errors.append(tail(file))
        if len(errors) > 10:
            clip(errors)
            raise Exception('to many errors')

def zipWrite(z, f):
    if not f:
        return 1
    try:
        name = re.sub('^\.', '', tail(f))
        compression = zipfile.ZIP_DEFLATED
        z.write(f, arcname=name, compress_type=compression)
        return 0
    except Exception as e:
        print(f, " -- ", "ERROR:", str(e))
        return 1


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
        files = ff('js')
        return writezip(files, name="javascript")

    if key == "test":
        files = ["v.js"]
        return writezip(
            files, name="test", delete=1
        )

    if key == "oldpy":
        files = ff("cwf py old")
        return writezip(
            files, name="oldpy", delete=1
        )

    if key == "oldjs":
        files = ff("pub js old")
        return writezip(
            files, name="oldjs", delete=1
        )

    if key == "recent":
        files = recentFiles()
        return writezip(files, name="recent")

    e = getExtension(key)

    if e == "html":
        files = getFileDependencies(key)
        return writezip(files, name=key)


def fixZipAccident():
    raise Exception('need to fix file path here')
    f = '/home/kdog3682/zip-files.log.txt'
    files = re.findall('file: (\S+)', read(f))
    files = map(files, lambda f: normpath(trashdir, f))
    files = filter(files, isfile)
    chdir(pubdir)
    files = key
    return writezip(
        files, name="oldjs"
    )

#backup('oldpy')
#backup('recent')
#consolidate.js
#backup(jsondir)
#backup(txtdir)
#printdir(jsdir)
#print(os.listdir(sandir))
#copydir(zipdir, sandir)
# the difficulties can be solved.

def unzipSpecificFile(s):
    inpath = drivedir + 'ZIP/JSONS-09-21-2022.zip'
    with zipfile.ZipFile(inpath, "r") as z:
        z.extract('known.json', path=dldir)

def unzipLatest():
    f = glf()
    readzip(f, flatten=True, outpath=normpath(dldir, removeExtension(tail(f))))

    flatdir(mostRecent(dldir))

#unzipLatest()

# Bad actors do not act bad on purpose.
# 


files = [
    "/home/kdog3682/PRODUCTIONS",
    "/home/kdog3682/SVG",
    "/home/kdog3682/EXAMS",
    "/home/kdog3682/TEACHING",
    "/home/kdog3682/PDFS",
    "/home/kdog3682/PICS",
    "/home/kdog3682/CLIPS",
    "/home/kdog3682/JSONS",
    "/home/kdog3682/COLORING",
    "/home/kdog3682/JAVASCRIPT/",
    "/home/kdog3682/PYTHON/",
    "/home/kdog3682/TEXTS",
    "/home/kdog3682/LOGS",
    "/home/kdog3682/MATH",
    "/home/kdog3682/SERVER",
    "/home/kdog3682/VIM & SH",
]


def check(outpath):
    import zipfile
    with zipfile.ZipFile(outpath, "r") as z:
       return map(z.filelist, lambda x: x.filename)
