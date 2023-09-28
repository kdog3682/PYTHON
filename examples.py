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
code:

from redditscript import Reddit, printSubmissionInfo, getSubreddit, getSubredditSubmissions

def checkpoint(submission):
    if submission.author != r.username:
        return False
    if r and not test(r, submission.title, flags=re.I):
        return False
    return True

def checkpoint(submission):
    return True

def cleanupMementomori(limit = 5, r = 'vim'):
    prompt({'r': r})

    reddit = Reddit()
    subreddit = getSubreddit(reddit, 'me')
    kwargs = dict(limit=limit, new=True, checkpoint=checkpoint)
    submissions = getSubredditSubmissions(subreddit, **kwargs)

    for submission in submissions:
        printSubmissionInfo(submission)
        submission.delete()
        red('Deleted', submission.title)


-------------------------------------------------------------

# mfile(oldjdjsonfile, jdjsonfile)
# printdir('~/.vim')
# '/usr/share/vim/vim82/doc/eval.txt'
# 4. Builtin Functions					*functions*
