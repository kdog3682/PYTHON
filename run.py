chatgptjsonfile = '/home/kdog3682/2023/chatgpt.json'
departurejsonfile = '/home/kdog3682/2023/departures.json'

from base import *
#from next import *
from announce import announce
import time
import inspect
import env


def drivePicturesToHammyArtContestFolder(contestNumber):
    from heif import heicToJpg
    assert contestNumber
    dir = mkdir(dir2023 + 'hammy-math-class/art-contest-' + str(contestNumber))
    files = mostRecentFileGroups(drivedir)
    f = lambda x: npath(dir, changeExtension(x, 'jpg'))
    items = double(files, f)
    for a,b in items:
        heicToJpg(a, b)


def email(body='', to=0, subject="", files=0):
    ids = None
    if files:
        files = toArray(files)
        drive = GoogleDrive()
        ids = map(files, drive.uploadFile)

    emailBody = {
        "attachments": ids,
        "from": env.EmailContacts.get("self"),
        "to": env.EmailContacts.get(to or "self"),
        "body": body,
        "subject": subject,
    }
    prompt(emailBody)

    appscript('email', emailBody)

def to_callable(s, *args):
    arg_str = ', '.join(map(args, to_argument))
    output = f"{s}({arg_str})"
    return output
def to_argument(s):
    return json.dumps(s)

def appscript(s, *args):
    s = to_callable(s, *args)
    s = f"Finish({s})"
    #print(s)
    #return
    googleAppScript(s)



def emailLastFile():
    email(subject="last file", files=glf())

def yuma(a, b, c):
    dprint(a, b, c)



def pythonWithState(s, state):

    args, kwargs = getArgsKwargs(s)
    fn = 0
    file = 0
    text = 0

    if kwargs.get('write'):
        fn = write
        file = kwargs.get('write')
    elif kwargs.get('append'):
        fn = append
        file = kwargs.get('append')
    else:
        fn = identity 
    
    if 'block' in args:
        text = state.get('blockText')
    else:
        text = read(state.get('file'))

    if isString(text) and fn and file:
        fn(file, text)
        webbrowser.open(file)
    else:
        print("'not done yet'")



    #if mode == 'append':
        #lang = state.get('lang')
        #name = re.sub('^(?:add|get|remove|find)', '', fnKey.lower())
        #append(state.get('file'), createVariable(name, value, lang))
    #else:
        #print(value)

def python(argv = sys.argv[1:]):
    if not argv:
        return print("requires shell")

    key, *args = argv

    if key == 'pythonWithState':
        return pythonWithState(*read('pythonWithState.json'))

    args = map(list(args), shellunescape)
    key = env.basepyref.get(key, key)
    fn = globals().get(key)
    #print(fn, args)
    fn(*args)



cwtFileDict = {
    'announcement': 5,
    'handout': 5,
    'extra': 4,
    'homework': 2,
    'classwork': 1,
    'exam': 3,
    'test': 3,
    'quiz': 3,
    'report': 6,
}
def sortCwtFiles(s):
    s = tail(s).lower()
    m = dsearch(s, cwtFileDict)
    assert m
    return (m, s)

def changers():
    
    changers = {
        "g5r.pdf": "Grade 5 Final Exam Review.pdf",
        "g4r.pdf": "Grade 4 Final Exam Review.pdf",
        "g5hw.pdf": "Grade 5 Homework.pdf",
        "g4hw.pdf": "Grade 4 Homework.pdf",
        "g5cw.pdf": "Grade 5 Classwork.pdf",
        "g4cw.pdf": "Grade 4 Classwork.pdf",
        "g5q.pdf": "Grade 5 Quiz.pdf",
        "g4q.pdf": "Grade 4 Quiz.pdf",
        "WG5Q1.pdf": "Grade 5 Quiz.pdf",
        "WG4Q1.pdf": "Grade 4 Quiz.pdf",
        "g4exam.pdf": "Grade 4 Exam.pdf",
        "g5exam.pdf": "Grade 5 Exam.pdf",
    }

    for file, destination in changers.items():
        if isfile(file) and not isRecent(
            destination, days=3
        ):
            if prompt('change it?', file, destination):
                mfile(file, destination)

