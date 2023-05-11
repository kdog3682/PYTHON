from base import *
#from zipscript import unzip
#import requests

def get_media(x):
    
    if isUrl(x):
        r = requests.get(url, allow_redirects=True)
        if r.status_code != 200:
            raise Exception('not valid download')
        return r.content
    e = getExtension(x)
    if e:
        if isfile(x):
            return read(x)

def write_media(outpath, data):
    with open(outpath, 'wb') as f:
        f.write(data)
        print('successfully wrote to dldir:', outpath)



def download_google_fonts():
    
    fontdir2023 = dir2023 + 'fonts/'
    fontfile = 'font.zip'

    for font in fonts:
        font_name = font.replace(' ', '+')
        url = f'https://fonts.google.com/download?family={font_name}'
    
        dirname = dash_case(font)
        outdir = fontdir2023 + dirname
        dprompt(dirname, outdir)
        data = get_media(url)
        write_media(fontfile, data)
        unzip(fontfile, mkdir(outdir))
    


#ff(fontdir2023)


#files = zipscript.unzipLatest()
#pprint(files)

#files = prompt(mostRecentFileGroups())

#If it is under a "'", it should look for a '
#Dont create temporary inroeabs because it hurts later.
#printdir(fontdir)


def dash_case(s):
    items = re.split('\W|(?=[A-Z]+[a-z])', s)
    return join(filter(items), delimiter='-').lower()

#pprint(dash_case('AAAhiBob'))


#mfiles(mostRecentFileGroups(), fontdir2023 + 'open-sans')


def unzipLatest():
    f = glf()
    readzip(
        f,
        flatten=True,
        outpath=normpath(dldir, removeExtension(tail(f))),
    )

    return flatdir(mostRecent(dldir))



# backup('oldpy')
# backup('recent')
# consolidate.js
# backup(jsondir)
# backup(txtdir)
# printdir(jsdir)
# print(os.listdir(sandir))
# copydir(zipdir, sandir)
# the difficulties can be solved.


#printdir(jsondir)


#printdir(rootdir)

# This works
def makeRepo(repo):
    from githubscript import KDOG3682
    KDOG3682(repo=repo)
    dir = rootdir + repo
    assert(not isdir(dir) and not isfile(dir))
    mkdir(dir)
    dprompt(dir)
    chdir(dir)
    write('README.md', 'howdy')
    gitaddstring = f"""
        cd {dir}
        git init
        git add .
        git commit -m "Initial commit"
        git remote add origin git@github.com:kdog3682/{repo}.git
        git push -u origin master
    """
    result = SystemCommand(gitaddstring, dir=dir)
    print(result.success, result.error)

#makeRepo('PUBLIC')


def root_two_cf_expansion():
    yield 1
    while True:
        yield 2

def z(a,b,c,d, contfrac):
    for x in contfrac:
        while a > 0 and b > 0 and c > 0 and d > 0:
            t = a // c
            t2 = b // d
            if not t == t2:
                break
            yield t
            a = (10 * (a - c*t))
            b = (10 * (b - d*t))
            # continue with same fraction, don't pull new x
        a, b = x*a+b, a
        c, d = x*c+d, c
    for digit in rdigits(a, c):
        yield digit

def rdigits(p, q):
    while p > 0:
        if p > q:
           d = p // q
           p = p - q * d
        else:
           d = (10 * p) // q
           p = 10 * p - q * d
        yield d

def decimal(contfrac):
    return z(1,0,0,1,contfrac)

a = decimal((root_two_cf_expansion()))
print(next(a))
print(next(a))
print(next(a))
print(next(a))
print(next(a))
print(next(a))
print(next(a))
print(next(a))
print(next(a))
print(next(a))
