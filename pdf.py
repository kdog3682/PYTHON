from base import *
import time
import fitz
from pikepdf import Pdf

pdfdict = {
    "aa": "/home/kdog3682/PDFS/math5.pdf",
    "men": "/home/kdog3682/PDFS/G9 Mental Math.pdf",
    # sat math
    "bb": "/home/kdog3682/PDFS/Acing the New SAT Math PDF Book.pdf",
    "cc": "/home/kdog3682/PDFS/GAN Academy Math Demo.pdf",
    "dd": "/home/kdog3682/PDFS/G4M Morning Jumpstarts.pdf",
    "ee": "/home/kdog3682/PDFS/WS Maylynn Math.pdf",
    "ff": "/home/kdog3682/PDFS/Nihan Math Notes.pdf",
    "gg": "/home/kdog3682/PDFS/G6M 501 Word Problems.pdf",
    "hh": "/home/kdog3682/PDFS/Olenych Math 2 - Fractions.pdf",
    "ii": "/home/kdog3682/PDFS/Hugel Math - Fractions.pdf",
    "jj": "/home/kdog3682/PDFS/G4M Workbook 2.pdf",
    "kk": "/home/kdog3682/PDFS/G3M BIM Workbook.pdf",
    "ll": "/home/kdog3682/PDFS/Olenych Math 1 - Number Sense.pdf",
    "mm": "/home/kdog3682/PDFS/G4M Mcgraw Workbook.pdf",
    "nn": "/home/kdog3682/PDFS/G5M Mcgraw Workbook.pdf",
    "oo": "/home/kdog3682/PDFS/G9M Exeter Workbook.pdf",
    "pp": "/home/kdog3682/PDFS/G4M BIM Workbook.pdf",
    "qq": "/home/kdog3682/PDFS/G5M BIM Workbook.pdf",
}


def createReportCards():
    javascript("print.js", "GXY")
    files = ff(dir=dldir, name="^GXY")
    mergepdf(files, dir=drivedir, outpath="Grade Reports")


def utilGAGB(*names, **kwargs):
    """
    Used for GA and GA making python files
    Used at f:mergeEm
    """
    store = []
    assert len(names) > 0
    for i in range(1, kwargs.get("amount", 5) + 1):
        for name in names:
            f = addExtension(name + str(i), "pdf")
            store.append(f)
    return store


def mergeEm(files=0):
    if not files:
        files = utilGAGB("GA", "GB")
    pdf = pikeCreate(files, lambda x: x.pages)


########### OLD CREATORS ABOVE ##############


def defaultBlocker(blocks, parser=0):
    if parser:
        return map(blocks, lambda x: parser(x[4].strip()))
    return [
        (int(b[0]), int(b[1]), b[4].strip()) for b in blocks
    ]


def fitzOpen(file=0):
    if not file:
        return fitz.open()
    file = addExtension(file, "pdf")
    assert getExtension(file) == "pdf"
    return fitz.open(file)


@recentFileCache
def extractPages(file):
    return [page.get_text() for page in fitzOpen(file)]


def groupConsecutive(nums):
    if not nums:
        return None
    nums = [int(n) for n in nums]
    ranges = sum(
        (
            list(t)
            for t in zip(nums, nums[1:])
            if t[0] + 1 != t[1]
        ),
        [],
    )
    a = nums[0:1] + ranges + nums[-1:]
    a = paired(a)
    b = max(a, key=lambda x: x[1] - x[0])
    return [i for i in range(b[0], b[1] + 1)]
    return b


def parseText(s):
    if test("^[ABCD]\)|^Unauth|^[\d\s]+$|\.\.\.\.\.", s):
        return
    return s


def parseAnswer(s):
    return re.sub("^[A-Z]\) *", "", s)


def parse(pointer, go, i, data):
    text = [data[_i] for _i in range(pointer, go)]
    question = data[go]
    answers = [data[_i] for _i in range(go + 1, i + 1)]
    text = join(mapfilter(text, parseText))
    text = re.sub("\n", " ", text)

    answers.sort()
    answers = [parseAnswer(x) for x in answers]
    question = re.sub("\n", " ", question)

    numbers = unique(re.findall("\d+(?![\]\-\.\?])", text))
    numbers.sort()
    numbers = groupConsecutive(numbers)
    if numbers:
        index = numbers[-1]
        r = f" (?:{'|'.join([str(n) for n in numbers])})"
        text = re.sub(r, "", text)
    else:
        index = None

    output = {
        "text": text,
        "question": question,
        "answers": answers,
        "index": index,
    }
    return output


