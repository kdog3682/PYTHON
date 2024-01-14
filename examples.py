# filetype: executable_template
# caller: runExampleFile.py
# notes:
    this file runs multiple types of things
    it can run python call functions
    it can ask reddit
    it can run bash
    it can start servers

    
------------------------------------------------------------
subreddit: git
title: Is there a way to show the files that are changed on git push?
body:
The result of my git message is:

    [main 97e3706] pushing directory
     2 files changed, 10 insertions(+)
    To github.com:mementomoriok/files.git
       077584e..97e3706  main -> main

Might there be some way to show the actual file names, instead of "2 files changed" ?


------------------------------------------------------------
subreddit: nostupidquestions
title: 
body:

Thus far, I havent detected any 

------------------------------------------------------------
subreddit: pickling 
title: A few beginner questions about pickling eggs
body:

Hey everybody,

I've been on a YouTube binge, watching lots of different egg pickling videos as I get started in my pickling journey. I have some questions, and I hope you guys could help me answer them.

Question 1: What is the purpose of putting in various vegetables into the jar along with the eggs? Is it to make the egg taste better, or is it also to pickle the vegetable at the same time and enjoy the vegetable? Why not pickle the vegetables and eggs separately? I ask this because I feel like it would be easier to take out the eggs one by one if it was all just pure eggs, rather than having vegetables mixed in.

Question 2: Why is it that the jars are always packed to the brim? In a lot of the YouTube videos, they try to pack 12 to 16 eggs completely to the brim of the jar. Does it have something to do with the surface area? Are they trying to minimize the surface area? Does leaving the jar half empty allow bacteria to propagate?

Question 3: What is the purpose of using a hot brine? I understand that salt and vinegar have preservative properties, but the eggs have just recently been boiled and cooled down. Why are we now using a hot brine? What difference is there between using a hot brine and a cold brine?

Thank you for the help. I'm excited to start pickling various foods.
------------------------------------------------------------
subreddit: webdev
title: How does daisyui manage its theme system?
body:

I have been reading thru its css file: 

- https://cdnjs.cloudflare.com/ajax/libs/daisyui/4.4.11/full.css

Something that really stands out is snippets like this:
    
    :root:has(input.theme-controller[value=light]:checked)



------------------------------------------------------------
subreddit: askculinary
title: Does blanching meat cause protein to tighten?

body:

I am watching some youtube videos on preparing chinese pork ribs.
Every video first blanches the meat for about 5 minutes.

This then lead me into reading a reddit thread on blanching meat and in particular asian cuisine:
    https://www.reddit.com/r/AskCulinary/comments/ijqqyt/chinese_recipes_call_for_preblanching_meats/

From experience, I know that if I boil something for some time, it becomes tough and stringy. 
Shouldn't this happen to the meat that gets blanched?

Why not steam the meat instead of blanching?
Why not soak the meat for >>> hours?

It seems over the past thousand years, asian cuisine has established blanching as a correct technique.

My main questions are:

1) Why did blanching win out over other forms of cleaning the meat?

2) Doesn't the texture of the meat get affected by the blanching process? Is this desirable.

------------------------------------------------------------
subreddit: askprogramming 
title: hwu find organize a config file which holds all the information for a timeline animation?

I am going to write a parser to parse the raw config file into a json

t = 0
    fn = revolve(r = 3, point = origin)
    ball1.move(50, 50).after(fn)
    ball2.move(30, 30)    
t = 37
    
------------------------------------------------------------
subreddit: askprogramming 
title: is there a way to access the value of a bound mapping?


------------------------------------------------------------
subreddit: vim 
title: is there a way to access the value of a bound mapping?

body:

Take for instance, the bindings

    nnoremap e0 :call EDefine()<CR>
    nnoremap <buffer> e0 :call EDefineBuffer()<CR>

I would like to use a "get" function in this manner:

    return s:get('e0')
    " the return value is a string repr of the command:
    "nnoremap e0 :call EDefine()<CR>"

