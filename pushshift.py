from base import *
import time
import requests

def redditLink(x):
    if isObject(x):
        id = x.get("id")
    elif hasattr(x, "id"):
        id = x.id
    elif isString(x):
        id = x
    else:
        raise Exception('')

    return "https://redd.it/" + id

def openReddit(x):
    webbrowser.open(redditLink(x))




fields = [
    "media_metadata",
    "url",
    "selftext",
    "id",
    "is_self",
    "created_utc",
]
fields = [
    "media_metadata",
    "url",
    "selftext",
    "id",
    "is_self",
    "created_utc",
]


def request(url, delay=0):
    if delay:
        time.sleep(delay)

    r = requests.get(url, {"user-agent": BROWSER_AGENT})
    print(r.status_code)
    return parseJSON(r.text) if r.status_code == 200 else ""

def get_pushshift_url(
    subreddit, after=0, score=1, fields=None, size=1, **kwargs
):
    url = f"http://api.pushshift.io/reddit/search/comment?subreddit={subreddit}&after={after}&size={size}&sort=created_utc&score>={score}"
    return url


def parse(data, image=0):
    if image and data.get('body'):
        print("only image", data.get('body'))
        #return

    payload = {
        'date': datestamp(data, 'praw'),
        'id': data.get('id'),
        'title': search('comments/\w+/(.*?)/', data.get('permalink')).replace('_', '-'),
    }

    #openReddit(payload)
    return payload


def pushshift(subreddit, debug=True, limit=None, **kwargs):
    imageSubreddits = ['unstable_diffusion']
    items = []
    image = 0
    if subreddit in imageSubreddits:
        image = 1
    if debug:
        #limit = 3
        #kwargs["size"] = 5
        kwargs["fields"] = ["title", "id", "created_utc"]

    with BeforeAfter(key=subreddit) as ba:
        after = ba.get("after", 0)

        kwargs["size"] = 20
        after = 0



        url = get_pushshift_url(
            subreddit, **kwargs, after=after
        )
        while True:
            data = request(url)
            if not data:
                raise Exception('')
            if len(data["data"]) == 0:
                break
            items += filter(map(data["data"], parse, image=image))
            after = data["data"][-1]["created_utc"] + 1
            url = get_pushshift_url(subreddit, after=after, **kwargs)
            if debug or (limit and len(items) > limit):
                break
            else:
                time.sleep(1)


        if items:
            ba.set("after", after)
            ba.set("date", datestamp(after, "praw"))
            ba.set("items", items)


#pushshift("mementomoriok")
#pushshift("unstable_diffusion",  score=10)


#history = read('reddit.json').get('unstable_diffusion').get('history')
#history = flat(map(history, lambda x: x.get('items')))
#history = history[0:3]
#map(history, openReddit)
