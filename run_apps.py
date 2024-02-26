from utils import *
import time

def implicit_code_colon_dict(s):
    """
        like colon dict, but if the "code" key is not present,
        the code key is implicitly added in by splitting the last item
    """
    items = map(filter(re.split("^(\S+):", s, flags = re.M)), trim)

    if "code" in items:
        return dict(partition(items))

    a,b = split_once(items[-1], "\n+")
    items.pop()
    items.append(a)
    items.append("code")
    items.append(b)
    return dict(partition(items))
    
def python_app_controller():
    id = None
    print("""
        Welcome to run_apps
        each app shown below is registered in the files: apps.py
    """)

    s = read("/home/kdog3682/PYTHON/apps.py")

    vim = {} if len(sys.argv) == 1 else shellunescape(get_last(sys.argv))
    base = dash_split(s)
    items = map(dash_split(s), implicit_code_colon_dict)
    if id:
        item = find(items, lambda x: x.get("id") == id)
    else:
        check = lambda x: not x.get("status", "").startswith("not")
        items = filter(items, check)
        for i, item in enumerate(items):
            print(i + 1, item.get("id"), blue(item.get("desc")))

        answer = int(input("\nchoose an answer in 1-based indexes\n")) - 1
        item = items[answer]

    if item:
        code = templater(item.get('code'), vim)
        exec(code)



def fix_necessary_dollar_inputs(s):
    return s
    r = "\$(\w+(?:\(.*?\)?)"
    matches = unique(re.findall(r, s))

    lib = {
        get_unlisted_git_directories
    }
    def replacer(x):
        m = x.group(1)
        if m in lib:
            display(lib[m](), m)

    def display(a, b):
        print("base key", b)
        answer = choose(a)
        return answer

    return sub(s, r, replacer)



def copy_file_to_drive(file, outpath = "", dir = ""):
    return base_copy_file(file, npath(drivedir + dir, outpath))

def get_unlisted_git_directories():
    return listdir(rootdir, lambda x: x.is_dir() and not test(x.name, "sample|^\.|^[A-Z]+$") and not is_dir(Path(x, ".git")))

def compile_typst(typst_file, outpath = None, data = None):
    if not outpath: outpath = "/home/kdog3682/2024-typst/test.pdf"
    if data:
        write("/home/kdog3682/2024/temp.json", data)
        print("sleeping for 1 second")
        time.sleep(1)

    with CD("/home/kdog3682/2024-typst/src/"):
        print("compiling typst")
        system_command(f"typst compile {typst_file} {outpath} --root /")
        open_url(outpath)


def cleanup_empty_viminfo_files():
    base = "/home/kdog3682/.viminf"
    store = []
    for letter in alphabet:
        file = f"{base}{letter}.tmp"
        info = get_file_info(file)
        if info and info.get("size") < 10:
            remove_file(file)
            store.append(info)
    return store

if __name__ == "__main__":
    python_app_controller()
