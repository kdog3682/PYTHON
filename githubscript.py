import time
import base64
import github
from base import *

class Github:

    def __init__(
        self,
        key=0,
        repo=0,
        private=0,
        **kwargs
    ):

        key = getattr(self, 'user', 0) or getattr(self, 'key', 0) or key
        actions = getattr(self, 'actions', kwargs)

        self.ref = env.REPOS.get(key, None)
        if self.ref:
            self.token = self.ref.get('token')
            self.github = github.Github(self.token)
            repo = repo or getattr(self, 'repo') or self.ref.get('repo')
            self.branch = self.ref.get('branchRef', {}).get(repo.lower(), 'main')
        else:
            self.token = env.kdogtoken
            self.github = github.Github(self.token)
            self.user = 'kdog3682'

        self.setRepo(repo)
        self.private = private
        self.isFirstTime = False

        if actions:
            for k,v in actions.items():
                m = getattr(self, k)
                if m:
                    try:
                        m(v)
                    except Exception as e:
                        print(e)
                        raise Exception('error')
                        m()
                    break

        if self.isFirstTime:
            pprint(self.getInfo())
            pprint('getting info because first time')

    def getInfo(self):
        print('Getting Repository Info because firstTime')
        user = self.User
        f = lambda x: not x.fork
        repos = filter(list(user.get_repos()), f)
        return map(repos, lambda x: x.name)


    def main(self, sourceFile = 0):

        def isMyScriptFile(file, githubFiles = 0):
            if isUrl(file):
                return False
            name = tail(file)

            if githubFiles and name in env.jslibraries:
                return name not in githubFiles

            return name not in env.jslibraries

        def getHtmlSourceFile():
            f = mostRecent(dir2023, name = '\w{2,}\.html')
            return f

        if not sourceFile:
            sourceFile = getHtmlSourceFile()
        files = getFileDependencies(sourceFile)
        files = filter(files, isMyScriptFile, self.Files)
        if len(files) > 2:
            prompt('files for upload', files)

        pprint(self.upload(files))

    def __str__(self):
        keys = ['user', 'repo']
        a = self.user
        b = self.repo
        return stringify({ 'user': a, 'repo': b })

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
        print('setting branch as', self.branch)

    def getService(self, repo):
        print('getting service for', repo)
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
        name = tail(args[0])
        content = ''

        branch = self.branch
        if len(args) == 1:
            if isfile(args[0]):
                content = read(args[0])
            else:
                raise Exception('need a valid file')
        else:
            content = textgetter(args[1])

        assert(content)

        if name == 'clip.html':
            name = prompt('Choose a file name. fallback=index.html')
            name = addExtension(name, 'html')
        elif name == 'hammy.html' or name == 'asdfsadf.html':
            name = 'index.html'

        result = 0
        try:
            service = self.Service.get_contents(name, ref=self.branch)
            result = self.Service.update_file(
                service.path,
                "--",
                content,
                service.sha,
                branch=self.branch
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

    def upload(self, key):
        if isArray(key):
            return map(key, lambda f: self.write(f))
        elif isObject(key):
            return map(key, lambda k, v: self.write(k, v))
        if isdir(key):
            return map(absdir(key), lambda f: self.write(f))
        elif isfile(key):
            if getExtension(key) == 'html':
                return self.main(key)
            else:
                return self.write(key)

        self.openLink()

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
        r = 'kdog3682|2023'
        if test(r, repo.name):
            print(f"Forbidden Deletion: {repo.name}")
            return
        elif test('github.io', repo.name):
            if not prompt(repo.name, 'are  you sure you want to delete?'):
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
            return {'path': file.path, 'time': getTime(file)}
        
        self.load(repo)
        contents = self.getContents()
        if contents:
            store = map(contents, runner)
            pprint(store)
        elif prompt(f"delete {self.name} because it is empty repo?"):
            self.deleteRepo(self.name)


class MyPublicRepo(Github):
    user = 'kdog3682'
    repo = 'public'

class UploadJsbinCss(MyPublicRepo):
    actions = {
        'upload': {
            'jsbin2.css': 'clip.js',
        }
    }




def get_repo_files(user, repo=0, start='', mode=''):
    if not repo:
        user, repo = split(user, '/')

    g = github.Github()
    #dprompt(user,repo)
    repo = g.get_repo(f"{user}/{repo}")
    default_branch = repo.default_branch
    contents = repo.get_contents(start, ref=default_branch)
    prompt(repo=repo, contents=contents, message='starting... press anything to continue')
    files = []
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            print('path', file_content.path)
            contents.extend(repo.get_contents(file_content.path, ref=default_branch))
        else:
            files.append(file_content)

    if mode == str:
        f = lambda x: x.decoded_content.decode("utf-8")
        s = join([f(x) for x in files])
        clip(s)
        return

    return [file.path for file in files]

#clip(get_repo_files('3b1b/manim'))
def jsdelivr(file, src=0, user=0, repo=0):
    if src:
        src = re.sub('/$', '', src)
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
    file, src='', user="kdog3682", repo="codemirror"
):
    if src:
        user, repo = src.split('/')
    url = "https://raw.githubusercontent.com/$1/$2/main/$3"
    url = templater(url, [user, repo, file])
    return url
#ofile(github_file_url("docs/source/documentation/utils/index.rst", src='3b1b/manim'))
#jsdelivr('3b1b/manim/manimlib/shaders/true_dot/vert.glsl')

#jsdelivr("3b1b/manim/manimlib/mobject/types/vectorized_mobject.py")
def plf():
    f = glf()
    print(fileInfo(f))
    print(read(f))

#plf()
#olf()

def github_usercontent_url(user, repo, *args, master='master'):
    base = 'https://raw.githubusercontent.com'
    file = '/'.join(args)
    return f"{base}/{user}/{repo}/{master}/{file}"

def manim(*args):
    ofile(github_usercontent_url('3b1b', 'manim', *args))

#manim('manimlib/mobject/types/vectorized_mobject.py')

#UploadJsbinCss()


s = """
box
reset
"""

#get_repo_files(user='alexbol99', repo='flatten-js', start='src', mode=str) # works every file is taken and merged together.

def create(dir, private=False):
    name = tail(dir).lower()
    #dprompt(name, dir)

    g = Github(repo=name)
    g.service.edit(private=private)

    SystemCommand(f"""
        git init 
        git branch -m master main
        git add .
        git remote add origin git@github.com:kdog3682/{name}.git
        git commit -m "Initial commit"
        git push -u origin main
    """, dir=dir)

    url = 'https://github.com/kdog3682/' + name
    ofile(url)

def log(x):
    try:
        print(x, 'error')
    except Exception as e:
        pass
    
        
    

firedir = rootdir + 'FIREBASE/'
playdir = rootdir + 'PLAYGROUND/'
#mkdir(playdir)
#chdir(playdir)
#write('index.html', 'aooola')
#create(playdir)
#printdir(playdir)
# '/home/kdog3682/PLAYGROUND/index.html'
