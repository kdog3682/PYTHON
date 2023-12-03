import time
import base64
import github
from base import *
from next import *


class Github:
    def seeFiles(self):
        contents = self.Repo.get_contents(
            "", ref=self.branch
        )
        print("files for", self.repo)
        pprint(map(contents, lambda x: tail(x.path)))

    def __init__(self, key=0, repo=0, private=0, **kwargs):

        key = (
            getattr(self, "user", 0)
            or getattr(self, "key", 0)
            or key
        )
        actions = getattr(self, "actions", kwargs)
        self.editIt = kwargs.pop("editIt", None)

        self.ref = env.REPOS.get(key, None)
        if self.ref:
            self.token = self.ref.get("token")
            self.github = github.Github(self.token)
            repo = (
                repo
                or getattr(self, "repo", None)
                or self.ref.get("repo")
            )
            self.user = self.ref.get("user")
        else:
            self.token = env.kdogtoken
            self.github = github.Github(self.token)
            self.user = "kdog3682"

        self.setRepo(repo)
        self.private = private
        self.isFirstTime = False

        if actions:
            for k, v in actions.items():
                m = getattr(self, k)
                if m and isFunction(m):
                    try:
                        m(v)
                    except Exception as e:
                        print(e)
                        raise Exception("error")
                        m()
                    break

        if self.isFirstTime:
            pprint(self.getInfo())
            pprint("getting info because first time")

    def getInfo(self):
        print("Getting Repository Info because firstTime")
        user = self.User
        f = lambda x: not x.fork
        repos = filter(list(user.get_repos()), f)
        return map(repos, lambda x: x.name)

    def main(self, sourceFile=0):
        def isMyScriptFile(file, githubFiles=0):
            if isUrl(file):
                return False
            name = tail(file)

            if githubFiles and name in env.jslibraries:
                return name not in githubFiles

            return name not in env.jslibraries

        def getHtmlSourceFile():
            f = mostRecent(dir2023, name="\w{2,}\.html")
            return f

        if not sourceFile:
            sourceFile = getHtmlSourceFile()
        files = getFileDependencies(sourceFile)
        files = filter(files, isMyScriptFile, self.Files)
        if len(files) > 2:
            prompt("files for upload", files)

        pprint(self.upload(files))

    def __str__(self):
        keys = ["user", "repo"]
        a = self.user
        b = self.repo
        return stringify({"user": a, "repo": b})

    @property
    def Repo(self):
        return self.Service

    @property
    def service(self):
        return self.Service

    @property
    def Service(self):
        if not hasattr(self, "_Service"):
            self._Service = self.getService(self.repo)
        return self._Service

    @property
    def User(self):
        if not hasattr(self, "_User"):
            self._User = self.github.get_user()
        return self._User

    @property
    def Files(self):
        return map(self.contents, lambda x: x.path)

    def auth(self):
        command = (
            'curl -H "Authorization: token '
            + self.token
            + '" --data \'{"name":"'
            + self.repo
            + "\"}' https://api.github.com/user/repos"
        )
        os.system(command)

    def setRepo(self, repo):
        if isString(repo):
            self.repo = repo
            self._Service = self.getService(repo)

        else:
            self._Service = repo
            self.repo = repo.name

        self.branch = self._Service.default_branch
        print(f"setting repo: {self.repo}")
        print("setting branch as", self.branch)

    def getService(self, repo):
        print("getting service for", repo)
        query = self.user + "/" + repo

        try:
            return self.github.get_repo(query)
        except Exception as e:
            log(e)
            try:
                self.isFirstTime = True
                return self.User.create_repo(
                    repo, private=self.private
                )
            except Exception as e:
                log(e)
                self.auth()
                time.sleep(2)
                return self.github.get_repo(query)

    def getFile(self, name):
        f = self.Service.get_contents(name)
        return base64.b64decode(f.content)

    def write(self, *args):
        file = args[0]
        name = tail(file)
        content = ""

        if len(args) == 1:
            if isfile(file):
                content = read(file)
                content = sub(content, vuesrc, vuescriptsrc)
                if self.editIt and not self.repo.endswith(
                    "github.io"
                ):
                    content = editSources(
                        content, self.repo
                    )
            elif isdir(file):
                return uploadDir(self.Repo, file)
            else:
                raise Exception(
                    "need a valid file or dir", file
                )
        else:
            content = textgetter(args[1])

        assert content

        if name == "clip.html":
            name = prompt(
                "Choose a file name because clip is not allowed. fallback=index.html"
            )

        elif test("^index\d+.html", name):
            name = "index.html"

        result = 0
        try:
            service = self.Service.get_contents(
                name, ref=self.branch
            )
            result = self.Service.update_file(
                service.path,
                "--",
                content,
                service.sha,
                branch=self.branch,
            )
        except Exception as e:
            result = self.Service.create_file(
                name, "--", content, branch=self.branch
            )
        print(result)
        return result

    def delete(self, file):
        server = self.Service.get_contents(file, ref="main")
        deletef = lambda f: self.Service.delete_file(
            f.path, "delete", f.sha, branch="main"
        )
        map(server, deletef)

    def upload_dir(self, dir):
        print("this is the streamlined version of upload")
        return uploadFolder(self.Repo, dir)

    def upload(self, key):
        if isArray(key):
            return map(key, lambda f: self.write(f))
        elif isObject(key):
            return map(key, lambda k, v: self.write(k, v))
        if isdir(key):
            return map(absdir(key), lambda f: self.write(f))
        elif isfile(key):
            return self.write(key)

    def openLink(self):
        return ofile(self.url)

    @property
    def url(self):
        return self.getRepo().html_url

    def getRepo(self, x=None):
        if not x:
            return self.User.get_repo(self.name)
        if isString(x):
            return self.User.get_repo(x)
        else:
            return x

    def deleteRepo(self, repo=0):
        repo = self.getRepo(repo)
        r = "kdog3682|2023"
        if test(r, repo.name):
            print(f"Forbidden Deletion: {repo.name}")
            return
        elif test("github.io", repo.name):
            if not prompt(
                repo.name,
                "are  you sure you want to delete?",
            ):
                print(f"Forbidden Deletion: {repo.name}")
                return

        repo.delete()
        print("deleting repo", repo.name)

    def getContents(self):
        try:
            return self.Service.get_contents("")
        except Exception as e:
            print("@getContents: empty repo", self.name)
            return []

    @property
    def contents(self):
        return self.getContents()

    load = setRepo

    @property
    def repos(self):
        return self.User.get_repos()

    @property
    def name(self):
        return self.repo

    def deleteForks(self):
        for repo in self.repos:
            self.deleteRepo(repo)

    def printRepo(self, repo):
        def getTime(f):
            strife = "%a, %d %b %Y %H:%M:%S GMT"
            date = f._headers.get("date")
            return datetime.strptime(date, strife)

        def runner(file):
            return {
                "path": file.path,
                "time": getTime(file),
            }

        self.load(repo)
        contents = self.getContents()
        if contents:
            store = map(contents, runner)
            pprint(store)
        elif prompt(
            f"delete {self.name} because it is empty repo?"
        ):
            self.deleteRepo(self.name)