or:

    return s:get('e0', 'buffer')
    " the return value is a string repr of the command:
    "nnoremap <buffer> e0 :call EDefineBuffer()<CR>"

------------------------------------------------------------
subreddit: python 
title: How would you collected repeated phrases in a string?
body:

Given the sample text below:
    
    The apple is tasty
    The apple is mushy
    The apple is tasty in autumn

Repeated phrases would be "the apple is" (count 3) and "the apple is tasty" (count 2).

Arguably, "the apple", and "apple is" are also repeating phrases. However, all of their existences exist inside of 'the apple is' so it is not considered unique.

Do you guys have any suggestions on where I could get started?






Do you guys have any suggestions on what I could try?


------------------------------------------------------------
subreddit: vim
title: istaw to trigger completions without using C-x-c-u?

body: when i try to use complete() in a function, i am given the error warning that it has to be used in insertion mode. 
im wondering if theres a way to get smth lk the afec belo

    answer = CustomCompletion(myItems)
    " use the answer however you like in your code

ikn thers input() and inputlist() but those do not create the popup menu, where you can toggle choices with arrow keys.

body: There is an autocmd for "InsertCharPre" and I am using it to

Do you guys have any suggestions on what I could try?

------------------------------------------------------------

subreddit: vim
title: is there a way to choose completions by pressing number keys?
body: For example, the vim completion list will show 5 options. Rather than pressing down 5 times to get the 5th option, I'd like to just press '5' and have it be chosen. I've been tinkering around with feedkeys(), but nothing I am doing is working.

Do you guys have any suggestions on what I could try?

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

 
------------------------------------------------------------

code: testing report lab
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Create a sample PDF
doc = SimpleDocTemplate("table_example.pdf", pagesize=letter)
print(doc)

# Create a list of data for the table
data = [
    ['Name', 'Age', 'Country'],
    ['Alice', 25, 'USA'],
    ['Bob', 32, 'Canada'],
    ['Charlie', 28, 'UK'],
    ['David', 23, 'Australia'],
]

# Create a table with the data
table = Table(data)

# Apply table styles
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))

# Create a story to hold the content
story = [table]

# Build the PDF
----------------------------------------------------------------------------
subreddit: vim
title: istaw
body:



----------------------------------------------------------------------------
----------------------------------------------------------------------------
subreddit: git
title: Can you some how "download" all of your git history?
body:

I am hoping to create a frontend ui where a user can view all of their github/git data.

Something like:

    on october 13, 2023, you 
        created:
            file a
            file b
            file c
        modified:
            file d (10 insertions)
            file e (12 insertions)
            file f (13 insertions, 3 deletions)

    on october 14, 2023, you ...

as well as stats:

    your most frequent file edited is
        file abc 
    
    it has been edited on:
        march 1
        march 2
        march 7
        ...
        for a total of 700 edits

But to do this, I will need to aggregate all of the git push data.

Is there a way for downloading such data?
Or maybe a way to parse it from the .git directory?


----------------------------------------------------------------------------
subreddit: pickling
title: How do you clean your pickling jars for reuse?
body:

I have pickled eggs in a standard mason jar.
The jar has a vinegar-salt-eggy smell.

I have designated this jar as the "pickled egg jar."

Part of me is wondering, is it even necessary to wash it very thoroughly?
I am just going to be adding more salt-vinegar-eggs to it in the future.

Part of me is fearing, if I dont give it a deep wash, botulism or other bad stuff could appear?

----------------------------------------------------------------------------
note: it doesnt work
bash:

cd /home/kdog3682/2024/
hugo new site quickstart
cd quickstart
git init
git submodule add https://github.com/theNewDynamic/gohugo-theme-ananke.git themes/ananke
echo "theme = 'ananke'" >> hugo.toml
hugo server

----------------------------------------------------------------------------

outpath: ~/GITHUB/typst-packages/codelst
github: https://github.com/jneug/typst-codelst


----------------------------------------------------------------------------
github: https://github.com/typst/templates
outpath: ~/GITHUB/typst-packages/templates

