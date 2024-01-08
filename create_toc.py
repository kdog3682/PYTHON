from utils import *

def get_toc_json(root, ignore = default_path_ignore):
    root_dir = Path(root)
    def recurse(directory):

        store = {}
        store["name"] = str(directory)
        store["type"] = "directory"
        store["contents"] = []

        for path in directory.iterdir():
            if ignore(path):
                continue

            value = None
            if path.is_dir():
                value = recurse(path)
            elif path.is_file():
                value = {"type": "file", "name": path.name}

            if value == None: continue
            store["contents"].append(value)

        if empty(store["contents"]):
            return None
        return store

    return recurse(root_dir)


def get_toc_string(data):
    def runner(state):
        name = state.get("name")
        type = state.get("type")
        contents = state.get("contents")

        if type == "directory":
            items = map(contents, runner)
            s = "dir: " + name + "\n"
            s += indent(join(items, "\n"))
            return s
        else:
            return name
    return runner(data)


def create_toc(dir):
    write(tocfile, get_toc_string(get_toc_json(dir)))

# file = get_most_recent_file(typstpackagedir)
# create_toc(file)
" ["[master 6ad2d0b] auto push"," 1 file changed, 52 insertions(+)"," create mode 100644 create_toc.py","Warning: Permanently added the RSA host key for IP address '20.29.134.23' to the list of known hosts.\r","To github.com:kdog3682/PYTHON","   1c2054a..6ad2d0b  master -> master"]
