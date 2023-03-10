import time
import base64
import github
from base import *

class Github:

    def __init__(
        self,
        key='kdog3682',
        repo=0,
        private=0,
        **kwargs
    ):
        ref = env.REPOS[key]
        self.token = ref.get('token')
        self.github = github.Github(self.token)
        self.user = ref.get('user')
        self.ref = ref.get('ref', 'main')
        self.setRepo(repo or ref.get('repo'))
        self.private = private
        self.isFirstTime = False

        if kwargs:
            for k,v in kwargs.items():
                m = getattr(self, k)
                if m:
                    try:
                        m(v)
                    except:
                        m()
                    break

        if self.isFirstTime:
            pprint(self.getInfo())

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

        print(f"loading repo: {self.repo}")

    def getService(self, repo):
        print('getting service for', repo)
        query = self.user + "/" + repo

        try:
            return self.github.get_repo(query)
        except Exception as e:
            handleError(e)
            try:
                self.isFirstTime = True
                return self.User.create_repo(
                    repo, private=self.private
                )
            except Exception as e:
                print('errror 2')
                handleError(e)
                self.auth()
                time.sleep(5)
                return self.github.get_repo(query)

    def getFile(self, name):
        f = self.Service.get_contents(name)
        return base64.b64decode(f.content)

    def write(self, *args):

        name = tail(args[0])
        content = ''

        ref = self.ref
        branch = self.ref
        if len(args) == 1:
            content = read(args[0])
        else:
            content = textgetter(args[1])
        if not content:
            print('no content')
            return 

        if name == 'clip.html':
            name = prompt('Choose a file name. fallback=index.html')
            name = addExtension(name, 'html')


        try:
            server = self.Service.get_contents(
                name, ref=ref
            )
            return self.Service.update_file(
                server.path,
                "--",
                content,
                server.sha,
                branch=branch,
            )
        except:
            return self.Service.create_file(
                name, "--", content, branch=branch
            )

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

#Github(key='hammy', printRepo='hammymathclass.github.io')