implementation:
1704518934 /home/kdog3682/PYTHON/SectionExecutorApps.py
1704518972 /home/kdog3682/PYTHON/SectionExecutor.py


----------------------------------------------------------------------------

typst: 

why does 50% baseline look a little bit off?

i was hoping to get the names centered completely inline with the text, but from what I can see, it looks a little bit off.


?r

#set page(width: 200pt, height: auto)

Good morning
#{
  let names = ("sam", "bob", "george")
  let abcde = [
     #for name in names {
       name
       parbreak()
       
     }
  ]
    
  let dictionary = (
    // left: blue + 2pt,
    // right: blue + 2pt,
    :
  )
  let outset = (
    x: 0pt,
  )
  let inset = (
    x: 5pt,
    y: 5pt,
  )
  let radius = 3pt
  let height = auto
  box(baseline: 10pt, clip: false, fill: yellow, height: height, inset: inset, outset: outset, radius: radius, stroke: dictionary, abcde)
}
!

----------------------------------------------------------------------------

github: https://github.com/EpicEricEE/typst-plugins/tree/master/quick-maths/src
outpath: ~/GITHUB/typst-packages/quick-maths
outpath: ~/GITHUB/typst-packages/leetcode
github: https://github.com/lucifer1004/leetcode.typ

# /home/kdog3682/GITHUB/typst-packages/quick-maths
# /home/kdog3682/GITHUB/typst-packages/leetcode
# /home/kdog3682/GITHUB/typst-packages/leetcode/build/leetcode.pdf


github: https://github.com/vuejs/core
outpath: ~/GITHUB/vuejs3
toc: 1

----------------------------------------------------------------------------
file: /home/kdog3682/2024/web.typ
regex: ^#?(let \\w+\\([\\w\\W]+?\\n *})\\n *(?=#?let)"


----------------------------------------------------------------------------
file: /home/kdog3682/2024/util.typ
regex: ^styles\\.[\\w+.]
unique: 1
join: 1


help: 1704518934 /home/kdog3682/PYTHON/SectionExecutorApps.py

----------------------------------------------------------------------------
subreddit: askprogramming
title: Is there a way to automatically refresh pdf on chromebook?
body:

----------------------------------------------------------------------------

fn: create_pip_package
dir: /home/kdog3682/2024-python/google-api-wrappers/gapi_wrappers
files: 
google_sheets.py
google_docs.py
google_classroom.py
manager.py
__init__.py
/home/kdog3682/2024-python/google-api-toolkit/setup.py
----------------------------------------------------------------------------

mkdir: /home/kdog3682/2024-python/utli
file: /home/kdog3682/2024-python/filesystem-setup-toolkit/fs_toolkit/abc.py
file: /home/kdog3682/2024-python/filesystem-setup-toolkit/fs_toolkit/create_pip_package.py
file: /home/kdog3682/2024-python/filesystem-setup-toolkit/setup.py
file: /home/kdog3682/2024-python/filesystem-setup-toolkit/fs_toolkit/__init__.py


filesystem-setup-toolkit/fs_toolkit

        
----------------------------------------------------------------------------
datetime: 01-08-2024 03:30PM
bash:

# cd /home/kdog3682/2024-python/filesystem-setup-toolkit
# pip3 install .

# this will allow you to incrementally readopt the item
cd /home/kdog3682/2024-python/filesystem-setup-toolkit
pip3 install -e .

----------------------------------------------------------------------------
datetime: 01-08-2024 03:30PM
bash:

# no. typechecking is not how python is used
# maybe u just write better doc notes
# it is a tool that exists ... 
# it will perhaps introduce better habits
# 
python3 -m pip3 install mypy

----------------------------------------------------------------------------
datetime: 01-08-2024 03:30PM
help_notes:

    log: config
        will log the config
    log: help_notes
        will log the help_notes value

instead of "log", can also write "debug" which will then early return