class MyPublicRepo(Github):
    user = "kdog3682"
    repo = "public"


class UploadJsbinCss(MyPublicRepo):
    actions = {
        "upload": {
            "jsbin2.css": "clip.js",
        }
    }


class Github2:
    def __init__(self):
        self.token = env.kdog_github_token
        self.github = github.Github(self.token)

    def clone_repo(self, path, dir):
        dir = rootdir + dir
        dprompt("cloning path to dir", path, dir)
        repo = self.github.get_repo(path)
        SystemCommand(f"git clone {repo.clone_url} {dir}")
        logfile(dir)

    def set_repo(self, path):
        self.repo = self.github.get_repo(path)
        self.branch = self.repo.default_branch
        return self.repo

    def get_repo_contents(self, path="", **kwargs):
        contents = self.repo.get_contents(
            path, ref=self.branch
        )

        if kwargs.get("filter"):
            f = lambda x: tail(x.path) == kwargs.get(
                "filter"
            )
            return filter(contents, f)
        if kwargs.get("find"):
            f = lambda x: tail(x.path) == kwargs.get("find")
            return find(contents, f)

        return contents

    def _download_repo_src_contents(self, contents):
        def runner(item):
            path = item.path
            name = tail(path)
            src = self.get_repo_contents(path, find="src")
            assert src
            target = self.get_repo_contents(
                src.path, find="index.ts"
            )
            if target:
                return [name, get_text(target)]

        store = map(contents, runner)
        s = ""
        for k, v in store:
            s += comment("file: " + k)
            s += "\n"
            s += v
        write("repo.temp.json", store)
        write("repo.temp.js", s, open=1)

    def download_repo_contents(self, path, target=""):
        dirName = tail(path)
        self.set_repo(path)
        contents = self.get_repo_contents(target)
        if some(contents, lambda x: tail(x.path) == "src"):
            print("setting to src")
            contents = self.get_repo_contents("src")

        elif every(contents, lambda x: x.type == "dir"):
            return self._download_repo_src_contents(
                contents
            )

        def runnerA(item):
            if item.type == "dir":
                return runnerB(
                    self.get_repo_contents(item.path)
                )
            elif ignore(item.path):
                return
            else:
                return item

        def runnerB(contents):
            return map(contents, runnerA)

        store = runnerB(contents)
        files = flat(store)
        paths = map(files, "path")
        names = map(paths, tail)
        dir = mkdir(dldir + dirName)
        filepaths = map(
            names, lambda name: npath(dir, name)
        )
        dprompt(files, paths, names, dir)
        logfile(filepaths)

        for i, filepath in enumerate(filepaths):
            write(filepath, get_text(files[i]))