def somethingsomethingsat(file):
    store = []
    examNumber = getLastNumber(file)
    data = extractpdf(file)
    data = [x[2] for x in flat(data, 1)]
    pointer = 0
    go = 0

    r = "To make this paragraph most logical"
    for i, item in enumerate(data):
        if "[1]" in item:
            pointer = i
        elif test(r, item):
            if i - pointer < 100:
                go = i
        elif go and "D)" in item:
            print(pointer, go, i)
            value = parse(pointer, go, i, data)
            go = 0
            pointer = 0
            store.append(value)

    return {"examNumber": examNumber, "data": store}


files = [
    #'/home/kdog3682/TEACHING/SAT Grammar Test 2.pdf',
    #'/home/kdog3682/TEACHING/SAT Grammar Test 3.pdf',
    #'/home/kdog3682/TEACHING/SAT Grammar Test 1.pdf',
    #'/home/kdog3682/TEACHING/SAT Grammar Test 4.pdf',
]


def runit():
    store = [run(f) for f in files]
    store.sort(key=lambda x: x.get("examNumber"))
    # write('foo.json', store, open = 1)


def f(t):
    if test("^\d+\.", t):
        return re.sub("^\d+\.", "", t).strip()


def pikeOpen(f=0):
    if not f:
        return Pdf.new()
    if isString(f):
        f = pdfdict.get(f, f)
        return Pdf.open(f, allow_overwriting_input=True)
    return f


def fixDest(s):
    s = re.sub("g(?=\d)", "Grade ", s)
    s = re.sub(" *hw", " Homework", s)
    s = re.sub(" *q", " Quiz", s)
    s = re.sub(" *cw", " Classwork", s)
    return s


# pikeExtract('logic', [9, 10, 11, 12], 'Grade 4 Classwork')
# pikeExtract('g5math', [89, 90, 91, 92], 'Grade 5 Homework')
# 10-12-2022
# pikeExtract('br5-sb.pdf', '302-304', 'g5cw')
# pikeExtract('br5-sb.pdf', '299-301 288', 'g5hw')
# pikeExtract('br5-sb.pdf', '302-304', 'g4hw')
# pikeExtract('2021_Felix.pdf', '1-5', 'g4hw')
# pikeExtract('2022_Felix.pdf', '2-5', 'g4cw')


def mergepdf(files, **kwargs):
    pdf = pikeCreate(files)
    save(pdf, **kwargs)


def fitzSave(pdf, outpath, dir=0, openIt=1):
    if not outpath:
        outpath = pdf.metadata["title"]
    if not outpath:
        raise Exception("no outpath")
    outpath = addExtension(outpath, "pdf")
    pdf.save(outpath)
    if openIt:
        ofile(outpath)


def save(pdf, outpath="test", dir=dldir, openIt=1):

    isFitz = strType(pdf) == "Document"
    if isFitz:
        return fitzSave(pdf, outpath, dir, openIt)

    assert pdf.pages

    if not outpath:
        outpath = str(pdf._original_filename)
    elif outpath and not isString(outpath):
        if objectClassName(pdf) == "pdf":
            outpath = pdf.filename
        else:
            raise Exception(
                "outpath is neither string nor pdf"
            )

    outpath = addExtension(outpath, "pdf")
    outpath = npath(dir, outpath)

    pdf.save(outpath)
    if openIt:
        ofile(outpath)


payload = {
    "outpath": "Grade 5 Homework",
    "items": [
        {
            "file": "mixed",
            #'indexes': [24, 27],
            "indexes": [38, 40, 43, 45],
        },
        # {
        #'file': 'ef',
        #'indexes': [7, 8],
        # },
    ],
}
# pdfs = map(payload.get('items'), lambda item: pikeExtract(item.get('file'), item.get('indexes'), None))


def deletePages(file, *indexes):
    pdf = pikeOpen(file)
    count = -1
    indexes = flat(list(indexes))
    indexes.sort()
    for i in indexes:
        pdf.pages.remove(p=i - count)
        count += 1
    return pdf


