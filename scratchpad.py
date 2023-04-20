from base import *
#from zipscript import unzip
#import requests
fonts = [
    #"Open Sans",
    "Roboto",
    "Lato",
    "Ubuntu",
    "Montserrat",
    "Raleway",
    "Source Sans Pro",
    "Poppins",
    "Merriweather",
    "Playfair Display",
    "Oswald",
    "Nunito",
    "Crimson Text",
    "Fira Sans",
    "PT Sans",
    "Droid Sans",
    "Noto Sans",
    "Josefin Sans",
    "Quicksand",
    "Archivo Narrow",
    "Bitter",
    "Vollkorn",
    "Cabin",
    "Comfortaa",
    "Exo",
    "Inconsolata",
    "Lobster",
    "Pacifico",
    "Poiret One",
    "Roboto Condensed",
    "Signika",
    "Titillium Web",
    "Yantramanav",
    "Abel",
    "Asap",
    "Baloo",
    "Cabin Condensed",
    "Dosis",
    "Ek Mukta",
    "Francois One",
    "Glegoo",
    "Hind",
    "Istok Web",
    "Jaldi",
    "Karla",
    "Lora",
    "Muli",
    "Noticia Text",
    "Old Standard TT",
    "Philosopher"
  ]

#chdir(dldir)

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
