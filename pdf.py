from base import *
from next import *
import time
import fitz
from pikepdf import Pdf
chdir(dldir)

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
    "bob": "/home/kdog3682/PDFS/Olenych Math 2 - Fractions.pdf",
    "ii": "/home/kdog3682/PDFS/Hugel Math - Fractions.pdf",
    "hugel": "/home/kdog3682/PDFS/Hugel Math - Fractions.pdf",
    "jj": "/home/kdog3682/PDFS/G4M Workbook 2.pdf",
    "kk": "/home/kdog3682/PDFS/G3M BIM Workbook.pdf",
    "bim3": "/home/kdog3682/PDFS/G3M BIM Workbook.pdf",
    "ll": "/home/kdog3682/PDFS/Olenych Math 1 - Number Sense.pdf",
    "bob1": "/home/kdog3682/PDFS/Olenych Math 1 - Number Sense.pdf",
    "mm": "/home/kdog3682/PDFS/G4M Mcgraw Workbook.pdf",
    "nn": "/home/kdog3682/PDFS/G5M Mcgraw Workbook.pdf",
    "oo": "/home/kdog3682/PDFS/G9M Exeter Workbook.pdf",
    "pp": "/home/kdog3682/PDFS/G4M BIM Workbook.pdf",
    "bim4": "/home/kdog3682/PDFS/G4M BIM Workbook.pdf",
    "qq": "/home/kdog3682/PDFS/G5M BIM Workbook.pdf",
    "bim5": "/home/kdog3682/PDFS/G5M BIM Workbook.pdf",
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
    if type(file) == fitz.fitz.Document:
        return file
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
        f = pdfdict.get(f, addExtension(f, 'pdf'))
        return Pdf.open(f, allow_overwriting_input=True)
    return f


def fixDest(s):
    s = re.sub("\\bg(?=\d)", "Grade ", s)
    s = re.sub(" *ehw", " Extra Homework", s)
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


def mergepdf(files, fn = lambda x: x.pages, **kwargs):
    if isdir(files):
        files = absdir(files)
    pdf = pikeCreate(files, fn)
    save(pdf, **kwargs)


def fitzSave(pdf, outpath, dir=0, openIt=1, incremental=0):
    if not outpath:
        outpath = pdf.metadata["title"]
    if not outpath:
        raise Exception("no outpath")
    outpath = addExtension(outpath, "pdf")
    if incremental:
        pdf.saveIncr()
    else:
        pdf.save(outpath)
    if openIt:
        ofile(outpath)


def save(pdf, outpath="test", dir=dldir, openIt=1):

    if strType(pdf) == "Document":
        return fitzSave(pdf, outpath, dir, openIt)

    assert pdf.pages

    if not outpath:
        outpath = str(pdf._original_filename)
    elif outpath and not isString(outpath):
        outpath = pdf.filename

    outpath = fixDest(outpath)
    outpath = addExtension(outpath, "pdf")
    if dir and not outpath.startswith('/'):
        outpath = npath(dir, outpath)

    pdf.save(outpath)
    if openIt: ofile(outpath)


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
    indexes = sorted(flat(list(indexes)), reverse=True)

    for i in indexes:
        del pdf.pages[i]
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
    if isNumber(f):
        prev = f
        f = lambda x: x.pages[prev]

    pdf = Pdf.new()
    for file in files:
        src = pikeOpen(file)
        value = f(src)
        try:
            pdf.pages.extend(value)
        except:
            pdf.pages.append(value)
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
    indexes = rangeFromString(indexes)
    pdf = pikeOpen()
    src = pikeOpen(file)


    for i in indexes:
        pdf.pages.append(src.pages[i])

    return pdf


def build_homework_files(s):
    s = removeComments(s)
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

        indexes = rangeFromString(indexes)
        pdf = pdfFromIndexes(src, indexes)

        if outpath.startswith('x'):
            return pdf
        outpath = fixDest(outpath)
        save(pdf, outpath, dir=dldir)

    return smallify(linegetter(s, trim=1, fn=fn))


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


