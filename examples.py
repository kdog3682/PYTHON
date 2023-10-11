LOCAL VIMSCRIPT

inoreab <buffer>-- -------------------------------------------------------------<C-R>=Eatchar('\s')<CR>

------------------------------------------------------------
subreddit: me 
title: vim is awesome
body: 

Seriously.

Vim is so fun to use.
Everything is just one movement away.

You can define and configure basically anything.
It's fast.

What makes vim awesome for you?
-----------------------------------------
title: vim rocks
body:  222

-----------------------------------------

subreddit: https://www.reddit.com/r/intermittentfasting/
title: Does this eating schedule count as intermittent fasting?
body: 

8AM = Breakfast
11:30AM = Lunch
5PM = Dinner

5:30PM to 8AM = no food ... only water and tea?


subreddit: askscience
title: How does


----------------------------------
subreddit: vim
title: is there a way to remove the default normal mappings of "[" and "]" ?
body:

I have my own normal mapping for '[' and ']'
However, vim waits like 1 second when I press it, which I'm pretty sure means there are other mappings also using '[' and ']'

None of my other mappings use these bindings, which must mean vim's defaults are using them.

Would there be some way to remove these default mappings?

Thanks for the help.

-------------------------------------------------------------
foobar: 123
r: ''
e: abc
title: unmap
text: unmap
flags: re.I

code:

# from redditscript import Reddit, printSubmissionInfo, getSubreddit, getSubredditSubmissions

def checkpoint(submission):
    if submission.author != r.username:
        return False
    if r and not test(r, submission.title, flags=re.I):
        return False
    return True

def checkpoint(submission):
    return True

def cleanupMementomori(limit = 5, r = 'vim'):
    reddit = Reddit()
    subreddit = getSubreddit(reddit, 'self')
    kwargs = dict(limit=limit, new=True, checkpoint=checkpoint)
    submissions = getSubredditSubmissions(subreddit, **kwargs)

    for submission in submissions:
        printSubmissionInfo(submission)
        submission.delete()
        red('Deleted', submission.title)

def redditTestf(title = None, text = None, flags = 0):
    def runner(submission):
        if title and test(title, submission.title, flags == flags):
            return true

        if text and test(text, submission.selftext, flags == flags):
            return true
    return runner

def pickfromMyRedditPosts(**kwargs):
    reddit = Reddit()
    submissions = list(reddit.getUserSubmissions('self', limit = 10))
    checkpoint = redditTestf(**kwargs)
    for submission in submissions:
        if checkpoint(submission):
            return ofile(submission.url)

    pick(submissions, display = lambda x: x.title, get = lambda x: ofile(x.url))

def foo(a, **kwargs):
    print(a)
    print(kwargs)


def replyToComments(submission):
    comments = post.comments.list()
    for ${GetForIterationVariable(comments) in comments):
       for item in items):
           for item in asd):
               for
           
-------------------------------------------------------------


inpath: /usr/share/vim/vim82/doc/eval.txt
code:

def foo(inpath):
    print(inpath)

-------------------------------------------------------------
subreddit: askmenover30
title: do you find that you want to eat more in yours 30s?
body: 

I am turning 34 this year, and I find myself able to eat a lot more.
I remember in my 20s, 1 bowl, and I would feel full.

Now, I can eat 2 bowls, and still want to eat more.

I know that metabolism slows down as we grow older.
Is it also, that appetite goes up?

-------------------------------------------------------------
subreddit: me 
title: How would you recommend being more productive in the afternoons?
body:

I find that I do my best work in the mornings.

In the afternoon, my brain feels much more sluggish and I just do "low-hanging" fruit.

And then around 5PM, I kind of don't want to do anything anymore.

How do you guys (if you do) stay productive in the afternoons?
-------------------------------------------------------------
date: 09-28-2023 
desc: testing it out
s:

line 1
line 2
line 3

y: 10

code:

def foo(s, y = 3):
    print(y - 3)


code
-------------------------------------------------------------
date: ${DateStamp()}
d: $date
desc: testing it out

arg: 

howdy from line 1
howdy from line 2
howdy from line 3

code:

$c

def foo(s):
    print(s)
    return 



code:

-------------------------------------------------------------

s:
def mfile(f, t, mode="move"):
    assert isfile(f)
    t = env.dirdict.get(t, t)
    e = getExtension(t)

    if test('\.\d+-\d+-\d+$', t):
        pass
    elif not e and not isdir(t):
        a = prompt('no extension for', t, 'did you forget it?')
        if a:
            t = addExtension(t, getExtension(f))
        else:
            prompt('are you sure you want to make a directory?', t)
            mkdir(t)
    elif not e:
        t = normpath(t, f)

    if tail(f) == tail(t):
        print('mode', "file", tail(f), "to", head(t))
    else:
        print(f"{mode} file: {f} to {t}")

    try:
        getattr(shutil, mode)(f, t)
        return 1000000000000000
    except Exception as e:
        config = black.FileMode(line_length=88, string_normalization=False)
        return 0


s:

config = black.FileMode(line_length=88, string_normalization=False)aaaaaaaa
code:

def foo(s):
    return len(s)


-------------------------------------------------------------

url: https://github.com/lezer-parser/python/tree/main/src
# stop: 1
code:

def parseRepoAndPathFromUrl(s):
    m = search('github.com/(.*?/.*?)(?:/|$)', s)
    path = ''
    return [m, path]

def getText(content):
    return content.decoded_content.decode('utf-8')

def writeGithubContent(content):
    if content.type == 'dir':
        return 

    name = tail(content.path)
    file = npath(name)
    if isfile(name):
        name = ask('Give a new name for %s', name) or name
        file = npath(name)

    write(file, getText(content))
    save(file)

def downloadExternalRepoContents(g, url):
    repoName, path = parseRepoAndPathFromUrl(url)
    repo = g.github.get_repo(repoName)
    path = 'src'
    contents = g.getRepoContents(repo, path = path, recursive = 1)
    announce('Contents for Github Download', contents)
    for content in contents:
        writeGithubContent(content)

-----------------------------------------------------------------


arg: 123

code:
def foo(s):
    return [s]
