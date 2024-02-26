dldir = "/mnt/chromeos/MyFiles/Downloads/"
drivedir = "/mnt/chromeos/GoogleDrive/MyDrive/"
rootdir = "/home/kdog3682"
tocfile = "/home/kdog3682/2024/toc.txt"
typstdir = "/home/kdog3682/GITHUB/typst"
typstpackagedir = "/home/kdog3682/GITHUB/typst-packages"
loremdir = "/home/kdog3682/LOREMDIR"
hugodir = "/home/kdog3682/2024/quickstart"
githubdir = "/home/kdog3682/GITHUB"
gdrive_transfer_dir = "/mnt/chromeos/GoogleDrive/MyDrive/Transfers"

import os
from pprint import pprint
import sys
import inspect
import env
from datetime import datetime, timedelta
import regex as re
from pathlib import Path, PosixPath
import json
import shutil
import variables
import webbrowser


clip_dot_pdf = "/home/kdog3682/2024/clip.pdf"
test_dot_pdf = "/home/kdog3682/2024/test.pdf"


shellescapedict = {
    "newline": "\n",
    "sq": "'",
    "rcb": "}",
    "lcb": "{",
    "lt": "<",
    "at": "@",
    "gt": ">",
    "caret": "^",
    "percent": "%",
    "star": "*",
    "ampersand": "&",
    "underscore": "_",
    "dollar": "$",
    "backslash": "\\\\",
    "bs2": "\\",
    "hash": "#",
    "colon": ":",
    "dq": '"',
    "dot": ".",
    "s": " ",
    "rp": ")",
    "lp": "(",
    "exc": "!",
    "nl": "\n",
}

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


