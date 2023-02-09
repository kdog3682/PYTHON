from base import *
import time
import inspect
import env



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


def buildFiles():
    base = ff(dldir, week=1, pdf=1)
    files = Partitioner2(base)()

    storage = Storage()

    for file in files:
        k = search('g(?:rade)? *(\d+)', file, flags=re.I)
        assert k
        storage.add(k, file)

    store = []
    for k,v in storage.toJSON().items():
        store.append({
            'key': k,
            'files': sort(v, sortCwtFiles),
        })
    return store

def uploadMaterials(skipClassroom=0, skipEmail=0, official=1):
    from ga import GoogleClassroom, GoogleDrive

    data = buildFiles()
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

    prompt(payload)
    googleAppScript("Action", "courseWork", payload)

def cwtBuildNecessaryFiles(grades=[4, 5]):

    extraFiles = [
        # "G4 & G5 Math Report Cards.pdf",
        # "G4 & G5 Online Report Cards.pdf",
        # "Announcements",
        # "Progress Reports",
        # "Midterm 1 Scores",
        # "Final Exam Scores",
        # "Report Cards",
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
    print("hii", a)
    if not a:
        return
    for s in submissions:
        if s.title in a:
            s.delete()
            print("deleting", s.title)


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
    if file:
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
        if dir == dir2023:
            print("cleaning dir2023")
            cleandir(dir2023)
            time.sleep(1)

        message = gitNames(dir)
        print({"m": message})

        time.sleep(1)
        mainCommand = f"""
            cd {dir}
            git add .
            git commit -m "{message}"
            git push
        """

    success = SystemCommand(mainCommand, dir=dir).success
    if success and not test('nothing to commit', success, flags=re.I):
        ofile(gitUrl(dir))


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


# gitManager(files=['a.js', 'b.js'], remove=1)
env.basepyref["gp"] = "gitPush"
env.basepyref["gd"] = "gitDelete"
env.basepyref["elf"] = "emailLastFile"

# files = sort(ff(pdfdir2, hours=13), mdate)
# email(to='work', subject='Additional G4 Materials', files=files, debug=0)


def gitNames(dir):
    cmd = "git diff --name-status"
    names = SystemCommand(cmd, dir=dir).success
    return names


def gitPushPython():
    gitPush(dir=pydir)


def gitUrl(dir):
    repo = tail(dir)
    return f"https://github.com/{env.githubUser}/{repo}"


env.basepyref["gi"] = "gitInit"
env.basepyref["gpy"] = "gitPushPython"
env.basepyref["fp"] = "filePicker"
#env.basepyref["google"] = "google @string"
#env.basepyref["twil"] = "sendTwilio @string"


def gitPushAll():
    gitPushPython()
    gitPush()

def PythonController(**kwargs):
    file = os.path.abspath(apps.__file__)
    keys = astFunctions(file)
    key = choose(keys, mode=1)
    fn = getattr(apps, key)
    fn()

env.basepyref['gpa'] = 'gitPushAll'
# gitInit()
# print(ofile(gitUrl(pydir)))
# print(isRecent(glf(), days=1))

def astFunctions(file):
    # cute but not necessary

    import ast
    def getFunctions(body):
        return (f for f in body if isinstance(f, ast.FunctionDef))
    tree = ast.parse(read(file))
    return unique([f.name for f in getFunctions(tree.body)])

#PythonController()

def smartManager():
    file = glf()
    name = removeExtension(file)
    e = getExtension(file)
    if False:
        pass

    elif name == 'online-document':
        unzip(file, mathchadir)
    elif e == 'zip':
        unzip(file, name)
    elif test('resume', name, flags=re.I):
        mfile(file, 'Kevin Lee resume.pdf')

#smartManager()


def pipInstall(s):
    cmd = 'abc ' + s
    print(cmd)

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
    print(cmd, 'hii')
    exec(cmd)

def googleAppController():
    items = split(smartDedent(env.gac), '\n+')
    s = dollarPrompt(items)
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
python()