def get_repo_files_from_url(url):

    log = createLogger()

    def parseContent(content):
        name = tail(content.path)
        if ignoreFile(name) or isImage(name):
            return

        log(name)

        try:
            text = content.decoded_content.decode("utf-8")
            return {"file": name, "content": text}
        except Exception as e:
            print("Error", name, str(e))

    def parse(s):
        s = re.sub(".*?github.com/", "", s)
        parts = s.split("/")
        if len(parts) == 2:
            parts.append("")
            return parts
        else:
            return [parts[0], parts[1], "/".join(parts[4:])]

    user, repo, start = parse(url)
    g = github.Github()
    repo = g.get_repo(f"{user}/{repo}")
    ref = repo.default_branch
    contents = None
    try:
        contents = repo.get_contents(start, ref=ref)
    except Exception as e:
        dprompt(
            repo,
            ref,
            start,
            'the error is most likely with the start. One time in the past, for "https://github.com/vadimdemedes/thememirror/tree/main/source/themes", the start should have been "source/themes", but the parse only took themes',
        )
        raise e
        assert contents

    store = []

    while contents:
        content = contents.pop(0)
        if content.type == "dir":
            contents.extend(
                repo.get_contents(content.path, ref=ref)
            )
        else:
            push(store, parseContent(content))

    return store


# https://github.com/nbremer/freshdatashapes/tree/gh-pages/slides
def get_repo_files(user, repo=0, start="", mode=""):
    if start == "root":
        start = ""
    if not repo:
        user, repo = split(user, "/")

    g = github.Github()
    repo = g.get_repo(f"{user}/{repo}")
    default_branch = repo.default_branch
    contents = repo.get_contents(start, ref=default_branch)
    prompt(
        repo=repo,
        contents=contents,
        message="starting... press anything to continue",
    )
    files = []
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            print("path", file_content.path)
            contents.extend(
                repo.get_contents(
                    file_content.path, ref=default_branch
                )
            )
        else:
            files.append(file_content)

    if mode == list:
        # files = (files, ignore=env.jslibraries)
        f = lambda x: x.decoded_content.decode("utf-8")
        for file in files:
            name = tail()
        s = join([f(x) for x in files])
        clip(s)
        return

    if mode == dict:
        f = lambda x: x.decoded_content.decode("utf-8")
        s = join([f(x) for x in files])
        clip(s)
        return

    if mode == str:
        f = lambda x: x.decoded_content.decode("utf-8")
        s = join([f(x) for x in files])
        clip(s)
        return

    return [file.path for file in files]


def jsdelivr(file, src=0, user=0, repo=0):
    if src:
        src = re.sub("/$", "", src)
    elif user:
        src = f"{user}/{repo}"
    else:
        url = f"https://cdn.jsdelivr.net/gh/{file}"
        clip(url)
        return
        return ofile(url)

    url = f"https://cdn.jsdelivr.net/gh/{src}/{file}"
    ofile(url)


def github_file_url(
    file, src="", user="kdog3682", repo="codemirror"
):
    if src:
        user, repo = src.split("/")
    url = "https://raw.githubusercontent.com/$1/$2/main/$3"
    url = templater(url, [user, repo, file])
    return url


def plf():
    f = glf()
    print(fileInfo(f))
    print(read(f))


def github_usercontent_url2(s):
    s = re.sub(
        "blob/(master|main)",
        lambda x: x.group(1),
        s,
        count=1,
    )
    s = re.sub(
        "github.com",
        "raw.githubusercontent.com",
        s,
        count=1,
    )
    return s


