from gapi_setup import *
from utils import *
from pprint import pprint

def mkdir(drive, name):
    metaData = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    return drive.files.create(
        body=metaData, fields="id"
    ).execute()

def mkfile(drive, file, directory_id):
    metaData = {
        "name": tail(file),
        "parents": [directory_id],
    }

    media = MediaFileUpload(
        file, mimetype=mimeTypeFromFile(file)
    )

    return drive.files.create(
        body=metaData, media_body=media, fields="id"
    ).execute()

def is_google_id(s):
    r = '[\d-_][a-zA-Z]'
    return is_string(s) and len(s) > 20 and len(re.findall(r, s)) >= 4
def rmfile(drive, x):
    return drive.files.delete(fileId=resolve_id(x)).execute()

class GoogleDrive:
    def __init__(self):
        self.files = servicer("drive")

    def get(self, *args, **kwargs):
        opts = create_query(*args, **kwargs)
        size = kwargs.get("size", 0)
        pageToken = None
        store = []

        while True:
            response = self.files.list(
                pageToken=pageToken,
                **opts,
            ).execute()
            store.extend(response.get("files", []))
            if size > 10:
                pageToken = response.get("nextPageToken")
            if size > len(store):
                return store
            if not pageToken:
                return store



def create_query(s = "", after = 0, mimetype = 0, before = 0, name = 0, size = 0, ascending = 0, descending = 0):
    if s:
        return create_query(**get_kwargs(s))

    fields = [ "id", "name" ]
    reqs = []
    reqs.append("trashed = false")
    if mimetype:
        reqs.append(f"mimeType='{mime_types.get(mimetype)}'")

    if name:
        reqs.append(f"name contains '{name}'")
    if before:
        date = parse_date_string(before)
        sign = "<"
        d = datetime.utcnow() - timedelta(**date)
        s = d.isoformat() + 'Z'
        reqs.append(f"modifiedTime {sign} '{s}'")
    if after:
        date = parse_date_string(after)
        sign = ">"
        d = datetime.utcnow() - timedelta(**date)
        s = d.isoformat() + 'Z'
        reqs.append(f"modifiedTime {sign} '{s}'")


    query = " and ".join(reqs)
    fieldString = ','.join(fields)
    if size != 1:
        fields = f"files({fieldString})"
    else:
        fields = f"files({fieldString})"
    payload =  { "q": query, "fields": fields }

    if ascending:
        payload["orderBy"] = 'modifiedTime desc'
    elif descending:
        payload["orderBy"] = 'modifiedTime desc'
    if size:
        if size > 10:
            size = 10
            payload["fields"] = "nextPageToken, " + fields
        payload["pageSize"] = size
    else:
        payload["pageSize"] = 1

    pprint(payload)
    return payload


def parse_date_string(date_str):
    ref = {
       'today': '1 day',
       'yesterday': '2 days',
    }
    date_str = ref.get(date_str, date_str)
    pattern = r'(\d+)\s*(day|hour|minute|second|week|month|year)s?'
    matches = re.findall(pattern, date_str, re.IGNORECASE)
    ref = {
       'years': 365,
       'weeks': 7,
       'months': 30,
    }

    time_dict = {'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0}
    for value, unit in matches:
        unit = unit.lower() + "s"
        if unit in ref:
            unit = 'days'
            time_dict[unit] += int(value) * multiplier
        else:
            time_dict[unit] += int(value)

    return time_dict


def delete_files(query):
    drive = GoogleDrive()
    files = drive.get(query)
    verify(files, "are you sure you wish to delete these files?")
    for file in files:
        print(rmfile(drive, file))

def get_file(**kwargs):
    kwargs["size"] = 1
    drive = GoogleDrive()
    files = drive.get(**kwargs)
    return files[0]
