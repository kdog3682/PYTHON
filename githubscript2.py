import base64
import github
from base import *
from next import *

def getToken(key = None):
    ref = {
        None: env.kdogGithubToken,
        'kdog3682': env.kdogGithubToken,
    }
    return ref[key]

class Github:
    
    def view(self, path='', file=''):
        contents = self.getRepoContents(path=path)
        if file:
            f = lambda x: tail(x.path) == tail(file)
            content = find(contents, f)
            if content:
                blue('content', content)
                blue('path', content.path)
                blue('text', content.decoded_content.decode('utf-8'))
            else:
                print('no content found')
                print('original contents:')
                pprint(contents)
        else:
            pprint(contents)
    

    def __init__(self, key=None):
        self.token = getToken(key)
        self.github = github.Github(self.token)
        self.user = self.github.get_user()
        self.username = self.user.login

    def doAuthentication(self, repoName):
        command = (
            'curl -H "Authorization: token '
            + self.token
            + '" --data \'{"name":"'
            + repoName
            + "\"}' https://api.github.com/user/repos"
        )
        os.system(command)
        blue('Authenticated', repoName)

    def setRepo(self, repoName, private=False, create=False):

        if '/' in repoName:
            repoName = repoName.split('/')[-1]

        print('repoName', repoName)
        try:
            self.repo = self.user.get_repo(repoName)
        except Exception as e:
            checkErrorMessage(e, 'Not Found')
            if not create:
                raise Exception('The repo doesnt exist and create is False')

            try:
                self.repo = self.user.create_repo(
                    repoName, private=private
                )
            except Exception as e:
                checkErrorMessage(e, 'Repository creation failed')

                self.doAuthentication(repoName)
                sleep(1)
                self.repo = self.github.get_repo(repoName)

        blue('Successfully set the repo', repoName)
        return self.repo

    def getRepoContents(self, repo=None, path='', recursive = 0):
        if not repo: 
            repo = self.repo

        try:
            ref = repo.default_branch
            contents = repo.get_contents(path, ref=ref)
            if not recursive:
                return contents

            store = []
            while contents:
                content = contents.pop(0)
                if content.type == "dir":
                    items = repo.get_contents(content.path, ref=ref)
                    contents.extend(items)
                else:
                    store.append(content)
            return store

        except Exception as e:
            message = getErrorMessage(e)
            if message == 'This repository is empty':
                return []
            raise e
        

    def getRepo(self, x):
        if isString(x):
            return self.user.get_repo(x)
        return x

    def getRepos(self):
        return self.user.get_repos()
    
    

def prompt(*args, aliases=None):
    if aliases:
        print(aliases)

    for arg in args:
        if arg:
            if isString(arg):
                print(arg)
            else:
                pprint(arg)
    a = input()
    return aliases.get(a, a) if aliases else a

def require(x, message):
    if x == None or x == '':
        raise Exception(message)

def choose(x):

    for i, item in enumerate(x):
        print(i + 1, item)

    print('')
    answer = input()
    if not answer:
        return 

    indexes = answer.strip().split(' ')
    value = [x[int(n) - 1] for n in indexes]
    return smallify(value)


