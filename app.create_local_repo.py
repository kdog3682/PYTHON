from utils import *
from create_toc import get_toc
from githubscript2 import create_local_repo, run

def get_all_paths_to_root(dir_path, root = rootdir):
    """
    Helper Function

    Recursively slices the dir_path until the root is reached.
    Returns a list of all paths from root to the provided directory.

    example input: /home/kdog3682/2024-writing/mmgg/
    """

    path = Path(dir_path)
    root_path = str(Path(root))
    paths = []

    while True:
        parent = path.parent
        if parent.name == "":
            break
        paths.append(str(path))
        if str(parent) == root_path:
            break
        path = parent

    return reverse(paths)

def create_local_repo(g, dir, **kwargs):
    g.createLocalRepo(rootdir, **kwargs)
    

dir = '/home/kdog3682/2024-writing/'
dir = '/home/kdog3682/LOREMDIR/'
dir = '/home/kdog3682/LOREMDIR/node_modules/foo.txt'
dir = '/home/kdog3682/2024-javascript/'
dir = '/home/kdog3682/2024-python/'
dir = '/home/kdog3682/2024-javascript/organize/'
dir = "/home/kdog3682/2024-writing/mmgg/"

main(example, dir, private = True)


def create_local_repo(g, dir, private=True):
    if is_dir(dir):
        inform("""
            the dir: $dir already exists.
            instead, the toc will be printed and we will early return.
        """)
        print(get_toc(dir))
        return 

    dir_paths = get_all_paths_to_root(dir)
    rootdir = dir
    if dir_paths > 1:
        inform("""
            the dir provided ($dir) is a non-root dir.
            it is thus necessary to choose the rootdir
            in which the repo will be initialized.

            in the next prompt, you will be asked to choose the rootdir
        """)
        rootdir = choose(dir_paths)

    address = f"{self.username}/{tail(dirName)}"

    name = tail(dir)
    inform("""
        dir: $dir            (the local directory path)
        name: $name          (the name the repo will be set as)
        address: $address    (the github access path)

        This is the last chance to stop before proceeding.
        Please make sure the information is correct.

        We will make $dir
        We will cd to it
        We will create a README.md
        Git will be initialized to branch main
    """)

    self.setRepo(name, private, create=True)
        
    mkdir(dir) # recursively builds the dir
    write_readme_file(rootdir)
    write_gitignore_file(rootdir)

    system_command(f"""
        cd {rootdir}
        git init
        git add .
        git commit -m "first commit"
        git branch -M main
        git remote add origin git@github.com:{address}.git
        git push -u origin main 
    """)

    view(self.repo.html_url)
    print("done!")