def buildFiles():
    chdir(dldir)
    changers()
    regex = reWrap(cwtFileDict)
    #files = ff(dldir, hours=40, pdf=1, regex=regex, flags=re.I, antiregex='test.pdf')

    files = [
        "G5 Classwork.pdf",
        "Grade 4 Announcements.pdf",
        "G4 Homework.pdf",
        "G4 Classwork.pdf",
        "Grade 5 Announcements.pdf",
        "G5 Homework.pdf",
        "Student Letters.pdf"
    ]

    storage = Storage()
    misc = []

    for file in files:
        k = search('g(?:rade)? *(\d+)', file, flags=re.I)
        if k and not test('announcement|report', file, flags=re.I):
            storage.add(k, file)
        else:
            misc.append(file)

    data = []
    for k,v in storage.toJSON().items():
        data.append({
            'key': k,
            'files': sort(v, sortCwtFiles),
        })
    prompt({
        'all-files': files,
        'data': data,
        'misc': misc,
        'caller': 'buildFiles',
    })
    return [data, misc, files]

def uploadFiles(files):
    from ga import GoogleDrive
    def fixName(s):
        return removeExtension(tail(s))
    drive = GoogleDrive()
    return [{'id': drive.uploadFile(f), 'name': fixName(f)} for f in files]



def uploadMaterials(skipClassroom=0, skipEmail=0, official=1, fileData=0, doGrades=1):
    from ga import GoogleClassroom, GoogleDrive

    data, misc, all = fileData or buildFiles()
    assert data
    store = []
    rooms = []

    for item in data:
        key = item.get("key") if official else "emc"
        files = item.get("files")
        room = GoogleClassroom(key)
        rooms.append(room)
        room.skipClassroom = skipClassroom 
        assert files
        results = map(files, room.uploadAssignment)
        assert results
        room.openLink()
        store.extend(results)

    # ------------------------------------------------
    def getSubject(subject="G4/G5", topic="Math"):
        date = upcomingDate("saturday")
        return f"{subject} {topic} Materials {date}"
    # ------------------------------------------------

    if misc:
        store.extend(uploadFiles(misc))

    payload = {
        "subject": getSubject(),
        "files": map(store, lambda x: x.get("name")),
        "attachments": map(store, lambda x: x.get("id")),
        "to": env.workEmail if official else env.EmailContacts.get('self')
    }

    # ------------------------------------------------
    if skipEmail:
        print('Done. Skipping email.')
        return 

    prompt('We always prompt the payload before going to google emails', payload)

    googleAppScript("Action", "courseWork", payload)
    gmailsenturl = "https://mail.google.com/mail/u/0/#sent"
    ofile(gmailsenturl)
    #clear(departurejsonfile)
    deleteFinishedPDFS()
    if doGrades:
        print("Starting the gradeClassroom auto process.")
        for room in rooms:
            gradeClassroom(room)

