chatgptjsonfile = '/home/kdog3682/2023/chatgpt.json'
departurejsonfile = '/home/kdog3682/2023/departures.json'


from base import *
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

def email(to=0, subject="", body="", files=0, debug=0):
    if debug:
        body = files
        to = "self"
        ids = None

    elif files:
        files = toArray(files)

        drive = GoogleDrive()
        ids = map(files, drive.uploadFile)
        if not body:
            body = files

    emailBody = {
        "attachments": ids,
        "from": env.EmailContacts.get("self"),
        "to": env.EmailContacts.get(to or "self"),
        "body": body,
        "subject": subject,
    }
    if debug:
        prompt(emailBody)
    googleAppScript("Action2", "email", emailBody)


def emailLastFile():
    email(subject="last file", files=glf())

def yuma(a, b, c):
    dprint(a, b, c)


def python(argv = sys.argv[1:]):
    if not argv:
        return print("requires shell")

    key, *args = argv
    args = map(list(args), shellunescape)
    key = env.basepyref.get(key, key)
    fn = globals().get(key)
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

def buildFiles():
    regex = reWrap(cwtFileDict)
    files = ff(dldir, week=1, pdf=1, regex=regex, flags=re.I, antiregex='test.pdf')

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



def uploadMaterials(skipClassroom=0, skipEmail=0, official=1, fileData=0):
    from ga import GoogleClassroom, GoogleDrive

    data, misc, all = fileData or buildFiles()
    assert data
    store = []

    for item in data:
        key = item.get("key") if official else "emc"
        files = item.get("files")
        room = GoogleClassroom(key)
        room.skipClassroom = skipClassroom 
        results = map(files, room.uploadAssignment)
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
    clear(departurejsonfile)

def cwtBuildNecessaryFiles(grades=[4, 5]):
    print("'this is kind of deprecated ... as the systems get better and better")

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


def gitPushObject(obj):
    if obj['ext'] != 'js':
        print('only pushing js at the moment')
        return 

    message = obj['line'].strip()
    dir = dir2023
    mainCommand = f"""
        cd {dir}
        git add .
        git commit -m "{message}"
        git push
    """

    success = SystemCommand(mainCommand, dir=dir).success
    if success and not test('nothing to commit', success, flags=re.I):
        ofile(gitUrl(dir))



    print(obj)

def gitPush(file=None, dir=dir2023):
    if file and isfile(file):
        if getExtension(file) == 'py':
            dir = pydir
        message = prompt('running gitPush', pydir, file, "upload message: ")

        a, b = os.path.split(file)
        if not a or len(a) < 2:
            a = dir2023

        mainCommand = f"""
            cd {a}
            git add {b}
            git commit -m "{message}"
            git push
        """
    else:
        fallbackMessage = 'howdy autopush'
        message = None
        if file:
            message = file

        if dir == dir2023:
            print("cleaning dir2023")
            cleandir(dir2023)
            time.sleep(1)

        nameObject = gitNames(dir)

        time.sleep(1)
        mainCommand = f"""
            cd {dir}
            git add .
            git commit -m "'{message or fallbackMessage }'"
            git push
        """

    response = SystemCommand(mainCommand, dir=dir)
    gitData = {
        'success': response.success,
        'error': response.error,
    }
    logger(**nameObject, action='gitpush', message=message, gitData=gitData)


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


env.basepyref["gp"] = "gitPush"
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
        'fn': lambda state: unzip(state.file, state.name)
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
    items = split(smartDedent(env.pac), '\n\n+')
    cmd = dollarPrompt(items, python=True)
    cmd = addPythonImports(cmd)
    dprint(cmd)
    exec(cmd)

def googleAppController():
    items = split(smartDedent(env.gac), '\n+')
    s = dollarPrompt(items)
    return googleAppScript(f"Finish({s})")

    name, args, kwargs = getNameArgsKwargs(s)
    command = stringCall('Action2', quote(name), kwargs, *args)
    pprint(dict(command=command))
    return googleAppScript(command)


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


python()
#smartManager()

#runChatgpt("""
#Explain what the function below does:
#def copyToBrowser(s):
    #return write(dldir + 'ofile.js', removeComments(s).strip(), 1)
#""")

