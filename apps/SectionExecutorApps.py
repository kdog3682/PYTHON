import env
from utils import *
from debugger_tools import *

GLOBAL_DEBUG_FLAG = 1

def ask_reddit(subreddit, title, body):
    from reddit_script import Reddit
    title = capitalizeTitle(title)
    subreddit = dictf(env.subreddits, subredditFromUrl)(subreddit)
    body = compose(newlinesToNbsp, prettyProse)
    r = Reddit()
    submission = r.ask(subreddit, title, body)
    print({"submission": submission})
    link = f"http://reddit.com/{submission}"
    ofile(link)


def git_download_repo(key, outpath = None):

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
    """

    parts = None
    reponame = None

    if is_url(key):
        parts = match(key, "github.com/([\w-]+)/([\w-]+)")
    elif test(key, "^\w+/\w+$"):
        parts = key.split("/")

    if parts[0] == parts[1]:
        reponame = parts[0]
    else:
        reponame = parts.join("-")
    keys = join(parts, "-")

    repodir = Path(githubdir, reponame)
    if repodir.is_dir():
        print("the repo already has been downloaded")
    else:
        result = system_command("""
            cd $dir
            git clone https://github.com/$key $repodir
        """, githubdir, key, outpath or repodir)
        pprint(result)