def cwtBuildNecessaryFiles(grades=[4, 5]):
    print("'this is kind of deprecated ... as the systems get better and better")
    raise Exception('use buildFiles instead')

    extraFiles = [
        # "G4 & G5 Math Report Cards.pdf",
        # "G4 & G5 Online Report Cards.pdf",
        # "Announcements",
        # "Progress Reports",
        # "Midterm 1 Scores",
        # "Final Exam Scores",
        # "Report Cards",
        "Grade Reports",
    ]
    baseFiles = [
        "Exam",
        "Final Exam",
        "Practice Exam",
        "Extra Homework",
        "Homework",
        "Classwork",
        "Quiz",
        # "Final Exam Review",
        # "Warmup",
        # "Handout Packet 1",
        # "Handout Packet 2",
        # "Handout Packet 3",
        # "Midterm Exam Review",
        # "Midterm Exam",
        # "Handout",
        # "Extra Worksheets",
        # "Quarter 1 Exam",
        # "Announcement",
    ]

    changers = {
        "g5r.pdf": "Grade 5 Final Exam Review.pdf",
        "g4r.pdf": "Grade 4 Final Exam Review.pdf",
        "g5hw.pdf": "Grade 5 Homework.pdf",
        "g4hw.pdf": "Grade 4 Homework.pdf",
        "g5cw.pdf": "Grade 5 Classwork.pdf",
        "g4cw.pdf": "Grade 4 Classwork.pdf",
        "g5q.pdf": "Grade 5 Quiz.pdf",
        "g4q.pdf": "Grade 4 Quiz.pdf",
        "WG5Q1.pdf": "Grade 5 Quiz.pdf",
        "WG4Q1.pdf": "Grade 4 Quiz.pdf",
        "g4exam.pdf": "Grade 4 Exam.pdf",
        "g5exam.pdf": "Grade 5 Exam.pdf",
    }

    for file, destination in changers.items():
        if isfile(file) and not isRecent(
            destination, days=3
        ):
            mfile(file, destination)

    storage = Storage()

    p1 = "Grade "
    p2 = "G"
    for file in baseFiles:
        file = toPdf(file)
        for grade in grades:
            a = str(grade) + " " + file
            if isRecent(p1 + a, days=3):
                storage.add(grade, p1 + a)
            elif isRecent(p2 + a, days=3):
                storage.add(grade, p2 + a)

    items = storage.toJSON().items()
    classFiles = [
        {"key": str(k), "files": v} for k, v in items
    ]
    extraFiles = filter(map(extraFiles, toPdf), isfile)
    data = {
        "classFiles": classFiles,
        "extraFiles": extraFiles,
    }
    return data


env.basepyref["em"] = "email"
env.basepyref["um"] = "uploadMaterials"
env.basepyref["mr"] = "mostRecentDirectoryFiles"
env.basepyref["rev"] = "revertFile"
env.basepyref["rr"] = "replyReddit"
env.basepyref["rjs"] = "redditFromJS"
env.basepyref["eod"] = "endOfDay"

def replyReddit():
    from redditscript import Reddit

    reddit = Reddit()
    reddit.reply_all_comments()
    print("done replying to comments")


def redditFromJS(items):
    from redditscript import Reddit

    reddit = Reddit()

    submissions = []
    for i, o in enumerate(items):
        try:
            submission = reddit.ask(**o)
            submissions.append(submission)
            openBrowser(submission.shortlink)
        except:
            print(o, "error")
            pass

    print("done")
    return
    a = choose(map(items, "title"), auto=0)
    if not a:
        return
    for s in submissions:
        if s.title in a:
            s.delete()
            print("deleting", s.title)


def runFunction(fn, *args):
    count = countArgs(fn)
    args = list(args)[0:count]
    print(args)

def countArgs(f, *args, **kwargs):
    data = inspect.signature(f)
    params = data.parameters
    s = str(data)
    if "*" in s:
        return 255
    return len(params)


def gitDelete(file):
    cmd = f"""
        git rm {file}
        git commit -m "REMOVE {file}"
        git push
    """

    SystemCommand(cmd)



def gitPushWorking():
    gitPush(message='everything is working')

def gitPush(dir=dir2023, message='autopush'):
    if dir == dir2023 or dir == pydir:
        cleandir(dir)
        time.sleep(1)

    if dir == dir2023:
        diff = parseDiff(dir=dir)
        appendjson('git.json', diff)
        time.sleep(1)

    mainCommand = f"""
        cd {dir}
        git add .
        git commit -m "'{message}'"
        git push
    """

    response = SystemCommand(mainCommand, dir=dir)
    gitData = {
        'success': response.success,
        'error': response.error,
    }
    pprint(gitData)
    if message != 'autopush':
        gitData['message'] = message
    #logger(**nameObject, action='gitpush', message=message, gitData=gitData)


