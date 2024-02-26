from utils import *
import markdown2

def generate(file):
    text = read(file)
    m = match(text, "^\s*\"\"\"([\w\W]+?)\"\"\"\n+([\w\W]+)")
    if m:
        a, b = m
        s = f"{a}\n```{b}```"
        return markdown2.markdown(s)


text = generate("/home/kdog3682/PYTHON/run_apps.py")
# write("/home/kdog3682/2024/markdown.html", text, openIt = 1)
