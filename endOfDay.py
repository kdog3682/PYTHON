from base import *
from next import *

def main():
    doGit()
    doVim()
    doReddit()
    doNotes()

def doGit():
    ref = [
        ('/home/kdog3682/.vim/ftplugin/', 0),
        ('/home/kdog3682/2023/',          1),
        ('/home/kdog3682/PYTHON/',        1),
        ('/home/kdog3682/RESOURCES/',     0),
    ]

    store = mapFilter(ref, lambda args: runner(*args))
    appendjson(gdjsonfile, store, mode = list, ask = 1)

def doVim():
    append('/home/kdog3682/.vimrc', '" ' + tomorrow())

def doReddit():
    pass

def doNotes():
    pass



def runner(dir, parseIt):

    blue('Starting GitPush Runner', longstamp())
    blue('Directory', dir)
    value = None
    if parseIt: 
        value = parse(dir)
    blue('Finished Parsed', longstamp())
    print(push(dir))
    blue('Finished Pushing', longstamp())
    blue('Sleeping for 2 seconds', longstamp())
    blue(linebreak)
    print()
    sleep(2)
    return value

def push(dir):
    s = f"""
        cd {dir}
        git add .
        git commit -m "'autopush'"
        git push
    """
    r = SystemCommand(s, dir=dir)
    return r.success or r.error


def parse(dir):

    result = SystemCommand('git status --short', dir=dir)
    r = '^ *(\?\?|M) (.+)'
    m = re.findall(r, result.success, flags=re.M)
    if not m:
        return 

    modified = []
    created = []
    for a,b in m:
        if removable(b):
            continue

        if a == '??':
            created.append(b)
        else:
            modified.append(b)

    date = datestamp()
    payload = {'date': datestamp()}
    if modified: payload['modified'] = modified
    if created: payload['created'] = created
    payload['directory'] = dir
    return payload

main()