def gitManager(
    file=0,
    files=0,
    move=0,
    remove=0,
    push=1,
    message=0,
    dir=dir2023,
    firstTime=0,
):
    pushStatement = (
        "git push -u origin main"
        if firstTime
        else "git push"
    )
    if remove:
        gitMode = "git rm "
        moveStr = ""
        if not message:
            message = "automated git remove"
    elif move:
        gitMode = "git mv "
        moveStr = " " + move
        if not message:
            message = "automated git move"
    elif push:
        gitMode = "git add "
        moveStr = ""
        if not message:
            message = "automated git push"

    lines = []
    if dir:
        lines.append(f"cd {dir}")

    if files:
        for file in files:
            lines.append(gitMode + tail(file))
    elif file:
        lines.append(gitMode + tail(file) + moveStr)
    elif push:
        lines.append("git add .")
        message = "automated git push everything"

    lines.append(f'git commit -m "{message}"')
    lines.append(pushStatement)
    cmd = join(lines)
    # return print('debugging', cmd)
    SystemCommand(cmd)

def gitPushAll():
    pass
    #gitPushPython()
    #time.sleep(1)
    #gitPush()


env.basepyref["gp"] = "gitPush"
env.basepyref["gpx"] = "gitPushAll"
env.basepyref["gd"] = "gitDelete"
env.basepyref["elf"] = "emailLastFile"

env.basepyref["gi"] = "gitInit"
env.basepyref["gpy"] = "gitPushPython"
env.basepyref["fp"] = "filePicker"
def gitPushAll():
    raise Exception()
    gitPushPython()
    gitPush()

def detect_content_type(text):
    # Check for HTML tags
    if '<html' in text or '<body' in text or '<div' in text:
        return 'HTML'

    code_keywords = ['const', 'function', 'def']
    #code_keywords = ['def', 'class', 'import', 'return', 'for', 'while', 'if', 'else', 'func]
    for keyword in code_keywords:
        if keyword in text:
            return 'Code'

    return 'Prose'


def parseMathcha(state):
    #unzip(state.file, mathchadir)
    file = mathchadir + 'index.html'
    ofile(file)

def filter2023(items, fn=0, **kwargs):
    checkpoint = fn if fn else checkpointf(**kwargs)
    return [item for item in items if checkpoint(item)]


def parseOpenai(state):
        raw = map(state.data, parseJSON)
        data = filter2023(raw, lambda x: not isPrimitive(x))
        return clip(flat(data))
        pprint(data)
        raise Exception()
        if every(data, lambda x: len(x.keys()) == 1):
            key = list(data[0].keys())[0]
            if every(data, lambda x: key in x):
                pprint('hi')
                payload = flat(map(data, lambda x: x.get(key)))
                return clip(payload)
            else:
                raise Exception()

        return pprint(data)
        item = reverseIter(data, runner)
        if item:
            return write('chatgpt-generated-html.html', item, 1)
        #return ofile(file)

smartItems = [
    {
        'name': 'online-document',
        'fn': parseMathcha
    },
    {
        'tail': 'openai.*?json',
        'fn': parseOpenai,
    },
    {
        'extension': 'html',
        'fn': lambda state: ofile(state.file)
    },

    {
        'extension': 'zip',
        'fn': lambda state: unzip(state.file, prompt('name for zip?'))
    },

    {
        'tail': 'resume.*?pdf',
        'fn': lambda state: mfile(state.file, 'Kevin Lee resume.pdf')
    },
]
class FileState:
    def __init__(self, file):
        self.file = file
        self.tail = tail(file)
        self.name = removeExtension(self.tail)
        self.extension = getExtension(file)
        pprint(self.file)

    @property
    def data(self):
        try:
            return read(self.file)
        except Exception as e:
            print(str(e))
            return 

def smartManager():
    file = glf()

    state = FileState(file)

    def runner(item, key):
        q = item.get(key)
        if q and test('^' + q, getattr(state, key)):
            return True

    keys = ['name', 'extension', 'tail', 'file']
    for item in smartItems:
        for key in keys:
            if runner(item, key):
                return item['fn'](state)