payload = {
    "outpath": "Grade 4 Homework",
    "items": [
        {
            "file": "mixed",
            "indexes": [25, 26],
        },
    ],
}


def pikeCreate(files, f=lambda x: x.pages):
    pdf = Pdf.new()
    for file in files:
        src = pikeOpen(file)
        pdf.pages.extend(f(src))
    return pdf


mathfiles = [
    "/home/kdog3682/PDFS/workbook-grade-4.pdf",
    "/home/kdog3682/PDFS/g4math.pdf",
    "/home/kdog3682/PDFS/g5math.pdf",
    "/home/kdog3682/PDFS/g3math.pdf",
    "/home/kdog3682/PDFS/math5.pdf",
    "/home/kdog3682/PDFS/Fraction Puzzles.pdf",
    "/home/kdog3682/PDFS/433967411-Fun-tabulous-Puzzles-pdf.pdf",
    "/home/kdog3682/PDFS/workbook-grade-5.pdf",
]
# ofile(mathfiles)
def getName(s):
    s = removeExtension(tail(s))
    s = re.sub("^\d+[ -]", "", s)
    n = search("^[a-z]+\d+", s)
    if not n:
        n = abrev(s)
    return n


fracfiles = [
    "/mnt/chromeos/MyFiles/Downloads/grade-4-equivalent-fractions-a.pdf",
    "/mnt/chromeos/MyFiles/Downloads/grade-4-equivalent-fractions-improper-a.pdf",
    "/mnt/chromeos/MyFiles/Downloads/grade-4-adding-mixed-numbers-a.pdf",
    "/mnt/chromeos/MyFiles/Downloads/grade-4-subtracting-fractions-from-mixed-numbers-a.pdf",
    "/mnt/chromeos/MyFiles/Downloads/grade-4-subtracting-mixed-numbers-missing-subtrahend-a.pdf",
    "/mnt/chromeos/MyFiles/Downloads/grade-4-adding-mixed-numbers-fractions-like-denominators-a.pdf",
    "/mnt/chromeos/MyFiles/Downloads/grade-4-fractional-part-set-a.pdf",
    "/mnt/chromeos/MyFiles/Downloads/grade-4-subtracting-fractions-like-denominators-a.pdf",
]


def foo():

    chdir(dldir)
    data = clip()
    for payload in data:
        pdfs = map(
            payload.get("items"),
            lambda item: pikeExtract(
                item.get("file"), item.get("indexes"), None
            ),
        )
        mergepdf(pdfs, outpath=payload.get("outpath"))


def pikeRpw(source, f):
    src = pikeOpen(source)
    f(src)
    save(src, source)


def appendPage(source, payload, n=1):
    def f(src):
        payload = pikeOpen(payload).pages[0:n]
        src.pages.extend(payload)

    pikeRpw(source, f)


def compile_shsat_pdfs(file):

    year = search(yearRE, tail(file))
    if not year:
        return "ERROR - no year"

    once = oncef()
    store = extractPages(file)
    indexes = []
    answers = []

    if len(store) < 100:
        return "ERROR - invalid pdf length < 100"
    g9index = 70
    if len(store) > 150:
        g9index = 120

    for i, text in enumerate(store):
        if test("part [12]", text, flags=re.I):
            indexes.append(i)
        if test("answer key", text, flags=re.I):
            answers.append(i)
        if once(
            i > g9index
            and test("grade 9", text, flags=re.I)
        ):
            indexes.append(i)

    source = pikeOpen(file)
    if len(indexes) != 5:
        pdf = pdfFromIndexes(source, indexes + answers)
        save(pdf, "temp.pdf", openIt=1)
        indexes = rangeFromString(
            prompt(indexes, "write new indexes:")
        )
        answers = rangeFromString(
            prompt(answers, "write new answer indexes:")
        )

    else:
        prompt(indexes, answers, "indexes and answers")

    def lamb(i, plusAmount):
        return list(
            range(indexes[i], indexes[i] + plusAmount)
        )

    g9 = lamb(4, 3)
    v1 = lamb(0, 16)
    v2 = lamb(2, 16)
    m1 = lamb(1, 8)
    m2 = lamb(3, 8)

    dir = examdir + f"SHSAT {year}"
    mkdir(dir)

    items = [
        "G8 Math Exam A",
        m1,
        "G8 Math Exam B",
        m2,
        "G8 Verbal Exam A",
        v1,
        "G8 Verbal Exam B",
        v2,
        "G9 Math Exam",
        g9,
        "Answer Key",
        answers,
    ]

    for name, indexes in partition(items):
        pdf = pdfFromIndexes(source, indexes)
        save(pdf, name, openIt=1)

    return True


