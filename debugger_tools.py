from utils import *

def force_write(*parts, **kwargs):
    path = Path(*parts)
    if not path.parent.is_dir():
        path.parent.mkdir(parents=True, exist_ok=False)

    with open(path.resolve(), "w") as f:
        f.write(kwargs.get("content", "howdy"))
        print("wrote", path.resolve())
