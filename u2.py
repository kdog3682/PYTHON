
def get_dirs_recursive(root):
    root_dir = Path(root)
    files = []

    def recurse(directory):
        for path in directory.iterdir():
            if default_path_ignore(path):
                continue
            if path.is_dir():
                recurse(path)
                files.append(str(path))

    recurse(root_dir)
    return files


def git_push_directories(dirs):
    template = """
        cd $1
        git add .
        git commit -m 'pushing directory'
        git push
    """

    for dir in dirs:
        print(system_command(template, dir))


def get_git_status_and_last_modified(directories):
    import os
    import subprocess
    git_info = {}
    o = ""

    for dir_path in directories:
        if not is_git_directory(dir_path):
            continue

        o += "dir: " + dir_path + "\n"
        os.chdir(dir_path)
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        status_lines = result.stdout.splitlines()

        files = []
        ref = {
           '??': 'created',
           'M': 'modified',
        }
        for line in status_lines:
            status, file_path = line[:2].strip(), line[3:].strip()
            if not file_path:
                continue
            if not is_file(file_path):
                continue
            status = ref.get(status, status)
            mtime = os.path.getmtime(file_path)
            dt = datetime.fromtimestamp(mtime)
            expr = pluralize_unit(days_ago(dt), "days")
            last_modified = strftime("datetime", dt)
            last_modified += f" ({expr} ago)"
            s = {
                'name': tail(file_path),
                'date': status + " " + last_modified,
            }
            files.append(s)
            for k,v in s.items():
                o += f"  {k}: {v}\n"
            o += "\n"

        o += "\n\n"
        # git_info.append({"dir": dir_path, "contents": files})

    outpath = "/home/kdog3682/2024/git-status.01-14-2024.txt"
    outpath = "/home/kdog3682/2024/git-status.01-15-2024.txt"
    write(outpath, o)



directories = [
"/home/kdog3682/2024/", "/home/kdog3682/2023/", "/home/kdog3682/.vim/ftplugin/", "/home/kdog3682/PYTHON/"
]

# git_push_directories(directories)
# get_git_status_and_last_modified(directories)


def write_readme_file(dir):
    return 
    if not is_file('README.md') and empty(os.listdir(dir)):
        write('README.md', 'howdy from ' + dir)


def unzip_and_move_executable_in_progress():
    """
        used for downloading hugo but it didnt work
    """
    file = get_most_recent_file()
    filename = tail(file)
    key = match(filename, "[a-zA-Z]+")

    print(system_command(""" 
        cd $directory
        tar -xvf $file 
    """, dldir, filename))
    unzipped_file = get_most_recent_file()
    file_path = Path(unzipped_file)
    contents = list(file_path.iterdir())
    content = choose(contents)
    content_path = str(content)
    print(system_command("cp $content_path /usr/local/bin", content_path))
    key = content.name
    print(system_command(""" $key --version """, key))


def get_most_recent_file(directory):
    dir_path = Path(directory)
    files = filter(dir_path.iterdir(), is_public_path)
    file = max(files, key=lambda f: f.stat().st_mtime)
    return str(file)


def get_files_recursive(root, fileRE = None, dirIgnoreRE = None):
    root_dir = Path(root)
    files = []

    def recurse(directory):
        for path in directory.iterdir():
            if path.is_dir():
                if dirIgnoreRE and test(path.name, dirIgnoreRE):
                    continue
                recurse(path)
            elif path.is_file():
                if fileRE and not test(path.name, fileRE):
                    continue
                files.append(str(path))

    recurse(root_dir)
    return files

def copy_last_downloaded_file_into_active_dir():
    name = file_prompt()
    file = most_recent_file()
    active_dir = get_dir("active_dir")
    outpath = npath(active_dir, name)
    debug(file, outpath)
    shutil.copy(file, outpath)
    print("success!")
    # announce("copied last downloaded file: $1 to $2", file, outpath)


def get_sentences(text):
    """
    Split the text into sentences.

    If the text contains substrings "<prd>" or "<stop>", they would lead 
    to incorrect splitting because they are used as markers for splitting.

    :param text: text to be split into sentences
    :type text: str

    :return: list of sentences
    :rtype: list[str]
    """
    alphabets= "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov|edu|me)"
    digits = "([0-9])"
    multiple_dots = r'\.{2,}'
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences]
    if sentences and not sentences[-1]: sentences = sentences[:-1]
    return sentences
