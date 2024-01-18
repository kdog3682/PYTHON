
"""

# Python App Controller

Often, I find myself writing "application" type functions like copying files, moving files, finding files, asking questions on reddit, pushing to github, et cetera.

Th function `python_app_controller` groups all of these app type files into a single page where they can be easily accessed.

Lets take a look!

``` 
id: craigslist
desc: scrape craigslist jobs and output to clip.js

from playwright_webscraper import playwright_runner, scrape_craigslist_jobs
playwright_runner(scrape_craigslist_jobs)

------------------------------------------------------
id: get_reddit_notes
desc: downloads my reddit saved comments. often, will save a few comments. this will immediately download them

from reddit_script import *
download_reddit_saved_comments_as_notes()

------------------------------------------------------

```

The above snippet comes from the file "apps.py".
The sections are marked by the dashed lines.
Upon run, a table of contents is generated using the id and the description.

Using the table of contents, you can choose a section to python_app_controller. The code written in that section is then executed as native python.

## Advantages

### Organization
The biggest advantage (in my opinion) is organization.
If a file is listed in the table of contents, I have a pretty good idea of what it is for.

Previously, I spent a lot of time looking for files and navigating around. This system of organization makes it much more wieldly.

### Fast

In javascript version ES6, you have to import everything at the very top.

```
import {packageManager3} from "./node-utils.js"
import * as utils from "./utils.js"
import * as lezerFunctions from "./lezer-functions.js"
import * as lezerSetup from "./lezer-setup2.js"

// your code

```

You cannot conditionally import code.
Everything must be loaded at the top.

Whats the result of this?

**Stuff can be slow!**


Take a look again at the below section.

``` 
id: craigslist
desc: scrape craigslist jobs and output to clip.js

from playwright_webscraper import playwright_runner, scrape_craigslist_jobs
playwright_runner(scrape_craigslist_jobs)

```

There is only one import present: importing `playwright_webscraper`, and we subsequently have fast python_app_controller times.



In my opinion, coding is often about gathering data, running processes, executing tasks, and in many times, doing multiples of these at the same time.




"""



from utils import *

def dash_split(s):
    return filter(map(re.split("^-{20,}", s, flags = re.M), trim))

def has_newlines(s):
    return test(s, "\n")

def split_once(s, r):
    return match(s, f"(.*?){r}([\w\W]+)")

def colon_dict(s):
    items = map(filter(re.split("^(\S+):", s, flags = re.M)), trim)
    a,b = split_once(items[-1], "\n+")
    items.pop()
    items.append(a)
    items.append("code")
    items.append(b)
    return dict(partition(items))
    
def python_app_controller():
    id = "" if len(sys.argv) == 1 else sys.argv[1]
    print("""
        Welcome to run_apps
        each app shown below is registered in the files: apps.py

        when no id is given, you will be asked to choose an id.
        each id is paired with a description

        have fun!
    """)

    s = read("/home/kdog3682/PYTHON/apps.py")
    base = dash_split(s)
    items = map(dash_split(s), colon_dict)
    if id:
        item = find(items, lambda x: x.get("id") == id)
    else:
        for i, item in enumerate(items):
            print(i + 1, item.get("id"), blue(item.get("desc")))

        answer = int(input("\nchoose 1 based indexes\n")) - 1
        item = items[answer]
    if item:
        print(item)
        exec(item.get("code"))

if __name__ == "__main__":
    python_app_controller()