def k5learning(grade=5):
    group = reverse(mostRecentFileGroups(minutes=2))
    pdfs = map(group, sliceStartEnd, end=1)
    mergepdf(
        pdfs,
        outpath=fixDest(f"g{str(grade)}cw"),
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


def whiteTheMargin(page, top=0, bottom=0, left=0, right=0):

    color = WHITE
    fill = WHITE
    width = 10

    r1 = 0
    r2 = 0
    r3 = 0
    r4 = 0

    if top:
        r1 = fitz.Rect(0, 0, page.rect.width, top)

    if bottom:
        r2 = fitz.Rect(
            0,
            page.rect.height - bottom,
            page.rect.width,
            page.rect.height,
        )

    if right:
        r3 = fitz.Rect(
            0,
            0,
            right,
            page.rect.height,
        )

    if left:
        r4 = fitz.Rect(
            left,
            0,
            page.rect.width,
            page.rect.height,
        )

    if not page.is_wrapped:
        page.wrap_contents()

    if r3:
        page.draw_rect(r3, color=color, fill=fill, width=width)
    if r4:
        page.draw_rect(r4, color=color, fill=fill, width=width)
    if r1:
        page.draw_rect(r1, color=color, fill=fill, width=width)
    if r2:
        page.draw_rect(r2, color=color, fill=fill, width=width)


def fitzOpenSave(f, fn, outpath=0, openIt=0, **kwargs):
    pdf = fitzOpen(f)
    try:
        value = fn(pdf, **kwargs)
        if value:
            inc = not outpath or tail(outpath) == tail(f)
            fitzSave(pdf, outpath or f, openIt=openIt, incremental=inc)
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
    return f


# removeStartEndPages('g4cw.pdf')


def sliceStartEnd(src, start=0, end=0, get=0):
    src = pikeOpen(src)
    if get:
        out = pikeOpen()
        a = 0
        b = get
        if isArray(b):
            a = b[0] - 1
            b = b[1]
        out.pages.extend(src.pages[a:b])
        return out
    if start:
        for i in range(start):
            del src.pages[0]
    if end:
        for i in range(end):
            del src.pages[-1]

    return src



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
    src = pikeOpen(pikeOpen(f))
    for item in items:
        pdf = pikeOpen()
        range = item.get("range")
        if isNumber(range):
            pdf.pages.append(src.pages[range - 1])
        elif isArray(range):
            pdf.pages.extend(
                src.pages[range[0] - 1 : range[1]]
            )
        else:
            for i in rangeFromString(range):
                pdf.pages.append(src.pages[i])
        save(pdf, outpath=item.get("name"))

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
#g4hw ll 25 | hh 9 | ii 16-17
#g4cw hh 7 8 15 17

#g5hw jj 149-152
g4hw pp 145 149
"""

#pprint(build_homework_files(removeComments(s)))


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
#rfile(glf(n=-1))
#mfile(glf(trashdir), dldir)
#rfile(glf())
#k5learning()


#f = "G5 2021 NYSE.pdf"
#f = sliceStartEnd(pikeOpen(f), get=4)
#save(f, outpath='g5cw')


def groupAction(f):
    group = mostRecentFileGroups()
    prompt(group, 'is this the group?')
    map(group, f)

#groupAction(removeWhitePages)


#To give a genuine amount.


def buildGrade4Classwork():
    s='''
        #g4hw bim3 139 145-147
        #g5hw bim3 160 161 163 165
        #g4ehw bim5 122 124 127 130
        #g4hw bim4 77 78 80 91 93 95
        x hugel 36 37 42
    '''
    f = glf()
    a = pikeOpen(f)
    indexes = getBlankPageIndexes(f)
    a = deletePages(a, indexes)

    pdf = build_homework_files(s)
    a.pages.extend(pdf.pages)
    save(a, 'g4cw')
#buildGrade4Classwork()
#print(glf())

def boop():
    names = [
        "G4 & G5 Extra Handout 1",
        "G4 & G5 Extra Handout 2",
        "G4 Extra Handout",
        "Student Letters",
    ]
    f = pikeOpen(glf())
    for i, name in enumerate(names):
        g = pikeOpen()
        g.pages.append(f.pages[i])
        save(g, outpath=name)

#splitpdf("G5 2021 NYSE", {
    #'G5 Classwork': '7-11',
    #'G5 Homework': '1-6',
#})

def grade5ClassworkHomework():
    file = glf()
    assert getExtension(file) == 'pdf'
    s = prompt('the pdf being used is the last file pdf of dldir. This will automatically create a classwork and homework via split of | creating 2 rangeIndexes.')
    a, b = split(s, '\|')

    pdf = pdfFromIndexes(file, a)
    save(pdf, 'g5cw')

    pdf = pdfFromIndexes(file, b)
    save(pdf, 'g5hw')


#pprint(grade5ClassworkHomework())

#pprint(k5learning(grade=4))

#pdfa = removeWhitePages(glf())
#pdfb = sliceStartEnd('Grade 4 Classwork', start=2)
#mergepdf([pdfa, pdfb], outpath='g4cw')
#insertpdf('test', )
def insertpdf(base=0, insert=0, after=0, before=0):
    if not insert: insert = 'test'
    base = gpdf(base)
    insert = gpdf(insert)
    pdf1 = pikeOpen(base)
    pdf2 = pikeOpen(insert)
    payload = pdf2.pages[0]
    pdf1.pages.insert(after, payload)
    save(pdf1, outpath='g4cw')
def gpdf(f):
    return addExtension(fixDest(f), 'pdf')

def opdf(f):
    ofile(gpdf(f))

#insertpdf('g4cw', after=7)


def whiteThePages(pdf, ignore=[], **kwargs):
    if isString(pdf):
        pdf = fitzOpen(pdf)
    for i, page in enumerate(pdf):
        if i not in ignore:
            whiteTheMargin(page, **kwargs)

    return pdf
        

def pictureBook():
    dir = colordir + datestamp()
    mergepdf(dir, outpath='Coloring Handouts')

#mergepdf(reverse(mostRecentFileGroups(minutes=2)), lambda x: x.pages[0])
#mergepdf(reverse(mostRecentFileGroups()), outpath='g4cw')
# Takes the last pdf group from dldir and combines them together. 
# It is important to do it in reverse so that the first downloaded items go first.


def bobThenHugel():
    s = "13 14 17    15 14"
    a, b = map(split(s, '   +|\|')[0:2], rangeFromString)
    A = pdfFromIndexes('bob', a)
    B = pdfFromIndexes('hugel', b)
    mergepdf([A, B], outpath='g4hw')

#bobThenHugel()

def classworkThenHomework():
    files = mostRecentFileGroups()
    a, b = splitInHalf(files)
    mergepdf(a, outpath='g5cw')
    mergepdf(b, outpath='g5hw')

#classworkThenHomework()
#snapshotOfDirectory()


#k5learning(4)


data = [
  {
    "classKey": "g5hw",
    "items": [
      {
        "fileKey": "bim4",
        "indexes": [
          172,
          175,
          176,
          177,
          178
        ]
      }
    ]
  },
  {
    "classKey": "g5cw",
    "items": [
      {
        "fileKey": "bim5",
        "indexes": [
          131,
          137,
          138,
          139,
          140
        ]
      }
    ]
  },
  {
    "classKey": "g4hw",
    "items": [
      {
        "fileKey": "bim5",
        "indexes": [
          115,
          165,
          177,
          178,
          181
        ]
      }
    ]
  }
]

pystring = '''
bob:
g4hw 23-25
'''
def buildFromJavascript():
    def runner(item):
        return pdfFromIndexes(item.get('fileKey'), item.get('indexes'))
    

    data = JavascriptAppCommand(key='pdfIni', arg=pystring)
    assert data

    for item in data:
        assignmentName = fixDest(item.get('classKey'))
        # this is not necessary to fix because save will fix it.
        # save kind of handles all of it.
        assert(assignmentName)
        children = map(item.get('items'), runner)
        assert children
        mergepdf(children, outpath=assignmentName)

#buildFromJavascript()

def getStateExams(name):
    dict = {
        'texas': '8-27',
        'california': '7-29',
    }

    files = mostRecentFileGroups(minutes=1)

    def runner(file):
        grade = search('gr?(?:ade)?-?(\d+)', file, flags=re.I)
        
        assert grade

        outpath = f"G{grade} {capitalize(name)} State Exam"
        indexes = dict.get(name)

        pdf = pdfFromIndexes(file, indexes)
        save(pdf, outpath=outpath)

    map(files, runner)

#printdir(dldir)
#pprint(getStateExams(name='texas'))
#pprint(getStateExams(name='california'))


def splitExamIntoMultipleParts(s, q):
    srcFile = find_file(q=q)
    ranges = map(linegetter(s), rangeFromString)
    #pprint(ranges)
    names = [
        'Homework',
        'Classwork',

        'Homework',
        'Classwork',
        'Extra Assignment'
    ]
    #pprint(srcFile)
    for i, indexes in enumerate(ranges):
        outpath = NameWrapper(names[i], next=i in [2,3])
        pdf = pdfFromIndexes(srcFile, indexes)
        pdf.save(outpath)
        ofile(outpath)

def NameWrapper(name, gradeLevel=5, next=0):
    aliases = {'e': 'Extra Homework', 'q': 'Quiz', 'h': 'Homework', 'c': 'Classwork'}
    def getName(s):
        m = search('^g?(\d)([hceq])w?$', s)    
        if m:
            return f"G{m[0]} {aliases[m[1]]}"
    
    dir = mathdir + upcomingDate('saturday', strife='-', next=next)
    file = getName(name) or f"G{gradeLevel} {capitalize(tail(name))}"
    file = addExtension(file, 'pdf')
    outpath = npath(dir, file)
    mkdir(dir)
    return outpath

s = """
    12-19
    5-11
    21-30
    21-27
    28-30 32-35
"""

#splitExamIntoMultipleParts(s, '-5')

#save(pdfFromIndexes(find_file('grade-3'), '7-12'), outpath=NameWrapper('g4hw'))

#name = NameWrapper('4h')
#save(whiteThePages(npath(dldir, name), bottom=50), dir=None, outpath=name)

#save(pdfFromIndexes(find_file('grade-4'), '10-16'), outpath=NameWrapper('4c'))

#name = NameWrapper('4c')
#save(whiteThePages(npath(dldir, name), bottom=50), dir=None, outpath=name)

#name = NameWrapper('4e')
#save(pdfFromIndexes('mm', "140 212 214 216"), outpath=name, dir=None)

#cfile(dldir + 'test.pdf', NameWrapper('4q'))
#cfile(NameWrapper('4q'), usbdrivedir)


#rlf()
#mergepdf(files, outpath='my_resumes_and_cvs.pdf')



def combineDownloadedPdfs():
    files = getFiles(dldir, pdf=1)
    save(pikeCreate(files, 0))
    results = chooseMultiple(files)
    pdf = mergepdf(results, outpath=incrementalName('Bulk PDF.pdf!'))
    prompt('Do you want to remove the files? ctrl-exit to depart')
    rfiles(files)

#combineDownloadedPdfs()
#sizes = map(files, fsize)
#checkpoint = iqrf(sizes)
#pdfs = filter(files, checkpoint)
#pdf = mergepdf(results, outpath=incrementalName('Bulk PDF.pdf'))

# iunmap <buffer> <expr> =
r   ='\d+\. +(\w+)'
# r='[a-z]{4,}'
file  ='/mnt/chromeos/MyFiles/Downloads/Third-Grade-Master-Spelling-Lists.pdf'
# rfile(glf())
file=glf()
def gt(file):
    return '\n'.join(fitzRead(file))

# clip(gt(file))
# data=re.findall(r, s)
# pprint(data)
# out='/home/kdog3682/2024/g3words.json'
# append(out, data)
file="/mnt/chromeos/GoogleDrive/MyDrive/TEACHING 2023/2021+Specialized+High+School+Handbook.pdf"
# 46 81 english
# 82 98 math
# 147 ak
# 150 185
# 186 203

def fitzRead(file, indexes = None):
    if indexes:
        return [page.get_text() for i, page in enumerate(fitzOpen(file)) if i > indexes[0] - 2 and i < indexes[1]]
    return [page.get_text() for page in fitzOpen(file)]

# clip(fitzRead(file, [82, 98]))



def white_bottom_footer(pdf, bottom = 0, left = 0, top = 0, right = 0, skip = []):
    def white(page):
        args = [
            left, # starts at the left
            page.rect.height - bottom, # bottom offset
            page.rect.width - right, # distance from right
            page.rect.height, # all the way to the bottom
        ]
        rect = fitz.Rect(*args)
        page.draw_rect(rect, color=WHITE, fill=WHITE, width=1)

    pdf = fitzOpen(pdf)
    for i, page in enumerate(pdf):
        if i - 1 in skip:
            continue
        white(page)

    return pdf

def delete_page_n(pdf, n):
    pdf = fitzOpen(pdf)
    if len(pdf) > 1:
        pdf.delete_page(n - 1)
    return pdf 

def extract_pdf_slice(input_pdf, a = 0, b = 0):
    if not b:
        b = a

    document = fitz.open(input_pdf)
    output_pdf = "/home/kdog3682/2024/test.pdf"
    new_doc = fitz.open()
    new_doc.insert_pdf(document, from_page=a, to_page=b)
    new_doc.save(output_pdf)
    new_doc.close()
    document.close()
    ofile(output_pdf)

test_dot_pdf = "/home/kdog3682/2024/test.pdf"
# file = "/mnt/chromeos/GoogleDrive/MyDrive/Chess Workbook (Part 1) [Advertisement].pdf"
# pdf = delete_page_n(file, 2)
# pdf = white_bottom_footer(pdf, skip = [1], bottom = 50, left = 150, right = 150)
# fitzSave(pdf, test_dot_pdf)
# /mnt/chromeos/GoogleDrive/MyDrive/Chess Workbook (Part 1) [Advertisement].pdf


# file = "/mnt/chromeos/GoogleDrive/MyDrive/Chess Workbook (Part 1) [Advertisement].pdf"
# pdf = white_bottom_footer(pdf, skip = [1], bottom = 50, left = 150, right = 150)
# fitzSave(pdf, test_dot_pdf, incremental = 1)

def get_page_dimensions(pdf_path, page_number = 1):
    page_number = page_number - 1
    document = fitzOpen(pdf_path)

    # Check if the document has the specified page
    if len(document) > page_number:
        # Get the specified page
        page = document[page_number]

        # Get the dimensions of the page
        page_dimensions = page.rect  # (x0, y0, x1, y1)
        width = page_dimensions.width
        height = page_dimensions.height

        print(f"Dimensions of page {page_number + 1}: Width = {width}, Height = {height}")
    else:
        print(f"The document does not have page number {page_number + 1}.")

    # Close the document
    document.close()

get_page_dimensions(test_dot_pdf)

