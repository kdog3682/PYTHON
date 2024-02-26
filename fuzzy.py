from utils import *
from fuzzywuzzy import process
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

# Directory containing files (change this to your directory)

directories = [
    "2024-writing",
    "2024-writingaasd",
]
dir_completer = WordCompleter(directories)
pprint(directories)
selected_dir = prompt('Select a directory: ', completer=dir_completer)
best_match = process.extractOne(selected_file, files)[0]
files = map(listdir(best_match), str)

file_completer = WordCompleter(files)
selected_file = prompt('Select a file: ', completer=file_completer)
best_match = process.extractOne(selected_file, files)[0]

print(best_match)