s = """
box
reset
"""


def create_new_repo(dir, private=False):
    name = tail(dir).lower()
    dprompt(name, dir, "creating a new repo for name @ dir")

    g = Github(repo=name)
    g.service.edit(private=private)

    SystemCommand(
        f"""
        git init 
        git branch -m master main
        git add .
        git remote add origin git@github.com:kdog3682/{name}.git
        git commit -m "Initial commit"
        git push -u origin main
    """,
        dir=dir,
    )

    url = "https://github.com/kdog3682/" + name
    ofile(url)


def log(x):
    try:
        print(x, "error")
    except Exception as e:
        pass


def get_text(x):
    return x.decoded_content.decode("utf-8")


def ignore(x):
    ignore = [
        "ts",
        "tsx",
        "css",
        "html",
    ]

    if isString(x):
        if x in env.fileignore:
            return True
        if getExtension(x) in ignore:
            return True
    return False


def upload(files):
    Github(
        key="kdog3682",
        repo="kdog3682.github.io",
        upload=files,
    )


def brooklyn(s=None, file="codeground.html"):
    if not s:
        s = longstamp()
    Github(key="brooklyn", upload={file: s})
    ofile("https://brooklynlearning.github.io/codeground")


# create_new_repo(markdowndir) # wonderful


def uploadHammy(upload):
    Github(key="hammy", upload=upload)
    Github(key="hammy0", upload=upload)


hammyV1 = """


<style>
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    outline: none;
  }
  body,
  html {
    height: 100%;
    width: 100%;
    font-family: sans;
  }
  html {
    font-size: 12pt;
  }
  body {
    position: relative;
  }
</style>

<style>
  .boxed-number {
    display: flex;
    column-gap: 24pt;
  }

  .left {
    color: #64b5f6;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    width: 16pt;
    height: 16pt;
    margin: auto 0;
  }

  .right {
    margin: auto 0;
  }
</style>

<style>
  .v-modal {
    padding: 5pt;
    text-align: center;
    font-size: 16pt;
    font-weight: bold;
  }

  .error {
    background: #ef9a9a;
    border: 0.5px solid #e57373;
  }

  .success {
    background: #a5d6a7;
    border: 0.5px solid #81c784;
  }
</style>

<body>
  <div class="vndy">
    <div style="padding: 40pt; background: rgb(100, 181, 246)">
      <div
        style="
          background: white;
          position: relative;
          padding: 20pt;
          border-radius: 10pt;
        "
      >
        <div
          style="
            justify-content: space-between;
            display: flex;
            width: 100%;
            padding: 10pt;
          "
        >
          <h1>Still Under Construction</h1>
          <h2
            style="
              padding-left: 20pt;
              padding-right: 20pt;
              color: rgb(100, 181, 246);
            "
          >
            Hammy Math
          </h2>
        </div>
        <div style="margin-top: 24pt; margin-bottom: 24pt; padding: 10pt">
          <div class="text-container" style="margin-bottom: 30pt">
            <p style="margin-bottom: 3pt">Hi everyone,</p>
            <p style="margin-bottom: 3pt">
              Mr. Lee is still working on Hammy's website, but it is not ready
              yet.
            </p>
            <div style="margin-bottom: 3pt">
              Hopefully a few more days, and everything will be ready.
            </div>
          </div>
        </div>
        <div class="v-list">
          <div class="v-numbered boxed-number">
            <div class="left">1</div>
            <div class="right">
              <div
                class="file-tab"
                style="
                  border-bottom: 0.5px solid rgb(25, 118, 210);
                  border-top: 0.5px solid rgb(25, 118, 210);
                  width: fit-content;
                  display: flex;
                  align-items: center;
                  column-gap: 12pt;
                "
              >
                <p style="color: rgb(25, 118, 210); font-weight: bold">
                  April 1st, 2023
                </p>
                <p>Extra Math Assignment 1 - Still Under Construction</p>
                <button
                  class="open-url"
                  style="
                    border-radius: 5pt;
                    padding: 3pt 10pt;
                    color: white;
                    font-weight: bold;
                    background: rgb(100, 181, 246);
                  "
                >
                  open
                </button>
              </div>
            </div>
          </div>
          <div class="v-numbered boxed-number">
            <div class="left">2</div>
            <div class="right">
              <div
                class="file-tab"
                style="
                  border-bottom: 0.5px solid rgb(25, 118, 210);
                  border-top: 0.5px solid rgb(25, 118, 210);
                  width: fit-content;
                  display: flex;
                  align-items: center;
                  column-gap: 12pt;
                "
              >
                <p style="color: rgb(25, 118, 210); font-weight: bold">
                  April 8st, 2023
                </p>
                <p>Extra Math Assignment 2 - Still Under Construction</p>
                <button
                  class="open-url"
                  style="
                    border-radius: 5pt;
                    padding: 3pt 10pt;
                    color: white;
                    font-weight: bold;
                    background: rgb(100, 181, 246);
                  "
                >
                  open
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div
      class="v-contact-fourth-grade"
      style="
        padding: 60pt;
        background: rgb(100, 181, 246);
        color: white;
        height: 50vh;
      "
    >
      <h1 style="margin-bottom: 12pt">Contact</h1>
      <p style="padding-bottom: 12pt; font-weight: bold">
        Hammy and Sammy are busy baking cakes at the moment.
      </p>
      <p class="available">Mr. Lee is available.</p>
      <p>
        <span>You can always email Mr. Lee at</span>
        <span style="font-weight: bold"
          ><a href="kevinlulee1@gmail.com">kevinlulee1@gmail.com</a></span
        >
      </p>
    </div>
  </div>
</body>
"""

