
# from env import *
# from setup import *
from utils import *


def filter_globals_by_suffix(checkpoint):
    return [v for k, v in globals().items() if checkpoint(k, v)]

def checkpoint(k, v):
    return is_string(v) and test(k, "dir$")

# pprint(len(globals().keys()))
# clip(filter_globals_by_suffix(checkpoint))
dirdict = {"2023":"/home/kdog3682/2023/","2024":"/home/kdog3682/2024/","fonts":"/home/kdog3682/2023/fonts","nm":"/home/kdog3682/2023/node_modules","res":"/home/kdog3682/RESOURCES","trash":"/home/kdog3682/TRASH","dl":"/mnt/chromeos/MyFiles/Downloads","budir":"/mnt/chromeos/GoogleDrive/MyDrive/BACKUP","node":"/home/kdog3682/2023/node_modules","g":"/home/kdog3682/latest-git-cloned-repo","py":"/home/kdog3682/PYTHON","ftp":"/home/kdog3682/.vim/ftplugin","23":"/home/kdog3682/2023","24":"/home/kdog3682/2024","r":"/home/kdog3682","usr":"/usr/local/bin"}
directoryaliases = {"24":"/home/kdog3682/2024","py":"/home/kdog3682/PYTHON","ftp":"/home/kdog3682/.vim/ftplugin","23":"/home/kdog3682/2023","res":"/home/kdog3682/RESOURCES"}

def values(*args):
    transform = lambda x: sub(x, "/$", "")
    getter = lambda x: list(x.values()) if is_object(x) else list(x)
    base = flat(map(args, getter))
    return unique(map(base, transform))
# clip(values(dirdict, directoryaliases, filter_globals_by_suffix(checkpoint)))
# clip(map(listdir(rootdir, is_dir, is_public_path), str))


s = """
# /home/kdog3682/2024-javascript/txflow/lexer.js StateContext3.js
# /home/kdog3682/2024-javascript/txflow/parser.js
# /home/kdog3682/2024-javascript/txflow/handlers.js


/home/kdog3682/2024-javascript/js-toolkit/Element.js
"""

values = map(line_getter(remove_comments(s)), lambda x: split_once(x, " "))
prompt(values)
for a,b in values:
    force_write(a)