----------------------------------------------------------------------------
datetime: 01-08-2024 05:08PM
title: how to use mypy && typing
snippet:

from typing import List

def foo(s: str) -> List[int]:
    return [s]

print(foo("hi"))

notes:

the arrow goes before the colon
cant use a normal list ... have to use a typing list



----------------------------------------------------------------------------
datetime: 01-08-2024 09:45PM
file: /home/kdog3682/PYTHON/google_sheets_api.py

sample_data = [['Header1', 'Header2'], ['Data1', 'Data2']]
gs = GoogleSheets()
gs.create("My New Spreadsheet", sample_data)
gs.format_headers()
webbrowser.open(gs.url)

----------------------------------------------------------------------------
datetime: 01-08-2024 09:45PM
file: /home/kdog3682/PYTHON/gapi_drive.py
desc: delete today spreadsheets

env.ask = 1
query = "mimetype = spreadsheet name = spreadsh size = 10 after = today"
delete_files(query)


----------------------------------------------------------------------------
datetime: 01-08-2024 09:45PM
file: /home/kdog3682/PYTHON/gapi_sheets.py

# working
finance = GoogleSheets("fina")
pprint(finance) # gets financial statements
finance.resize(rows = 10, cols = 10)
open(finance)

----------------------------------------------------------------------------
datetime: 01-11-2024 12:28PM
subreddit: 
title: Is there a way to do movements in autocompletion?
body:

I have tried a few times using <expr> and feedkeys, but nothing seems to be working.
The goal is to embed movements into autocompletion

Normally with the completion object: {word: banana, abbr: ban}
completing on ban gives banana

I would like this: {word: banana<left>, abbr: ban} to also work.
completing on ban gives banana, and then moves one to the left.

Doing a preparse doesnt work

------------------------------------------------------------
subreddit: learnprogramming
title: Why does this example use "Args" and not "Parameters" ?
body:

args are the literal things passed to the function
params are the definitions of the args being passed


I feel like the below (Google Style DocString) should use the word "Parameters" instead of "Args".
What do you guys think?


    def function_with_pep484_type_annotations(param1: int, param2: str) -> bool:
        """Example function with PEP 484 type annotations.

        Args:
            param1: The first parameter.
            param2: The second parameter.

        Returns:
            The return value. True for success, False otherwise.

        """


----------------------------------------------------------------------------
datetime: 01-12-2024 07:30PM
bash:

cd /home/kdog3682/2024-javascript/
ls /home/kdog3682/2024-javascript/
npm i @lezer/python
npm i @lezer/javascript
ls /home/kdog3682/2024-javascript/

----------------------------------------------------------------------------
datetime: 01-13-2024 07:29PM
file: /home/kdog3682/PYTHON/githubscript2.py

def get_all_paths_to_root(dir_path, root = rootdir):
    """
    Recursively slices the dir_path until the root is reached.
    Returns a list of all paths from root to the provided directory.

    input: /home/kdog3682/2024-writing/mmgg/
    """
    path = Path(dir_path)
    root_path = str(Path(root))
    paths = []

    while True:
        parent = path.parent
        if parent.name == "":
            break
        paths.append(str(path))
        if str(parent) == root_path:
            break
        path = parent

    return reverse(paths)

def create_local_repo(g, dir, **kwargs):
    dir_paths = get_all_paths_to_root(dir)
    mkdir(dir)
    print("choose the directory for the local repo")
    dir = choose(dir_paths)
    filetype = choose(defs.filetypes, )
        write_git_ignore(dir)
    g.createLocalRepo(dir, **kwargs)
    

dir = '/home/kdog3682/2024-writing/'
dir = '/home/kdog3682/LOREMDIR/'
dir = '/home/kdog3682/LOREMDIR/node_modules/foo.txt'
dir = '/home/kdog3682/2024-javascript/'
dir = '/home/kdog3682/2024-python/'
dir = '/home/kdog3682/2024-javascript/organize/'
dir = "/home/kdog3682/2024-writing/mmgg/"

main(example, dir, private = True)