# uploadHammy({'version1.html': hammyV1})
# clip(get_repo_files_from_url('https://github.com/nbremer/freshdatashapes/tree/gh-pages/slides'))


def upload_kdog3682_main(files):
    Github(
        key="kdog3682",
        repo="kdog3682.github.io",
        upload=files,
    )


def browse(
    file_name=0, reponame=0, username="kdog3682", filter=0
):

    g = github.Github(env.kdogtoken)
    user = g.get_user(username)
    if not reponame:
        repos = user.get_repos()
        names = [repo.name for repo in repos]
        pprint(names)
        reponame = choose(names)[0]

    url = f"{username}/{reponame}"
    repo = g.get_repo(url)
    branch = repo.default_branch
    try:
        contents = repo.get_contents("", ref=branch)
    except Exception as e:
        print(e)
        return browse()

    names = [tail(content.path) for content in contents]
    if filter:
        names = [
            name
            for name in names
            if test(filter, name, flags=re.I)
        ]

    chosenNames = choose(names)
    for content in contents:
        name = tail(content.path)
        if name in chosenNames:
            text = content.decoded_content.decode("utf-8")
            if isfile(name):
                print(
                    "skipping because exists on disk",
                    name,
                    "writing as clip.js",
                )
                clip(text)
            else:
                path = (
                    "/mnt/chromeos/MyFiles/Downloads/"
                    + name
                )
                write(path, text)
                save(path)
                # saves to saved.txt


# browse(reponame='2023', filter='color')


# "https://hammymathclass.github.io"


# s = 'https://github.com/vadimdemedes/thememirror/tree/main/source/themes'
# clip(get_repo_files_from_url(s))


def pushContent(repo, file, content):
    branch = repo.default_branch
    try:
        return repo.create_file(
            path=file,
            message=f"Upload {file}",
            content=content,
            branch=branch,
        )
    except Exception as error:
        el = repo.get_contents(file, ref=branch)
        print(el)
        return repo.update_file(
            path=el.path,
            message="Update file content",
            content=content,
            sha=el.sha,
            branch=branch,
        )


def pushFile(repo, file, to):
    branch = repo.default_branch
    with open(file, "rb") as file_content:
        content = file_content.read()
        try:
            repo.create_file(
                path=to,
                message=f"Upload {file}",
                content=content,
                branch=branch,
            )
            return True
        except Exception as error:
            if str(error).startswith('Invalid Request'):
                print('hi')
            val = error.value
            dprompt2(error, val)
            el = repo.get_contents(to, ref=branch)
            repo.update_file(
                path=el.path,
                message="Update file content",
                content=content,
                sha=el.sha,
                branch=branch,
            )
            return True


def iterateDir(dir, fn, dirname=0):
    if not dirname:
        dirname = tail(dir)
    for root, _, files in os.walk(dir):
        for file in files:
            a = os.path.join(root, file)
            b = os.path.join(
                dirname, os.path.relpath(a, dir)
            )
            fn(a, b)

def uploadFolder(repo, folder):
    def runner(a, b):
        pushFile(repo, a, b)

    iterateDir(folder, runner)

    def reader(item):
        date = item.last_modified
        path = item.path

    getRepoContents(repo, fn=reader)