def addPythonImports(s):
    
    importRef = {
        'Github': 'githubscript',
        'Google': 'ga',
        'aiprompt': 'chatgpt',
    }
    extra = dsearch(s, importRef, '^(?:$1)')
    return f"from {extra} import *\n{s}" if extra else s

def pythonAppController():
    resourcedir = rootdir + 'Resources2023/'
    items = split(removeComments(read(resourcedir + 'pac.txt')), '\n\n+')
    cmd = dollarPrompt(items)
    cmd = addPythonImports(cmd)
    try:
        exec(cmd)
    except Exception as e:
        pprint(cmd)
        pprint(e) 
    

def googleAppController():
    items = split(removeComments(read('gac.txt')), '\n+')
    s = dollarPrompt(items)
    return googleAppScript(f"Finish({s})")


def execPython(s=''):
    dict = {
        'av': 'appendVariable',
    }
    s = dreplace(s, dict, template='b')
    exec(s)


env.basepyref['pac'] = 'pythonAppController'
env.basepyref['sm'] = 'smartManager'
#pprint(smartManager())


exclude = ['decimals', 'percentages', 'exponents', 'square roots']
chatgptPrompts = f"""
#Samantha walks a total of 2/3 miles to and from school every day. Finish the text for this math question. Create 4 possible answer choices. Only one of them should be correct. Output the results in a json containing keys: "problem", "choices", "answer."

Use the following instructions for all further prompts. The instructions are: Finish the text for the math question based on the given prompt. Then, create 4 possible answer choices. Only one answer choice should be correct. Output the results in a json containing keys: "problem", "choices", "answer", and "tags". The tags should describe what type of math question it is.

If the problem incorporates a table, do not write the table in the problem. Rather, incorporate the table as data under a "data" key.

When generating the problem, do not use {', '.join(exclude)}.


If the question or answer or choices include math, write them as latex.
Always output the result in a json object.


What is this insane magic ...
What is this absolute insanity ...

If a job can be automated ...

"""
def reverseIter(items, f):
    for i in range(len(items) -1, -1, -1):
        item = items[i]
        result = f(item)

        if result == True:
            return item
        elif result == False:
            return 

def opener(s):
    s = removeComments(s).strip()
    return write('ofile.js', s, 1)

#opener(chatgptPrompts)

#pprint(smartManager())

def getChatGptPrompt():
    def runner(x):
        s = x.group(0)
        return stringify(eval(s))
    s = read('/home/kdog3682/2023/chatgpt.txt')
    s = removeComments(smartDedent(s))
    s = re.sub('(?<== ).+', runner, s)
    s += '\n'
    s += '\n'
    s += 'Output the results in json list form.'
    return s

def runChatgpt(cmd=0):
    debug = 1
    if not cmd: 
        cmd = getChatGptPrompt()
        debug = 0

    from chatgpt import ask
    response = ask(cmd).strip()
    payload = {
        'prompt': cmd,
        'response': response,
    }

    if debug:
        print(response)
    else:
        appendjson(chatgptjsonfile, payload, mode=list)


def previewMaterials():
    try:
        fileData = read(departurejsonfile)
        if exists(fileData):
            return uploadMaterials(fileData=fileData)
    except Exception as e: 
        pass

    data, misc, files = buildFiles()
    ofile(files)
    if prompt(files, 'ready for departure?'):
        write(departurejsonfile, [data, misc, files])


env.basepyref['pm'] = 'previewMaterials'
#pprint(runChatgpt())


def masterFileInfo(dir=dir2023):
    files = sorted(absdir(dir))
    def runner(f):
        name = tail(f)
        date = datestamp(f)
        size = fsize(f)
        return {
            "name": tail(f),
            "size": fsize(f),
            "date": date,
            "extension": getExtension(f)
        }
    payload = map(files, runner)
    outpath = tail(dir) + '.directory.json'
    write(outpath, payload, True)


def gitPushPython():
    gitPush(dir=pydir)