def pdfFromIndexes(file, indexes):
    pdf = pikeOpen()
    src = pikeOpen(file)

    indexes = rangeFromString(indexes)

    for i in indexes:
        pdf.pages.append(src.pages[i])

    return pdf


def build_homework_files(s):
    def fn(s):
        s = s.strip()
        if test("\|", s):
            outpath, rest = s.split(" ", maxsplit=1)
            items = map(re.split(" *\| *", rest), splitonce)
            outpath = fixDest(outpath)
            pdf = pikeOpen()
            for src, x in items:
                src = pikeOpen(src)
                indexes = rangeFromString(x)
                for i in indexes:
                    pdf.pages.append(src.pages[i])

            save(pdf, outpath=outpath, dir=dldir)
            return

        elif test("  ", s):
            outpath, s = splitonce(s, "  ")
            src, indexes = splitonce(s, " ")
        else:
            outpath, src, indexes = s.split(" ", maxsplit=2)

        outpath = fixDest(outpath)
        indexes = rangeFromString(indexes)
        pdf = pdfFromIndexes(src, indexes)
        save(pdf, outpath, dir=dldir)

    linegetter(s, trim=1, fn=fn)


def build_shsat_files():
    files = mapdir(clip(1), dldir)
    results = map(files, infof(compile_shsat_pdfs))
    pprint(printDirRecursive(examdir))
    pprint("RESULTS----------")
    pprint(results)


def toPike(fn):
    def decorator(x, *args, **kwargs):
        pdf = pikeOpen(x)
        return fn(pdf, *args, **kwargs)

    return decorator


def pikeMetaData(pdf):
    meta = pdf.open_metadata()
    print(meta["dc:title"])
    meta["dc:title"] = "foo"


def k5learning(minutes=50):
    group = mostRecentFileGroups(
        dldir, targetIndex=0, minutes=minutes
    )
    pdfs = map(group, lambda x: deletePages(x, -1))
    mergepdf(
        pdfs,
        outpath=promptOutpath(fallback="g5cw", fn=fixDest),
    )


# build_homework_files()
# k5learning(minutes=5)
# build_shsat_files() # something is wrong with localdef:lamb ...
# the files being output arent accurate
# need to move the stuff over
# pprint(build_homework_files()) # from workbooks ...

# from fitz.utils import getColor as g

WHITE = [1, 1, 1]
BLACK = [0, 0, 0]


def whiteTheMargin(pdf, xMargin=30, yMargin=20):
    count = len(pdf)

    if count == 4:
        page = pdf[1]
    else:
        page = pdf[0]

    r1 = fitz.Rect(0, 0, page.rect.width, yMargin)

    r2 = fitz.Rect(
        0,
        page.rect.height - yMargin,
        page.rect.width,
        page.rect.height,
    )

    r3 = fitz.Rect(
        0,
        0,
        xMargin,
        page.rect.height,
    )

    r4 = fitz.Rect(
        page.rect.width - xMargin,
        0,
        page.rect.width,
        page.rect.height,
    )

    if not page.is_wrapped:
        page.wrap_contents()

    color = WHITE
    fill = WHITE

    page.draw_rect(r1, color=color, fill=fill, width=10)
    page.draw_rect(r2, color=color, fill=fill, width=10)
    page.draw_rect(r3, color=color, fill=fill, width=10)
    page.draw_rect(r4, color=color, fill=fill, width=10)
    return pdf


def fitzOpenSave(f, fn, outpath=None, openIt=0):
    pdf = fitzOpen(f)
    try:
        value = fn(pdf)
        if value:
            fitzSave(pdf, outpath or f, openIt=openIt)
            print("success", f)
        return pdf
    except:
        print(f, "error")
        raise Exception()


