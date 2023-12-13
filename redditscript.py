from base import *
from next import *
# from utils import *
import requests
import praw

def getSubreddit(r, subreddit):
    key = env.subreddits.get(subreddit, subreddit)
    if hasattr(r, 'reddit'):
        return r.reddit.subreddit(key)
    return r.subreddit(key)

def get_reddit():
    reddit = praw.Reddit(**env.redditinfo)
    reddit.validate_on_submit = True
    return reddit


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
def get_submission_data(submission):
    return {
        "title": submission.title,
        "author": submission.author.name if submission.author else "",
        "subreddit": submission.subreddit.display_name,
        "score": submission.score,
        "url": submission.url,
        "id": submission.id,
        "num_comments": submission.num_comments,
        "created_utc": submission.created_utc,
        "date": datestamp(submission.created_utc),
    }
def printSubmissionInfo(submission):
    blue("Submission Title:", submission.title)
    blue("Submission Author:", submission.author)
    blue("Submission Score:", submission.score)
    blue("Submission URL:", submission.url)
    blue("Submission Comments:", submission.num_comments)
    blue("Submission Created UTC:", submission.created_utc)

def getSubredditSubmissions(subreddit, **kwargs):

    def get():
        computedKwargs = {}
        computedKwargs['limit'] = kwargs.get('limit', 10)
        if kwargs.get('new'): return subreddit.new(**computedKwargs)
        if kwargs.get('hot'): return subreddit.hot(**computedKwargs)
        return subreddit.new(**computedKwargs)
    
    submissions = mapFilter(get(), kwargs.get('checkpoint'))
    blue("Number of Submissions", len(submissions))
    return submissions

class Reddit:
    def getUserSubmissions(self, key, limit = 100):
        if key == 'self':
            user = self.reddit.user.me()
        else:
            user = self.reddit.user.me()
        return user.submissions.new(limit = limit)
    

    def __init__(self):
        reddit = get_reddit()
        self.username = env.redditinfo.get('username')
        self.reddit = reddit
    
    def ask(self, subreddit, title, body):
        try:
            sub = self.reddit.subreddit(subreddit)
            submission = sub.submit(title, body)
            return submission
        except Exception as e:
            print(str(e))
            return 

    def reply_all_comments(self):
        comments = self.get_comments()
        for comment in comments:
            title = str(comment.submission.title)
            author = str(comment.author)
            body = str(comment.body)
            answer = prompt(title, author, body)
            comment.upvote()
            if answer:
                comment.reply(answer)

    def get_posts(
        self,
        subreddit="me",
        mode="new",
        limit=None,
        **kwargs,
    ):
        def filter(post):
            if post.subreddit == "Mementomoriok":
                return False
            if kwargs:
                return isRecent(post.created, **kwargs)
            else:
                return True

        def getter(subreddit, limit, mode):
            if subreddit == "me":
                user = self.reddit.redditor(
                    env.redditusername
                )
                return user.submissions.new(limit=limit)

            else:
                subreddit = reddit.subreddit(subreddit)
                return getattr(subreddit, mode)(limit=limit)

        posts = getter(subreddit, limit, mode)
        store = []
        for post in posts:
            if filter(post):
                store.append(post)
            if len(store) == limit:
                return store
        return store

    def get_comments(self, flat=0):
        def getter(post, mode="all"):
            if flat:
                post.comments.replace_more(limit=None)

            return (
                post.comments
                if mode == None
                else post.comments.list()
            )

        posts = self.get_posts("me", limit=10, days=1)
        store = []
        for post in posts:
            for c in getter(post, mode="all"):
                if isMeatyComment(c):
                    store.append(c)
        return store


def isMeatyComment(c):
    if c.likes:
        return
    if len(c.body) < 15:
        return
    if test("\\bbbot\\b", c.body, flags=re.I):
        return
    if test(
        "bot|AutoModerator|mementomoriok",
        str(c.author),
        flags=re.I,
    ):
        return

    return True


class RedditAPI(Reddit):
    def checkpoint(
        self,
        submission,
        before=0,
        after=0,
        comments=0,
        image=0,
        score=10,
        body=0,
        title=0,
        clicked=0,
        **kwargs,
    ):
        if before and submission.created_utc >= before:
            print("failed at before")
            return 0
        if after and submission.created_utc <= after:
            print("failed at after")
            return 0
        if image and submission.is_self:
            print("failed at image")
            return 0
        if score and submission.score < score:
            print(submission.score, score)
            print("failed at score")
            return 0
        if clicked and submission.clicked < clicked:
            return 0
        if comments and submission.num_comments < comments:
            print("failed at comments")
            return 0
        if body and not test(
            body, submission.selftext, flags=flags
        ):
            print("failed at body")
            
        if title and not test(
            title, submission.title, flags=flags
        ):
            print("failed at title")
            return 0

        return 1

    def getSubmissionData(self, submission, **kwargs):

        if isString(submission):
            submission = self.reddit.submission(
                id=submission
            )

        data = {
            "date": datestamp(submission),
            "title": submission.title,
            "url": submission.url,
            "timestamp": submission.created_utc,
            "score": submission.score,
            "id": submission.id,
            "shortlink": "http://redd.it/" + submission.id,
            #'permalink': 'https://reddit.com' + submission.permalink,
        }
        if hasattr(submission, "media_metadata"):
            store = []
            for key in list(submission.media_metadata):
                ref = submission.media_metadata[key]["p"]
                urls = map(
                    coerceArray(ref), lambda x: x["u"]
                )
                store.extend(urls)
            data["urls"] = store

        return data

        return {
            "title": submission.title,
            "author": str(submission.author),
            "score": submission.score,
            "num_comments": submission.num_comments,
            "body": submission.selftext,
            "clicked": submission.clicked,
            "url": submission.url,
            "upvote_ratio": submission.upvote_ratio,
            "is_image": not submission.is_self,
        }

    def get_submissions(self, subreddit=0, redditor=0, limit=0):

        channel = (
            self.reddit.subreddit(subreddit)
            if subreddit
            else self.reddit.redditor(redditor)
        )
        return channel.new(limit=limit)

             
    def getSubmissionDataItems(
        self, subreddit=0, redditor=0, limit=10, **kwargs
    ):

        with BeforeAfter(
            "reddit.temp.json", key=subreddit or redditor
        ) as ba:

            items = []
            submissions = self.get_submissions(
                subreddit, redditor, limit
            )
            for s in submissions:
                data = self.getSubmissionData(s, **kwargs)
                if self.checkpoint(
                    s, after=after, **kwargs
                ):
                    items.append(data)

            if not items:
                raise Exception("stop")

            after = items[0].get("timestamp")
            ba.set("after", after)
            ba.set("date", datestamp(after, "praw"))
            ba.set("size", len(items))
            ba.set("items", items)


# Reddit().reply_all_comments()