#masterFileInfo()
#pprint(len(map(filter(read('2023.directory.json'), lambda x: x.get('extension')=='js'), lambda x: x.get('name'))))
env.basepyref['gpy'] = 'gitPushPython'
def copyToBrowser(s):
    return write(dldir + 'ofile.js', removeComments(s).strip(), 1)

def temporaryBackup(state):
    announce()
    pprint(state)
    files = ff(state.get('buffers'), js=1, biggerThan=100)
    cfiles(files, tempbudir, ask=1)


def revert(file=0, vim=0, increment=0, dir=0, ask=0):
    if not file:
        file = mostRecent(budir)
        if not dir:
            dir = dirFromFile(file)
        name = dir + file
    elif increment:
        if not dir:
            dir = dirFromFile(file)
        name = incrementName(npath(dir, file))
    elif ask:
        name = prompt(file, "name for the file ?")
        name = dir + name

    if not dir:
        dir = dirFromFile(file)
        dir = budir

    outpath = name or dir
    dprint(outpath, file)
    if vim:
        appendVim("filedict", outpath)
    cfile(file, outpath)

def revertjs(file):
    print('reverting js', file)
    assert(file) 
    src = trashdir + file
    if not isfile(src):
        src = budir + file

    assert isfile(src)
    outpath = dirFromFile(file)
    input(dprint(src, outpath))
    mfile(src, outpath)

def deleteFinishedPDFS():
    ff(dldir, pdf=1, mode='delete', weeks=2)

# The file is reverted from 
#smartManager()

#runChatgpt("""
#Explain what the function below does:
#def copyToBrowser(s):
    #return write(dldir + 'ofile.js', removeComments(s).strip(), 1)
#""")


def shonitProject():

    import redditscript
    from tesseract import tesseractExtractText

    kwargs = dict(
        user = 'shonitB',
        type = 'image',
        minScore = 5,
        minNumComments = 5,
        subreddit = None,
        fromDate = 0,
        toDate = 'today',
    )
    shonitImageLinks = redditscript.Reddit().getPosts(**kwargs)
    store = []
    for url in shonitImageLinks:
        localPath = downloadImage(url, name = 'temp')
        text = tesseractExtractText(localPath)
        text = postProcess(text)
        if text:
            store.append(text)

    return store


def downloadImage(url, name, openIt=0):
    import requests
    r = requests.get(url)
    if r.status_code == 200:
        with open(name, "wb") as f:
            f.write(r.content)
            print("Image sucessfully Downloaded: ", name)
            if openIt:
                ofile(name)
            return name
    else:
        print("Image Couldn't be retreived", name)

#printdir()



def surmonChinese(links):
    raise Exception('do later')
    import bs4
    import html

    def getLinks(n):
        base = f"https://surmon.me/article"
        soup = bs4.BeautifulSoup(request(base), "html.parser")
        soup.find_all('links')

    def runner(url):
        text = request(url, delay=5)
        if not text:
            return 

        store = []
        body = bs4.BeautifulSoup(text, "html.parser").body
        for item in body.find_all(recursive=True):
            name = item.name
            if name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                text = item.get_text()
                if isChinese(text) or isEnglish(text):
                    store.append((name, text))

        return store

    store = filter(map(links, runner))
    return store

#pprint(surmonChinese())