def colorStuff():

    f = absdir(colordir)
    d = colordir + "dist/"

    for file in f:
        name = d + tail(file)
        if not test("punch", name, flags=re.I):
            continue
        pdf = fitzOpenSave(file, whiteTheMargin, name)
        pdf = pikeOpen(name)
        if len(pdf.pages) == 2:
            save(deletePages(pdf, 1), None)

        elif len(pdf.pages) == 4:
            # pprint(pdf.pages)
            save(deletePages(pdf, 0, 2, 3), None)


# pprint(colorStuff())
def printStuff():
    items = absdir(colordistdir)
    partitioner = Partitioner(items, "a")
    store = flat(list(partitioner.storage.store.values()))
    prompt(store)
    outpath = prompt("outpath for this stuff?")
    mergepdf(store, dir=dldir, outpath=outpath)


def fitzRead(file):
    return [page.get_text() for page in fitzOpen(file)]


def getBlankPageIndexes(file):
    store = []
    pages = fitzRead(file)
    for i, text in enumerate(pages):
        if not text.strip():
            store.append(i)
    return store


def merger(f, *files, **kwargs):
    indexes = getBlankPageIndexes(f)
    f = deletePages(f, indexes)
    for file in files:
        file = pikeOpen(file)
        f.pages.append(file.pages[0])
    save(f, **kwargs)


# temp = "/home/kdog3682/COLORING/dist/FC Pikachu and Friends.pdf"
# temp2 = "/home/kdog3682/COLORING/dist/FC Pikachu & Friends 2.pdf"
# merger(glf(), temp2, outpath=dldir + 'Grade 4 Final Exam.pdf')


names = [
    "Shujing",
    "Austin",
    "Anderson",
    "Alexander",
    "Mingrui",
    "Bonnie",
    "Stephen",
    "Felix",
    "Stephanie",
    "Jayden",
    "Ivy",
    "Vincent",
    "Alex",
    "Jeffery",
    "Sandy",
    "Daphne",
    "Olivia",
    "Jamin",
    "Leon",
    "Raymond",
    "Emerson",
]
r = "|".join(names)
# files = ff(dldir, name='^ga\d')


def reader(file):
    s = join(fitzRead(file))
    m = search(r, s)
    return [file, m]


# clip(map(files, reader))
# clip(join(fitzRead(glf())))

# def slicepdf(file):
# pdfOpen(f)

# save(pdfFromIndexes(glf(), '4-30'), outpath='G5 Practice Exam')


def foo(
    file=0,
    outpath=0,
    author="Brooklyn Learning",
    title="Math Homework",
):
    file_in = open(file, "rb")
    pdf_reader = PdfFileReader(file_in)
    metadata = pdf_reader.getDocumentInfo()
    pprint(metadata)

    pdf_merger = PdfFileMerger()
    pdf_merger.append(file_in)
    pdf_merger.addMetadata(
        {"/Author": author, "/Title": title}
    )
    file_out = open(outpath, "wb")
    pdf_merger.write(file_out)

    file_in.close()
    file_out.close()
    ofile(outpath)


def getStartEndIndexes(file, start=None, end=None):
    store = []

    pages = fitzRead(file)
    length = len(pages)
    clip(pages)
    # prompt('hi')
    raise Exception()

    if start:
        for i, text in enumerate(pages):
            if test(start, text, flags=re.I):
                prompt(text)
                store.extend(list(range(0, i)))
                prompt(store)
                break
    raise Exception()

    if end:
        for i, text in reverse(list(enumerate(pages))):
            if test(end, text):
                end = map(
                    list(range(0, i)),
                    lambda x: length - x - 1,
                )
                store.extend(end)
                break

    return store


def removeStartEndPages(file):
    chdir(dldir)
    indexes = getStartEndIndexes(
        file, start="page *2", end="stop"
    )
    prompt(indexes)
    f = deletePages(file, indexes)
    save(f)
    # save(f, outpath=file)


def removeWhitePages(f):
    indexes = getBlankPageIndexes(f)
    f = deletePages(f, indexes)
    save(f, outpath=None)


# removeStartEndPages('g4cw.pdf')


def sliceStartEnd(f, start, end):
    def runner(src):
        length = len(src.pages) - 1

        if start:
            for i in range(start):
                src.pages.remove(p=1)
        if end:
            for i in range(end):
                src.pages.remove(p=len(src.pages))

    pikeRpw(f, runner)


