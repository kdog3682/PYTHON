id: craigslist
desc: scrape craigslist jobs and output to clip.js

from playwright_webscraper import playwright_runner, scrape_craigslist_jobs
clip(playwright_runner(scrape_craigslist_jobs))

------------------------------------------------------
id: get_reddit_notes
desc: downloads my reddit saved comments. often, will save a few comments. this will immediately download them

from reddit_script import *
download_reddit_saved_comments_as_notes()

------------------------------------------------------

id: None
desc: copies the latest file (probably a resume) to my resume file

file = most_recent_file()
ref = {
    "resume": "Resume",
    "cv": "Cover Letter",
    "letter": "Cover Letter",
}
key = match(file, re_wrap(ref), flags = re.I)
if key:
    key = ref[key]
    outpath = "Kevin Lee {key}.pdf"
    cpfile(file, outpath)


------------------------------------------------------

status: in_progress
desc: creates a local git directory
import os
from githubscript2 import run


def create(g):
    dir = choose(get_unlisted_git_directories())
    g.create_local_directory(str(dir))

run(create)


------------------------------------------------------
id: combine_files_together
desc: first used to combine typ files together

def combine_files_together(dir_key, ext):

    dir = Path("/home/kdog3682/" + dir_key)
    files = list(dir.glob("*" + ext))
    items = map(files, lambda x: x.read_text())
    items
    s = join(items)
    clip(s, openIt = 1)

combine_files_together("2024", "typ")


------------------------------------------------------
id: generate_dialogue_prompt_for_chatgpt
desc: reads the raw file and reads the prompt file ... merges them together

def generate_dialogue_prompt_for_chatgpt():
    """
        reads the instruction file
        reads the raw file
        prepends it to the start
        clips and opens it

    """

    raw = "/home/kdog3682/2024-writing/shsat_math/percent_more_than/raw.txt"
    instructions = "/home/kdog3682/2024/gpt-math-instructions.txt"
    clip(read(instructions) + "\n\n" + read(raw), openIt = 1)

generate_dialogue_prompt_for_chatgpt()

------------------------------------------------------
id: move_most_recent_downloaded_file_to_gdrive_transfer_directory
desc: self-explanatory

def move_most_recent_downloaded_file_to_gdrive_transfer_directory():
    cpfile(most_recent_file(), gdrive_transfer_dir)

move_most_recent_downloaded_file_to_gdrive_transfer_directory()
------------------------------------------------------
status: not in use
id: foo 
desc: i think it recursively cleans up a directory ... for unwanted files

def foo():
    
    while True:
        dir = Path(dldir)

        pprint(list(dir.iterdir()))
        query = input("choose a glob query")
        files = dir.glob(query)
        ignore = anti_choose(files)
        for file in files:
            if file in ignore:
                continue
            else:
                trash(file)



------------------------------------------------------
id: copy current file to drive

copy_file_to_drive("$file", dir = "")


------------------------------------------------------
id: copy curent file to drive/Transfers

copy_current_file_to_drive("$file", dir = "Transfers")
printdir(gdrive_transfer_dir)


------------------------------------------------------
id: write_toc
desc: turns the current directory into a toc

from create_toc import write_toc, get_directory_sub_paths 

# dir = "/home/kdog3682/GITHUB/typst-packages/packages/preview"
# dir = "/home/kdog3682/GITHUB/typst-packages/packages/preview/cetz"
# dir = "/home/kdog3682/typst-packages"
# name = "typst-packages-root"

dir = choose(get_directory_sub_paths("$file"))
name = ask("choose a toc name for $dir")
write_toc(dir, name)

------------------------------------------------------
id: print_typst_rough_draft
desc: turns the current file into a typst pdf file (2 columns). used for previewing rough drafts. current use: percents more than math dialogue. need to print it out to come up with a parsing strategy

status: working
todo: maybe not the best idea to ... number the typ


import time

def get_mmgg_json(file):
    file_name = sub(remove_extension(tail(file)), "[-_]+", " ")
    body = split(read(file), "\n\n+")
    json_data = {
        "title": file_name,
        "body": body,
    }
    return json_data


json_data = get_mmgg_json("$file")
compile_typst("mmgg.typ", "test.pdf", data = json_data)

------------------------------------------------------
id: rename_last_downloaded_file
status: working

def rename_last_downloaded_file():
    file = str(most_recent_file())
    move_file(file, rename_file(file))

rename_last_downloaded_file()


------------------------------------------------------
id: copy_last_downloaded_file_to_2024
status: working

def copy_last_downloaded_file_to_2024():
    file = str(most_recent_file())
    copy_file(file, npath("/home/kdog3682/2024/", file))

copy_last_downloaded_file_to_2024()

------------------------------------------------------
id: print stuff
s = """

1706298473 /home/kdog3682/2024-typst/src/archive.typ
1706300223 /home/kdog3682/2024-typst/src/canvas-utils.typ
1706305710 /home/kdog3682/2024-typst/src/todo.typ
/home/kdog3682/2024-typst/src/ex-riemann-graph.typ
1706318150 /home/kdog3682/2024-typst/src/ex-multiple-choice-item.typ
1706320362 /home/kdog3682/2024-typst/src/draft-shsat-ws-1.typ
1706320829 /home/kdog3682/2024-typst/src/draft-shsat-ws-2-small-version.typ
"""
# r = "/home\S+"
# m = findall(s, r)
# data = [{"title": remove_extension(tail(a)), "body": read(a)} for a in m]
# assert data
data = None
compile_typst("code-printer.typ", data = data)



------------------------------------------------------
id: push dir

from githubscript2 import run

# def fn(g):
    # g.initialize_local_directory("/home/kdog3682/2024-typst/")

run(fn)

------------------------------------------------------
id: move_and_rename_file

def move_and_rename_file():
    file = str(most_recent_file())
    name = ask("choose a name for $file")
    # dir = "/home/kdog3682/2024-typst/mmgg-assets/"
    ref = {
        "2024": "/home/kdog3682/2024/",
        "typst": "/home/kdog3682/2024-typst/",
        "typst-chess": "/home/kdog3682/2024-typst/chess-assets/",
        "mmgg-chess": "/home/kdog3682/2024-mmgg/chess-assets/",
    }
    s = prompt("choose a starting dir key: for replacement", ref)
    dir = sub(s, re_wrap(ref, "start"), lambda x: ref.get(x.group(0)))
    assert is_dir(dir)
    move_file(file, dir + add_extension(name, file))

move_and_rename_file()

------------------------------------------------------
id: test pdf to dldir

# copy_file("/home/kdog3682/2023/test.pdf", dldir)
# should use junegunn with this.
# you can enact a name

--------------------------

id: zipping a chrome extension

from zipscript import zip

dir = '/home/kdog3682/2024-chrome-extensions/web-nanny/0.0.1/'
out = '/home/kdog3682/2024-chrome-extensions/web-nanny/dist'
out = '/home/kdog3682/2024-chrome-extensions/web-nanny/dist/0.0.1.zip'
zip(map(listdir(dir), str), out)

--------------------------------
id: clean up vim files

pprint(cleanup_empty_viminfo_files())
