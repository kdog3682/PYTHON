from base import *
import time
import inspect
import env

APPS = []
APPS.append({'name': 'k5learning', 'description': 'Reads DLDIR for the most recent file group. Maps the group by deleting the last page. Merges the pdfs together'})
APPS.append({'name': 'k5learning', 'description': 'Reads DLDIR for the most recent file group. Maps the group by deleting the last page. Merges the pdfs together'})

def runApps():
    ref = choose(APPS)
    fn = ref.get('fn', globals().get(ref.get('key'), None))
    print({'fn': fn})


def main(override=0):

    """ file: run.py
        this is the primary accessor function 
        for touching other files 
        it only connects to _python
        from base import *
    """

    if isMacbook():
        global drivedir
        drivedir = "~/Google\ Drive"
        runMacbook()

        """ 
            print: print the most recent files
            move: move the most recent files to ~/
            execute: execute the most recent python file
         """
    if override:
        python(override)
    elif len(sys.argv) > 1:
        try:
            python()
        except KeyboardInterrupt as e:
            print('done via keyboard')

        """ only runs if sys.argv is active """
    else:
        print('no run because not from shell')

def email(to=0, subject='', body='', files=0, debug=0):
    if debug:
        body = files
        to = 'self'
        ids = None

    elif files:
        files = toArray(files)
        from ga import GoogleDrive
        drive = GoogleDrive()
        ids = map(files, drive.uploadFile)
        if not body:
            body = files

    emailBody = {
        'attachments': ids,
        'from': env.EmailContacts.get('self'),
        'to': env.EmailContacts.get(to or 'self'),
        'body': body,
        'subject': subject,
    }
    if debug:
        prompt(emailBody)
    googleAppScript("Action2", "email", emailBody)

def emailLastFile():
    email(subject='last file', files=glf())


def python(override=0):
    if override:
        arg = override
        args = []
    else:
        baseArgs = sys.argv[1:]
        arg, args = splitonce(map(baseArgs, shellunescape))

    if arg.endswith("dir") and isdir(eval(arg)):
        return printdir(eval(arg))

    basepyref = env.basepyref
    env.basepyref['fp'] = "filePicker"
    basepyref["google"] = "google @string"
    basepyref["twil"] = "sendTwilio @string"

    key = basepyref.get(arg, arg)
    key = re.sub("^:", "", key)
    key, config = mget("@(\w+)", key)
    #print({'key':key, 'config':config})

    fn = globals().get(key)
    if not fn:
        return print("no fn")

    value = 0
    if config.get("string"):
        args = " ".join(args)
        value = fn(args)

    elif len(args) > 0:
        availableAmount = countArgs(fn)
        print(availableAmount)
        if availableAmount == 1:
            print('only one arg')
            value = fn(args[0])
        else:
            value = fn(*args)
    else:
        print('ddd no args')
        value = fn()

    pprint(
        {
            "caller": key,
            "success": "Yes!",
            "args": args,
            "value": value,
        }
    )


def uploadMaterials(official=1, dontEmail=0):
    from ga import GoogleClassroom, GoogleDrive
    chdir(dldir)
    #------------------------------------------------
    data = cwtBuildNecessaryFiles()
    prompt('status', official, 'file-data', data)
    store = []

    for item in data.get("classFiles"):
        key = item.get("key") if official else 'emc'
        files = item.get("files")
        room = GoogleClassroom(key)
        results = map(files, room.uploadAssignment)
        store.extend(results)

    if dontEmail:
        pprint(store)
        print('dont email so early return')
        return 
    #------------------------------------------------
    extraFiles = data.get("extraFiles")
    individualFiles = data.get("individualFiles")
    extraItems = filter([extraFiles, individualFiles])

    if official and extraItems:
        drive = GoogleDrive()
        for group in extraItems:
            for file in group:
                fileId = drive.uploadFile(file)
                store.append({"id": fileId, "name": file})
    #------------------------------------------------
    def getSubject(subject = 'G4/G5', topic = 'Math'):
        date = upcomingDate('saturday')
        return f"{subject} {topic} Materials {date}"
    #------------------------------------------------

    files = map(store, lambda x: removeExtension(x.get('name')))
    attachments = map(store, lambda x: x.get('id'))
    to = env.workEmail if official else env.myEmail
    payload = {
        "subject": getSubject(),
        "data": store,
        "attachments": attachments,
        "files": files,
        "to": to,
    }
    #------------------------------------------------

    answer = prompt('uploaded all materials', payload, 'confirm?', 'Type anything to continue', 'Type G to run the script again as OFFICIAL')
    if not official and answer == 'G':
        uploadMaterials(official=1)
    else:
        googleAppScript("Action", "courseWork", payload)

