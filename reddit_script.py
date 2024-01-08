# /home/kdog3682/PYTHON/redditscript.py

from utils import *
import praw


def get_data(x):
    fn = get_comment_data if is_comment(x) else get_submission_data
    return fn(x)


def get_text(x):
    return x.body if is_comment(x) else x.selftext


def get_submission_data(submission):
    return {
        "title": submission.title,
        "author": submission.author.name if submission.author else "",
        "subreddit": submission.subreddit.display_name,
        "score": submission.score,
        "text": submission.selftext,
        "url": submission.url,
        "id": submission.id,
        "num_comments": submission.num_comments,
        "created_utc": submission.created_utc,
        "date": datestamp(submission.created_utc),
    }


def create_reddit_checkpoint(**kwargs):
    tests = []

    def runner(k, v):
        if k == "comment":
            return is_comment
        if k == "today":
            return is_today
        if k == "is_root":
            return lambda x: x.is_root
        if k == "min_score":
            return lambda x: x.score >= v
        if k == "min_sentences":
            return lambda x: len(get_sentences(get_text(x))) >= v

    tests = map(kwargs, runner)
    return everyf(tests)


def get_reddit():
    reddit = praw.Reddit(**env.redditinfo)
    reddit.validate_on_submit = True
    return reddit


def download_reddit_saved_comments_as_notes():
    reddit = get_reddit()
    posts = reddit.user.me().saved(limit=2)
    comments = filter(posts, everyf(is_comment))
    data = map(comments, get_data)
    append_reddit_notes(data)
    map(comments, unsave)


def append_reddit_notes(data):
    reddit_note_file = "my_saved_comments_from_reddit.json"
    append_json(reddit_note_file, data)


def get_submission(reddit, x):
    if is_string(x):
        id = match(x, "comments/(\w+)") if is_url(x) else x
        return reddit.submission(id)
    elif get_constructor_name(x) == "Submission":
        return x


def get_comments(s, min_score=5, min_sentences=5, is_root=0, more=1):
    tests = []
    checkpoint = everyf(tests)
    if more:
        s.comments.replace_more(limit=None)
    return filter(s.comments, checkpoint)


def get_high_scoring_comments_from_submission(x):
    reddit = get_reddit()
    s = get_submission(reddit, x)
    checkpoint = create_reddit_checkpoint(
        is_root=1, min_score=20, min_sentences=5
    )
    comments = filter(get_comments(s, more=True), checkpoint)
    data = map(comments, get_comment_data)
    append_reddit_notes(data)


def unsave(c):
    print("uncommenting", c)
    c.unsave()


def get_comment_data(comment):
    return {
        "text": comment.body,
        "author": comment.author.name if comment.author else "",
        "score": comment.score,
        "id": comment.id,
        "parent_id": comment.submission.id,
        "created_utc": comment.created_utc,
        "parent_created_utc": comment.submission.created_utc,
        "subreddit": comment.subreddit.display_name,
        "date": datestamp(comment.created_utc),
    }


def is_comment(item):
    return get_constructor_name == "Comment"


def get_flairs(subreddit):
    flairs = subreddit.flair.templates
    return [{'id': f.get("id"), 'text': f.get("text")} for f in flairs]


def ask(reddit, subreddit, title, body):
    sub = reddit.subreddit(subreddit)

    try:
        submission = sub.submit(title, body)
        return submission
    except Exception as e:
        if "SUBMIT_VALIDATION_FLAIR_REQUIRED" in str(e):
            # flairs = get_flairs(sub)
            # flair = choose(flairs)
            # flair_id = flair.get("id")
            submission = sub.submit(title, body)
            submission.mod.flair(flair = "Resources")
            return submission
        else:
            raise e

class Reddit:
    def __init__(self):
        self.reddit = get_reddit()

    def ask(self, subreddit, title, body):
        return ask(self.reddit, subreddit, title, body)