chdir(dldir)

# sliceStartEnd('g5cw.pdf', 8, 3)
# pprint(build_homework_files())
# that in this state ... I am not really talkative ...
# sliceNewPdf('g4cw.pdf', 'G4 Classwork', 10)
# that you dont get that far.
# What you want ... and this couldve been done much faster.


def sliceNewPdf(a, b, n):
    # 0-based indexes for the pages
    # 0:10 = 1 2 3 4 5 6 7 8 9 10 ???
    # pprint(list(range(0, 10))) # starts from 0 and gets to 9
    # is what it looks like

    src = pikeOpen(a)
    pdf = pikeOpen()
    pdf.pages.extend(src.pages[0:n])
    save(pdf, outpath=addExtension(b, "pdf"))


# removeWhitePages('WG5Q1.pdf')
def boo():
    file = glf()
    indexes = getBlankPageIndexes(file)
    f = deletePages(file, indexes)
    splitpdf(
        f,
        {
            "warmup": [1, 2],
            "ews": [3, 14],
            #'ws2': [5,6],
            #'ws3': [7,8],
            #'ws4': [9,10],
            #'ws5': [11,12],
            #'ws6': [13,14],
        },
    )


def fixOutpath(s, grade=4):
    dict = {
        "ews": "Extra Classwork",
        "ws1": "Extra Worksheet 1",
        "ws2": "Extra Worksheet 2",
        "ws3": "Extra Worksheet 3",
        "ws4": "Extra Worksheet 4",
        "ws5": "Extra Worksheet 5",
        "ws6": "Extra Worksheet 6",
    }
    s = dict.get(s, s)
    n = "G" + str(grade) + capitalize(s)
    n = addExtension(n, "pdf")
    return n


def splitpdf(f, items):
    items = [
        {"range": v, "name": k} for k, v in items.items()
    ]
    src = f
    for item in items:
        pdf = pikeOpen()
        range = item.get("range")
        if isNumber(range):
            pdf.pages.append(src.pages[range - 1])
        else:
            pdf.pages.extend(
                src.pages[range[0] - 1 : range[1]]
            )
        save(pdf, outpath=fixOutpath(item.get("name")))

def splitworksheets(f):
    # ehh not so much
    pages = fitzRead(f)
    store = []
    for i, page in enumerate(pages):
        if test("warmup|worksheet \d", page, flags=re.I):
            store.append(i)


# boo()


def spliter(srcFile, outpath, indexes):
    indexes = map(split(indexes, " "), rangeFromString)
    source = pikeOpen(srcFile)
    for i, range in enumerate(indexes):
        pdf = pdfFromIndexes(source, range)
        path = f"{outpath} Part {str(i + 1)}"
        save(pdf, outpath=path)


# spliter('g5cw.pdf', 'G5 2019 NYSE', '8-15 21-30')


s = """
g4hw ll 25 | hh 9 | ii 16-17
g4cw hh 7 8 15 17

g5hw jj 149-152
"""

# pprint(build_homework_files(s))


def scrapeAndFix():
    files = scrapeLinks()
    for file in files:
        outpath, indexes = promptSplit(
            tail(file), "outpath|indexstring"
        )
        pdf = pdfFromIndexes(file, indexes)
        save(pdf, outpath=outpath)


# scrapeAndFix()


def get():
    return pikeOpen(glf())




def getSet(*args, **kwargs):
    pdf = pikeOpen(kwargs.get('file') or glf())
    if every(args, isNumber):
        pdf = pdfFromIndexes(pdf, args)
    save(pdf, outpath=kwargs.get("outpath"))

#getSet(5, 6, 8, outpath="Student Letters")

def manager():
    prefix = 'G4 '
    def replacer(s):
        s = re.sub(' *week.+', '', s, flags=re.I)
        s = prefix + capitalize(s)
        return s

    file = glf()
    name = removeExtension(tail(file))
    def namechange(file):
        newName = changeFileName(file, replacer)
        mfile(file, newName)
        return newName

    if test('week', name, flags=re.I):
        return namechange(file)

    if name == 'warmup':
        file = namechange(file)
        return removeWhitePages(file)

#manager()
