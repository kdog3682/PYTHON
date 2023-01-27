
def downloadImage(url, name):
    from requests import get
    r = get(url)

a = 'asdf'
asdfasdfsd = 'asdf'
#chdir(rootdir)
#shutil.move('VIM & SH', 'VIM')
#printdir(rootdir)

#pprint(mostRecentFileGroups(rootdir + 'SVG', minutes=5))

def downloadImage(url, name):
    from requests import get
    r = get(url)
    if r.status_code == 200:
        with open(name,'wb') as f:
            f.write(r.content)
            print('Image sucessfully Downloaded: ',name)
            return name
    else:
        print('Image Couldn\'t be retreived', name) 






#SystemCommand('npm update')
#SystemCommand('git show --name-only')
#SystemCommand('git add .\ngit show --name-only')
#SystemCommand('git rev-list --all --count') # 34 commits
#SystemCommand('git shortlog -s')
#ff(text='g4stud', js=1)
#print(tail(pydir))
#mfile('vue-directives.js', 'vue-utils.js')