class GithubController(Github):

    def run(self):

        store = []
        repos = self.getRepos()

        def runner(prevAnswer=None):
            if prevAnswer:
                repo = repos[int(prevAnswer) - 1]
            else:
                repo = choose(repos)
            if not repo:
                return finish()
            contents = self.getRepoContents(repo)
            if not contents:
                store.append(['deleteRepo', repo])
                return runner()

            aliases = {
                'd': 'deleteRepo',
                'v': 'viewRepo',
            }

            answer = prompt(contents, aliases=aliases)
            if answer:
                if isNumber(answer):
                    return runner(answer)
                store.append([answer, repo])
                runner()
            else:
                return finish()

        def finish():
            if not store:
                return 

            prompt(store)
            for methodKey,repo in store:
                getattr(self, methodKey)(repo)

            blue('Finished')

        
        runner()


    def deleteRepo(self, x):
        repo = self.getRepo(x)

        if test('kdog3682|2023', repo.name):
            if not test('kdog3682-', repo.name):
                return red('Forbidden Deletion', repo.name)

        repo.delete()
        blue('Deleting Repo', repo.name)
        localName = re.sub('kdog3682-', '', repo.name)
        localDir = npath(rootdir, localName)
        rmdir(localDir, ask=True)


    def createLocalRepo(self, dirName, private=False):

        address = f"{self.username}/{tail(dirName)}"
        dir = None
        try:
            dir = dirGetter(dirName)
        except Exception as e:
            raise e

        blue('dir', dir)
        name = tail(dirName)
        blue('dirName', name)
        blue('address', address)
        input('Awaiting Input to Continue')

        self.setRepo(name, private, create=True)
            
        blue('Repo has been set')
        blue('Starting the mkdir and local git process')

        mkdir(dir)
        chdir(dir)

        if not isfile('README.md') and empty(os.listdir(dir)):
            write('README.md', 'howdy from ' + dir)

        s = f"""
            cd {dir}
            git init
            git add .
            git commit -m "first commit"
            git branch -M main
            git remote add origin git@github.com:{address}.git
            git push -u origin main 
        """

        blue('starting shell command to push git')
        shell(s)
        ofile(self.repo.html_url)
        blue('all finished')

    def upload(self, file, content=None):
         updateRepo(self.repo, file, content)

    def uploadFolder(self, dir, subFolder=None):
        files = getFiles(dir, recursive=1)
        for file in files:
            updateRepo(self.repo, file, subFolder=None)
    

def updateRepo(repo, file, content=None, subFolder=None):
    if not content:
        content = raw(file)

    branch = repo.default_branch
    path = removeHead(file)
    if subFolder:
        path = os.path.join(subFolder, path)

    try:
        return repo.create_file(
            path=path,
            message=f"Upload {file}",
            content=content,
            branch=branch,
        )

    except Exception as e:
        reference = repo.get_contents(path, ref=branch)
        assert(reference)

        return repo.update_file(
            path=reference.path,
            message="Update file content",
            content=content,
            sha=reference.sha,
            branch=branch,
        )

    

def getErrorMessage(e):
    s = search('"message": "(.*?)"', str(e))
    return re.sub('\.$', '', s.strip())


def example(g):
    g.run() # press d to delete the chosen repo
            # the options will shown up in the aliases

def example(g):
    # g.createLocalRepo('RESOURCES', private=True)
    g.createLocalRepo('ftplugin', private=False)
    g.view() # views the repo that was created

def example(g):
    """
        The key for getToken initializes via kdog3682
        We enter the codesnippets repo
        We upload a file
        We view the contents of the repo
    """
    g.setRepo('codesnippets')
    g.upload('/home/kdog3682/PYTHON/githubscript2.py')
    g.view()


def checkErrorMessage(e, s = None):
    m = getErrorMessage(e)
    if s == None:
        return prompt(m)
    if m != s:
        warn('Invalid Error', str(e))


def buildVite(file):

    assertion(file, isfile)
    assertion(file, isHtmlFile)

    result = javascript('viteServe.js', 'build', file)
    clip(result)
    prompt()

    # f = lambda x: not results.get('success').startswith('vite')
    # assertion(results, f, 'vite build error')

    sleep(2)

def example(g, file, projectName):
    buildVite(file)

    g.setRepo('projects')
    vitedistdir = "/home/kdog3682/2023/dist/"
    g.uploadFolder(vitedistdir, subFolder=projectName)
    g.view(path=projectName)




def example(g, **kwargs):
    g.setRepo('ftplugin')
    g.view(**kwargs)


def runExample(**kwargs):
    blue('Kwargs', kwargs)
    blue('Running the Function', toString(example))
    g = GithubController(key='kdog3682')
    blue('Github Instance Initialized', g)
    example(g, **kwargs)

def example(g, **kwargs):
    g.createLocalRepo('/home/kdog3682/2024/', **kwargs)

# runExample(private = True)