def subprocessRun(s):
    import subprocess
    lines = linegetter(s)
    dprint(lines)
    kwargs = dict(stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    for line in lines:
        result = subprocess.run(line, **kwargs)
        success = result.stdout.decode()
        error = result.stderr.decode()
        if result.returncode == 0:
            dprint(success)
        else:
            dprint(line)
            dprint(error)
            return 


def compile_latex(texFile):
    initCommand = """

         sudo apt-get update
         sudo apt-get install texlive-latex-base

    """
    subprocessRun(initCommand)


    if find_latex_packages_dir():
        subprocessRun("sudo apt-get install texlive-latex-extra")

    pdfFile = changeExtension(texFile, 'pdf')
    createCommand = f"pdflatex {texFile}"
    subProcessRun(createCommand)

    if isfile(pdfFile):
        print('success')
        ofile(pdfFile)


def create_tex(file = 'document.tex'):
    write(file, env.sampleTexText.strip())
    return file

def find_latex_packages_dir():
    import subprocess
    try:
        output = subprocess.check_output(["kpsewhich", "-var-value", "TEXMFMAIN"])
        return output.decode("utf-8").strip()
    except (subprocess.CalledProcessError, OSError):
        print("Error: Could not find LaTeX packages directory.")
        return None


def doLatex():
    raise Exception('lock package is running... need to check it later')
    print("cannot run at the moment or something may break")
    chdir(latexdir)
    compile_latex(create_tex())

def is_package_manager_locked():
    lock_file_path = '/var/lib/dpkg/lock'
    if isfile(lock_file_path):
        try:
            open(lock_file_path, 'w')
            return False
        except IOError as e:
            print("error")
            print(e)
            return True
    else:
        return False

env.basepyref['rev'] = 'revertjs'
env.basepyref['rev'] = 'revertFile'
def isAFile(name):
    file = addExtension(name, 'js')
    print(npath(file), isfile(file) or isfile(capitalize(file)))

env.basepyref['isf'] = 'isAFile'

temp = [
    "/home/kdog3682/2023/clip.html",
    "/home/kdog3682/2023/ec.html",
    "/home/kdog3682/2023/build.html",
    "/home/kdog3682/2023/ham.html",
    "/home/kdog3682/2023/hammy.html",
    "/home/kdog3682/2023/asdf.html",
    "/home/kdog3682/2023/flashcards.html",
    "/home/kdog3682/2023/t.html",
    "/home/kdog3682/2023/chatgpt-generated-html.html",
    "/home/kdog3682/2023/chatgpt.html",
    "/home/kdog3682/2023/chat.html",
    "/home/kdog3682/2023/chat2.html",
    "/home/kdog3682/2023/gpt.html",
    "/home/kdog3682/2023/index.html"
]

def imagePrompt(prompt= 'hamster snail baking cake', size=512):
    #openai
    raise Exception('the images suck. and are creepy no go')
    
    if isNumber(size):
        size = f"{size}x{size}"

    response = openai.Image.create(
      prompt=prompt,
      size=size,
      response_format='url'
    )

    url = response['data'][0]['url']
    downloadImage(url, 'gpt.png', openIt=True)

env.basepyref['gpw'] = 'gitPushWorking'



def testingvimimagePrompt(prompt= 'hamster snail baking cake', size=512):
    
    if isNumber(size):
        pass
    response = openai.Image.create(
      prompt=prompt,
      size=size,
      response_format='url'
    )

    url = response['data'][0]['url']
    downloadImage(url, 'gpt.png', openIt=True)

def vxcv():
    pass

def gitNames(dir):
    s = SystemCommand('git status --short', dir=dir).success
    pairs = unique(re.findall('(\S+) (\w+(?:\.\w+)+)', s))
    store = [[], []]
    for a,b in pairs:
        if a == 'M':
            store[0].append(b)
        else:
            store[1].append(b)
    a, b = store
    return {
        'modified': a,
        'created': b,
    }
def blackify(s):
    import black

    return black.format_str(
        s,
        mode=black.Mode(
            target_versions={black.TargetVersion.PY36}
        ),
    )


def block_to_browser(s, mode):
    # mode is implicit from visualBTB.dict
    s = re.sub('\\\\n', '\n', s)
    if not s:
        print("'no text early rert")
        return 
    if mode == 'text' or mode == 'clip':
        write('temp.txt.js', s, open=1)
    elif mode == 'email':
        email(body=s)

    elif mode == 'gdoc':
        name = prompt('what is the name for this gdoc file?')
        appscript('gdoc', name, s)

#block_to_browser('hi\nbye', mode='email')
#appscript('emailLastDocToSelf')
python()
#print(appscript('hi', 'a\nb', [1]))

#pprint("appscript('emailLastDocToSelf')", 1072)
#email(read('changelog.md'))

#cfile(budir + 'class.js11-08-2022', dir2023 + 'class.js')
#untouched 1080
