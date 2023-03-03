from base import *
import inspect
announcements = """ 

----------------------------------------------------------------
# temporaryBackup

VimConnector = ExecRef via AnythingHandler('tbu')

Desc = When you dont want to git push ...
And simply want a temporary backup of what you're doing,
Use this function.

tempbudir = "/mnt/chromeos/GoogleDrive/MyDrive/BACKUP/TEMP/"

----------------------------------------------------------------

# asdfsd

asdfasdf


""" 


def getCaller(n=0):

    stack = inspect.stack()
    if n == -1:
        return stack[2][3]
    else:
        return stack[len(stack) - 2][3]

def announce(key=0):
    if not key: key = getCaller()

    #items = split(announcements, '^---+', flags=re.M)
    #pairs = map(items, lambda x: search('# *(.+)\s+([\w\W]+)', x))
    #ref = dict(pairs)

    r = '(?:\n|^)# *(.+)\s+([\w\W]+?)(?:\n*$|\n+---)'
    ref = dict(re.findall(r, announcements))


    print("This is an announcement for", key)
    print("-" * 60)
    print("key", key)
    print("-" * (len(key) + 4))
    print("announcement:", ref.get(key))
    print("-" * 60)
    print("press anything to continnue")
    input()

