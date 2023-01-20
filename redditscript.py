from base import *
import praw


class Reddit:
    def __init__(self):
        reddit = praw.Reddit(**env.redditinfo)
        reddit.validate_on_submit = True
        self.reddit = reddit

    def ask(self, subreddit, title, body):
        subreddit = self.reddit.subreddit(subreddit)
        submission = subreddit.submit(title, body)
        return submission

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
        self, subreddit = 'me', mode="new", limit=None, **kwargs
    ):
        def filter(post):
            if post.subreddit == 'Mementomoriok':
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
    def get_comments(self):
        def getter(post, mode="all"):
            #post.comments.replace_more(limit=None)
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
