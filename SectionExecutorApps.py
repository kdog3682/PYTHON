
import env
from utils import *
from debugger_tools import *

def ask_reddit(subreddit, title, body):
    from reddit_script import Reddit
    # title = capitalizeTitle(title)
    # subreddit = dictf(env.subreddits, subredditFromUrl)(subreddit)
    # body = compose(newlinesToNbsp, prettyProse)
    r = Reddit()
    submission = r.ask(subreddit, title, body)
    print({"submission": submission})
    link = f"http://reddit.com/{submission}"
    ofile(link)


def download_github_repo(key, outpath = None):

    """
         this function clones a github repo into @githubdir
         /home/kdog3682/GITHUB 

         the key is a url
            it will be parsed for owner/repo

         or the key is a string like: "tryst/tryst"
            first: the owner - tryst
            second: the repo - tryst

         the folder will be named as: tryst-tryst
         if the folder is named tryst-tryst ... it will be "tryst"

         if the folder exists, it is not cloned
         if an outpath is specified, it overrides repodir

        url_repo_key
    """

    parts = None
    reponame = None

    print(key)
    if is_url(key):
        parts = match(key, "github.com/([\w-.]+)/([\w-.]+)")
    elif test(key, "^\w+/\w+$"):
        parts = key.split("/")

    if parts[0] == parts[1]:
        reponame = parts[0]
    else:
        reponame = join(parts, "-")
    key = join(parts, "-")
    url_repo_key = join(parts, "/")

    repodir = Path(githubdir, reponame)
    if repodir.is_dir():
        print("the repo already has been downloaded")
    else:
        out = outpath or repodir
        result = system_command("""
            cd $dir
            git clone https://github.com/$url_repo_key $repodir
        """, githubdir, url_repo_key, out)
        append("/home/kdog3682/2024/files.log", out)
        pprint(result)


CONTROL_ITEMS = [
    { "identifiers": ["bash"], "fn": "bash", "aliases": {"cmd": "bash"} },
    { "identifiers": ["mkdir"], "fn": "fs_setup", "aliases": {"dir": "mkdir"} },
    { "identifiers": ["subreddit"], "fn": "ask_reddit" },
    { "identifiers": ["regex", "file"], "fn": "regex_match" },
    { "identifiers": ["code"], "fn": "execute_code" },
    { "identifiers": ["github"], "fn": "download_github_repo", "aliases": {"key": "github" }},
    { "identifiers": ["file"], "fn": "execute_file" },
]

def regex_match(file, regex):
    s = read(file)
    flags = 0
    if test(regex, "^\^"):
        flags = re.M
    regex = "^ *#?(let \w+\([\w\W]+?\n *})\n *(?=#?let|#)"
    matches = re.findall(regex, s, flags = flags)
    assertion(matches)
    prompt(join(matches, "\n\n"))
    append_section(join(matches))


def append_section(x):
    append("/home/kdog3682/PYTHON/examples.py", hr(70) + x)

def fs_setup(dir):
    mkdir(dir)

def bash(cmd):
    return system_command(cmd)

def execute_file(file):
    if "\n" in file:
        a, b = match(file, "(.+)\n+([\w\W]+)")
        text = read(a)
        code = text + "\n\n" + b
        exec(code)
    elif get_extension(file) == "py":
        exec(read(file))
