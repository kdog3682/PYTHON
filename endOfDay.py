from base import *
from next import *
from datetime import datetime, timedelta

def tomorrow():
    tomorrow = datetime.today() + timedelta(days=1)
    return tomorrow.strftime("%m-%d-%Y")

def main():
    gdjson = '/home/kdog3682/2023/git-data3.json'

    store = []
    store.append(runner('/home/kdog3682/2023/', 1))
    store.append(runner('/home/kdog3682/PYTHON/', 1))
    store.append(runner('/home/kdog3682/RESOURCES/', 0))

    prompt(store, 'continue to append?') 
    appendjson(gdjson, filter(store), mode = list)
    append('/home/kdog3682/.vimrc', tomorrow())


def runner(dir, parseIt = 0, pushIt = 1):

    # def parse(a): return a
    # def push(a): return a

    blue('Start', longstamp())
    if parseIt: value = parse(dir)
    blue('Parsed', longstamp())
    if pushIt: push(dir)
    blue('Pushed', longstamp())
    blue('Sleeping', longstamp())
    sleep(5)
    blue('Wake', longstamp())
    print()
    print()

def push(dir):

    s = f"""
        cd {dir}
        git add .
        git commit -m "'autopush'"
        git push
    """
    SystemCommand(s, dir=dir)


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