def uploadDir(repo, dir):
    outdir = tail(dir)
    branch = repo.default_branch
    for root, _, files in os.walk(dir):
        for file in files:
            path = os.path.join(root, file)
            remote_path = os.path.join(
                outdir, os.path.relpath(path, dir)
            )

            with open(path, "rb") as file_content:
                content = file_content.read()
                try:
                    repo.create_file(
                        path=remote_path,
                        message=f"Upload {file}",
                        content=content,
                        branch=branch,
                    )
                except:
                    try:
                        el = repo.get_contents(
                            remote_path, ref=branch
                        )
                        print(el)
                        repo.update_file(
                            path=el.path,
                            message="Update file content",
                            content=content,
                            sha=el.sha,
                            branch=branch,
                        )
                        print("success", file)
                    except Exception as e:
                        print(str(e))


def upload_kdog3682_test():
    repo = "magicscript"
    dir = "/home/kdog3682/2023/dist/"
    # index = '/home/kdog3682/2023/dist/index2.html'
    g = Github(
        key="kdog3682", repo=repo, upload=dir, editIt=1
    )
    g.seeFiles()
    # g.openLink()


def editSources(s, repo):
    return sub(s, "/assets", "/" + repo + "/assets")



# upload_kdog3682_test()

def create_lorem_dir():
	
    g = Github(
        key="kdog3682", repo="projects", upload_dir=dir
    )

def create_project():
    dir = "/home/kdog3682/2023/dist/"
    dir = "/home/kdog3682/2023/sample-project/"
    g = Github(
        key="kdog3682", repo="projects", upload_dir=dir
    )
    ''' the file is uploaded as directory inside /projects '''
    ''' the key is the relative pathing '''


def create_local_sample_project():

    dir = "/home/kdog3682/2023/sample-project/"
    mkdir(dir)
    chdir(dir)
    src = "./abc.js"
    s = f"""<!DOCTYPE html><html lang="en">\n<script src="https://cdnjs.cloudflare.com/ajax/libs/vue/2.6.14/vue.min.js" integrity="sha512-XdUZ5nrNkVySQBnnM5vzDqHai823Spoq1W3pJoQwomQja+o4Nw0Ew1ppxo5bhF2vMug6sfibhKWcNJsG8Vj9tg==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>\n<script src="{src}"></script> <body> <div id="app">howdy</div> </body></html>"""
    write("index.html", s)
    write("abc.js", "document.write('howdy from abc.js')")
    printdir(dir)
    ofile("index.html")


def getRepoContents(repo, start='', fn=identity):
    if isString(repo):
        repo = getRepo(repo)

    store = []
    ref = repo.default_branch
    contents = repo.get_contents(start, ref=ref)

    while contents:
        content = contents.pop(0)
        if content.type == "dir":
            items = repo.get_contents(content.path, ref=ref)
            contents.extend(items)
        else:
            push(store, fn(content))
    return store

#create_project()


def getRepo(repo):
    g = Github(key="kdog3682", repo=repo)
    return g.Repo

def deleteContent(repo, content):
    return repo.delete_file(
        path=content.path,
        message=f'Delete {content.name}',
        sha=content.sha,
        branch=repo.default_branch
    )

def deleteProject(reponame, projectname):
    repo = getRepo(reponame)
    contents = repo.get_contents(projectname)
    branch=repo.default_branch

    for content in contents:
        if content.type == 'file':
            deleteContent(repo, content)

    repo.delete_file(
        path=project,
        message=f'Delete folder {project}',
        sha=contents[0].sha,
        branch=branch
    )
    print(f'Folder "{folder_path}" and its contents have been deleted.')

def deleteRepoFiles(self, repoName):

    self.setRepo(repoName)
    contents = self.getRepoContents()
    targets = choose(contents)

    for content in targets:
        self.repo.delete_file(
            path=content.path,
            message=f'Delete {content.name}',
            sha=content.sha,
            branch=repo.default_branch
        )

def cleanupRepo(reponame):
     repo = getRepo(reponame)
     contents = getRepoContents(repo)
     chosen = chooseMultiple(contents)
     prompt(chosen)
     for content in chosen:
         print(deleteContent(repo, content))


def updateRepo(reponame, index=None, readme=None):
     repo = getRepo(reponame)
     if index:
         print(pushContent(repo, 'index.html', read(index)))
     if readme:
         print(pushContent(repo, 'readme.md', read(readme)))

