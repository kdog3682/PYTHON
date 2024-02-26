import dropbox
import env
from utils import *

# Define access token, local file, and Dropbox destination
local_file_path = '/path/to/your/local/file'
dropbox_destination_path = "/foobar.py"

def init_dropbox():
    dbx = dropbox.Dropbox(env.dropboxtoken)
    return dbx


def dropbox_upload_file(dbx, file, outpath):
    bytes = read_bytes(file)
    try:
        dbx.files_upload(bytes, outpath, mode=dropbox.files.WriteMode('overwrite'))
        print(f'Successfully uploaded {local_file_path} to {dropbox_destination_path}')
    except dropbox.exceptions.ApiError as err:
        print(f'API error: {err}')


dbx = init_dropbox()
dropbox_upload_file(dbx, "/home/kdog3682/PYTHON/dropbox_script.py", dropbox_destination_path)