def cwtBuildNecessaryFiles(grades=[4, 5]):

    extraFiles = [
        #"G4 & G5 Math Report Cards.pdf",
        #"G4 & G5 Online Report Cards.pdf",
        #"Announcements",
        #"Progress Reports",
        #"Midterm 1 Scores",
        #"Final Exam Scores",
        #"Report Cards",
    ]
    baseFiles = [
        "Final Exam",
        "Practice Exam",
        "Homework",
        "Classwork",
        "Quiz",
        #"Final Exam Review",
        #"Warmup",
        #"Handout Packet 1",
        #"Handout Packet 2",
        #"Handout Packet 3",
        #"Midterm Exam Review",
        #"Midterm Exam",
        #"Handout",
        #"Extra Worksheets",
        #"Quarter 1 Exam",
        #"Announcement",
    ]

    changers = {
        'g5r.pdf': 'Grade 5 Final Exam Review.pdf',
        'g4r.pdf': 'Grade 4 Final Exam Review.pdf',
        'g5hw.pdf': 'Grade 5 Homework.pdf',
        'g4hw.pdf': 'Grade 4 Homework.pdf',
        'g5cw.pdf': 'Grade 5 Classwork.pdf',
        'g4cw.pdf': 'Grade 4 Classwork.pdf',

        'g5q.pdf': 'Grade 5 Quiz.pdf',
        'g4q.pdf': 'Grade 4 Quiz.pdf',
        'WG5Q1.pdf': 'Grade 5 Quiz.pdf',
        'WG4Q1.pdf': 'Grade 4 Quiz.pdf',
    }

    for file, destination in changers.items():
        if isfile(file) and not isRecent(destination, days=1):
            mfile(file, destination)

    storage = Storage()

    p1 = 'Grade '
    p2 = 'G'
    for file in baseFiles:
        file = toPdf(file)
        for grade in grades:
            a = str(grade) + " " + file
            if isRecent(p1 + a, days=1):
                storage.add(grade, p1 + a)
            elif isRecent(p2 + a, days=1):
                storage.add(grade, p2 + a)

    items = storage.toJSON().items()
    classFiles = [
        {"key": str(k), "files": v} for k,v in items
    ]
    extraFiles = filter(map(extraFiles, toPdf), isfile)
    data = {
        "classFiles": classFiles,
        "extraFiles": extraFiles,
    }
    return data


e = env.basepyref
e['em'] = 'email'
e['um'] = 'uploadMaterials'
e['mr'] = 'mostRecentDirectoryFiles'
e['apps'] = 'runApps'
e['rev'] = 'revertFile'
e['rr'] = 'replyReddit'
e['rjs'] = 'redditFromJS'
e['eod'] = 'endOfDay'

def replyReddit():
    from redditscript import Reddit
    reddit = Reddit()
    reddit.reply_all_comments()
    print('done replying to comments')

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
            print(o, 'error')
            pass
    
    print('done')
    return 
    a = choose(map(items, 'title'), auto=0)
    print('hii', a)
    if not a:
        return 
    for s in submissions:
        if s.title in a:
            s.delete()
            print('deleting', s.title)



def countArgs(f, *args, **kwargs):
    data = inspect.signature(f)
    params = data.parameters
    s = str(data)
    if '*' in s:
        return 255
    return len(params)

def gitDelete(file):
    cmd = f"""
        git rm {file}
        git commit -m "REMOVE {file}"
        git push
    """

    SystemCommand(cmd)

def gitPush(file = None, message='automated git push'):
    if file:
        message = prompt(file, 'upload message: ')
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

        cleandir(dir2023)
        time.sleep(1)
        time.sleep(1)
        mainCommand = f"""
            cd {dir2023}
            git add .
            git commit -m "{gitNames(dir2023)}"
            git push
        """
    SystemCommand(mainCommand)

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
    pushStatement = "git push -u origin main" if firstTime else "git push"
    if remove:
        gitMode = 'git rm '
        moveStr = ''
        if not message: message = 'automated git remove'
    elif move:
        gitMode = 'git mv '
        moveStr = ' ' + move
        if not message: message = 'automated git move'
    elif push:
        gitMode = 'git add '
        moveStr = ''
        if not message: message = 'automated git push'

    lines = []
    if dir:
        lines.append(f"cd {dir}")


    if files:
        for file in files:
            lines.append(gitMode + tail(file))
    elif file:
        lines.append(gitMode + tail(file) + moveStr)
    elif push:
        lines.append('git add .')
        message = 'automated git push everything'


    lines.append(f"git commit -m \"{message}\"")
    lines.append(pushStatement)
    cmd = join(lines)
    #return print('debugging', cmd)
    SystemCommand(cmd)


#gitManager(files=['a.js', 'b.js'], remove=1)
env.basepyref['gp'] = 'gitPush'
env.basepyref['gd'] = 'gitDelete'
env.basepyref['elf'] = 'emailLastFile'

#files = sort(ff(pdfdir2, hours=13), mdate)
#email(to='work', subject='Additional G4 Materials', files=files, debug=0)

def gitInit():

    dir = pydir
    repo = tail(dir)
    user = 'kdog3682'
    gitIgnore = """
        .gitignore
        env.py
        __pycache__
    """

    chdir(dir)
    if not isfile('.gitignore'):
        write('.gitignore', smartDedent(gitIgnore))
        from githubscript import Github
        Github(key = user, repo = repo)

    res = SystemCommand(f"""
        git init
        git add .
        git commit -m "push everything"
        git remote add originpython git@github.com:{user}/{repo}
        git push -u originpython main
    """, dir=dir)

    print(res)
    #ofile(f"https://github.com/{user}/{repo}")

def gitNames(dir):
    cmd = 'git diff --name-status'
    cmd = 'git status'
    names = SystemCommand(cmd, dir=dir).success
    return names

env.basepyref['gi'] = 'gitInit'
main()
gitInit()
