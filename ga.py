from __future__ import print_function
from pprint import pprint
from base import *

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
import mimetypes
from email.message import EmailMessage
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import base64
import env
import time
import io
import os
import requests
import shutil


def relaxTokenScope():
    os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"


relaxTokenScope()
creds = None


class GoogleSearch:
    def __init__(self, **kwargs):
        service = getService("search", tokenfile="token2")
        self.cse = service.cse()
        self.results = self.search(**kwargs)

    def search(self, q=None, amount=50, image=0):
        if not q:
            return

        kwargs = {}
        if image:
            kwargs["searchType"] = "image"
            kwargs["fileType"] = "png,jpg,svg"

        def runner(cse, start, num):
            return cse.list(
                q=q,
                key=env.googlesearchapikey,
                cx=env.googlesearchengineid,
                start=start,
                num=num,
                **kwargs,
            ).execute()

        store = []
        getter = objectf("title link snippet")
        for i in range(0, amount, 10):
            num = min(amount, 10)
            response = runner(self.cse, i, num)
            if response:
                items = response.get("items")
                items = map(items, getter)
                store.extend(items)
            else:
                break

        if image:
            return downloadImages(store, q)
        else:
            return store


def downloadImage(url, name):
    r = requests.get(url)
    if r.status_code == 200:
        with open(name, "wb") as f:
            f.write(r.content)
            print("Image sucessfully Downloaded: ", name)
            return name
    else:
        print("Image Couldn't be retreived", name)


class GoogleDocument:
    def __init__(
        self,
    ):
        service = getService("docs")
        self.document = service.documents()

    def get(self, id):
        return self.document.get(documentId=id).execute()


def getService(
    key="classroom", reset=0, tokenfile="token.json"
):
    global creds
    versionRef = {
        "classroom": {"version": "v1"},
        "drive": {"version": "v3"},
        "gmail": {"version": "v1"},
        "docs": {"version": "v1"},
        "youtube": {"version": "v3"},
        "search": {"version": "v1", "name": "customsearch"},
    }

    ref = versionRef.get(key)
    version = ref.get("version")
    if ref.get("name"):
        key = ref.get("name")
    creds = getCreds(tokenfile)
    service = build(key, version, credentials=creds)
    print("Service success: returning service for ", key)
    return service




def superIsFile(file):
    return normpath(dldir, file)
    assert file


def queryHelper(key, mode=0):
    if mode == "mimeType":
        return f"mimeType='{key}'"

    if mode == "id":
        return f"'{key}' in parents"

    if mode == "folder":
        return f"mimeType = 'application/vnd.google-apps.folder' and name = '{key}'"


class GoogleDrive:
    def downloadFile(self, x=0, outpath=0):
        if isObject(x):
            file = x
        elif isString(x):
            file = self.getFiles2(name=x)
        else:
            file = self.getFiles2()

        fileId = file.get('id')
        fileName = outpath or removeDateString(file.get('name'))
        fileName = addExtension(npath(dldir, fileName), 'pdf')

        r = self.files.export(
            fileId=fileId, mimeType="application/pdf"
        )

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, r)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

        fh.seek(0)
        with open(fileName, "wb") as f:
            shutil.copyfileobj(fh, f, length=131072)
        ofile(fileName)

    def getFiles2(self, folder=0, name=0, r=0, e=0, n=1):
        if folder:
            q = f"mimeType = 'application/vnd.google-apps.folder' and name = '{folder}'"
            folders = driveGetter(self, q=q, pageSize=1)
            folder = folders[0]
        else:
            folder = self.files.get(fileId="root").execute()

        q = createq(folder=folder)
        if e:
            q += f" and mimeType = {getMime(e)}"


        results = driveGetter(self, q=q, pageSize=n)
        if name:
            results = filter(
                results, lambda x: test(name, x.get("name"), flags=re.I)
            )
        dprint(
            results=results, lengthMatch=len(results) == n
        )
        if n == 1:
            return smallify(results)
        return results

    def downloadFiles(self, **kwargs):
        files = self.getFiles2(**kwargs)
        for file in files:
            f = googleDriveDownloadFile(self, file)
            ofile(f)

    def searchFile(self, query):
        pageToken = None

        kwargs = {
            "q": queryHelper(query),
            "spaces": "drive",
            "fields": ["nextPageToken", "files(id, name)"],
            "pageToken": pageToken,
        }

        response = service.files().list(**kwargs).execute()
        return response.get("files", [])

    def deleteFile(self, fileId):
        self.files.delete(fileId=fileId).execute()
        print("deleting file", fileId)

    def clearFolder(self, folderId):

        fileIds = self.getFileIds(folderId)
        for fileId in fileIds:
            self.deleteFile(fileId)

    def getFileIds(self, folderId):
        f = lambda x: x.get("id")
        return map(self.getFiles(folderId), f)

    def getFiles(self, folderId):
        query = queryHelper(folderId, mode="id")

        pageToken = None
        store = []
        while True:
            response = self.files.list(
                q=query,
                pageSize=10,
                pageToken=pageToken,
                fields="nextPageToken, files(id, name)",
            ).execute()

            store.extend(response.get("files", []))
            pageToken = response.get("nextPageToken")

            if not pageToken:
                return store

    def getFolderId(self, folderName):
        query = (
            f"mimeType = 'application/vnd.google-apps.folder' and name='{folderName}'",
        )

        folders = (
            self.files.list(q=query).execute().get("files")
        )
        return folders[0].get("id")

    def createFolder(self, name):
        print("creating folder", name)
        metaData = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        folderResponse = self.files.create(
            body=metaData, fields="id"
        ).execute()
        return folderResponse.get("id")

    def uploadFile(self, file):

        metaData = {
            "name": tail(file),
            "parents": [self.uploadDestination],
        }

        media = MediaFileUpload(
            file, mimetype=mimeTypeFromFile(file)
        )

        fileResponse = self.files.create(
            body=metaData, media_body=media, fields="id"
        ).execute()

        return fileResponse.get("id")

    def __init__(self):
        service = getService("drive")
        self.service = service
        self.files = service.files()
        classroomUploadsDir = (
            "1sD9pfkJVa0WBH_FPygLQ-gCaJQRGaO-B"
        )
        self.uploadDestination = classroomUploadsDir
        self.doDownloadFile = True

    def getFile(self, fileObject):
        fileId = fileObject.get("id")
        name = fileObject.get("title")

        if self.doDownloadFile:
            data = self.files.get_media(
                fileId=fileId
            ).execute()
            writeBuffer(name, data)

        return name

    def getFileMetaData(self, fileId):
        return self.files.get(fileId=fileId).execute()


class GoogleClassroom:
    def createResource(self, file, fileId=None):
        if not fileId:
            fileId = self.drive.uploadFile(file)
        materials = createMaterials(fileId)
        resource = self.getResourceMetaInfo(file)
        resource["materials"] = materials
        return resource

    def getStudentId(self, name):
        student = find(self.studentList, lambda x: x.get('name') == name)
        if student:
            return student.get('id')

    def createCourseWork(self, resource, individualStudents=0):

        assigneeMode = 'ALL_STUDENTS'
        individualStudentOptions = None

        if individualStudents:
            print("this is an individual coursework for", individualStudents)
            assigneeMode = 'INDIVIDUAL_STUDENTS' 
            self.studentList = self.getStudents()
            ids = map(xsplit(individualStudents), self.getStudentId)
            ids = filter(ids)
            if not ids:
                raise Exception('no ids found for individual students')
            individualStudentOptions = {
                'studentIds': ids
            }
        
        return self.courseWork.create(
            courseId=self.courseId, body=resource,
            assigneeMode=assigneeMode,
            individualStudentOptions=individualStudentOptions
        ).execute()

    def onlyEmail(self, files):
        store = []
        for file in files:
            file = addExtension(file, "pdf")
            fileId = self.drive.uploadFile(file)
            fileName = tail(file)
            store.append(
                {
                    "id": fileId,
                    "name": fileName,
                }
            )

        appScript(
            "cwtEmailCoursework", store, use="css-utils"
        )

    def deleteCourseWork(self, courseWorkIds):
        for id in courseWorkIds:
            try:
                self.courseWork.delete(
                    courseId=self.courseId, id=id
                )
                print("deleted coursework", id)
            except Exception as e:
                print("couldnt delete", id)

    def gradeAllSubmissions(self, data):

        for courseWorkId, v in data.items():
            for student, studentData in v.items():
                print("student", student)
                studentSubmissionId = studentData.get(
                    "submissionId"
                )
                grade = 93

                self.gradeSubmission(
                    courseWorkId, studentSubmissionId, grade
                )

    def getAllSubmissionMedia(self):

        self.getAssignments()
        self.getAssignmentIds()

        assignmentStore = {}

        for id in self.assignmentIds:
            print("running assignmentId", id)
            submissions = self.getStudentSubmissions(id)
            submissionStore = {}

            for submission in submissions:

                studentSubmissionId = submission.get("id")
                studentId = submission.get("userId")

                studentName = self.getStudentName(
                    submission
                )
                print(
                    "getting student submission",
                    studentSubmissionId,
                    studentName,
                )

                attachments = map(
                    submission.get(
                        "assignmentSubmission"
                    ).get("attachments"),
                    lambda x: x.get("driveFile"),
                )

                attachmentNames = map(
                    attachments, self.drive.getFile
                )
                submissionStore[studentName] = {
                    "attachments": attachmentNames,
                    "submissionId": studentSubmissionId,
                    "studentId": studentId,
                }

            assignmentStore[id] = submissionStore

        return assignmentStore

    def clearFolder(self):
        loc = self.drive.uploadDestination
        self.drive.clearFolder(loc)

    def uploadAssignment(self, file):
        name = removeExtension(tail(file))
        skipClassroom = self.skipClassroom or isSkippable(name)
        fileId = self.drive.uploadFile(file)
        print('Uploaded File to GoogleDrive:', name)
        nameRE = '^(?:Ella Wu|Dianna Huang)
        individual = search(nameRE, name)

        if skipClassroom:
            print('Skipping Classroom', name)
        else:
            resource = self.createResource(file, fileId)
            response = self.createCourseWork(resource, individual)
            print('Created GoogleClassroom Coursework')

        return {
            "id": fileId,
            "name": name,
        }

    def getResourceMetaInfo(self, fileName):
        fileName = tail(fileName)

        points = 100
        workType = "ASSIGNMENT"

        if itest("quiz", fileName):
            workType = "QUIZ"
            workType = "ASSIGNMENT"
        elif itest("exam|test", fileName):
            workType = "ASSIGNMENT"
        elif itest("handout|cw|classwork", fileName):
            points = None

        uploadFileName = self.toUploadName(fileName)

        scheduledTime = self.date.get("scheduledTime")
        """
            By default, we always publish homework as draft.
            The only time we do not publish as draft
            is if date of publication == today.
            in this case, scheduledTime = None
            self.asDraft is no longer used
        """

        if scheduledTime:
            publishState = "DRAFT"
        else:
            publishState = "PUBLISHED"

        dueTime = (
            self.date.get("dueTime") if points else None
        )
        dueDate = (
            self.date.get("dueDate") if points else None
        )
        description = self.creationReference.get(
            fileName, ""
        )
        description = ""

        return {
            "state": publishState,
            "scheduledTime": scheduledTime,
            "maxPoints": points,
            "title": uploadFileName,
            "workType": workType,
            "description": description,
            "dueTime": dueTime,
            "dueDate": dueDate,
        }

    def gradeSubmission(
        self, courseWorkId, studentSubmissionId, grade
    ):

        body = {"assignedGrade": grade, "draftGrade": grade}

        try:
            self.studentSubmissions.patch(
                courseId=self.courseId,
                courseWorkId=courseWorkId,
                id=studentSubmissionId,
                updateMask="assignedGrade,draftGrade",
                body=body,
            ).execute()

            self.studentSubmissions.return_(
                courseId=self.courseId,
                courseWorkId=courseWorkId,
                id=studentSubmissionId,
            ).execute()

            print("successful grading")

        except Exception as e:
            print("skip", studentSubmissionId, str(e))

    def printStudentInfo(self):
        students = (
            self.courses.students()
            .list(courseId=self.courseId)
            .execute()
            .get("students")
        )
        info = map(students, lambda x: x.get("profile"))
        normWrite("google.classroom.students.json", info)

    def getStudentName(self, userId):
        if isObject(userId):
            userId = userId.get("userId")

        data = self.userProfiles.get(
            userId=userId
        ).execute()
        return data.get("name").get("fullName")

    def openLink(self):
        ofile(self.classWorkLink)

    def loadClass(self, classKey):
        ref = env.ClassroomRef.get(classKey)
        if not ref:
            ref = env.ClassroomRef.get("g" + classKey)

        self.classWorkLink = ref.get("classWorkLink")
        self.courseName = ref.get("name", classKey)
        self.courseSubject = capitalize(ref.get("subject"))
        self.onlineStudents = ref.get("onlineStudents")
        self.courseId = ref.get("id")
        print(
            "initializing self.courseName", self.courseName
        )
        print("initializing self.courseId", self.courseId)
        print("initializing self.courseWork()")
        print("initializing self.studentSubmissions()")

    def __init__(self, classKey):
        service = getService(key="classroom", reset=0)
        self.loadClass(classKey)
        self.skipClassroom = False

        courses = service.courses()
        courseWork = courses.courseWork()
        self.service = service
        self.userProfiles = service.userProfiles()
        self.courses = courses
        self.courseWork = courseWork
        self.studentSubmissions = (
            courseWork.studentSubmissions()
        )
        self.drive = GoogleDrive()
        print("initializing self.courses()")
        print("GoogleClassroom successfully initialized")
        print("------------------------------")

        self.defaultAssignmentPoints = 100
        self.date = upcomingDateObject("saturday")
        self.creationReference = {}
        self.differentVersionForOnlineStudents = False

        self.labelFileDate = False
        self.asDraft = False
        self.labelFileSubject = False

        self.labelFileDate = True
        self.labelFileSubject = True
        self.asDraft = True

    def toUploadName(self, fileName):
        date = (
            self.date.get("string")
            if self.labelFileDate
            else None
        )
        subject = (
            self.courseSubject
            if self.labelFileSubject
            else None
        )
        name = cleanupFileName(
            fileName, date, prepend=subject
        )
        return name

    def getAssignments(self, amount=None):
        assignments = (
            self.courseWork.list(courseId=self.courseId)
            .execute()
            .get("courseWork")
        )
        if amount:
            assignments = assignments[amount:]

        raise Exception("whats going on here")
        self.assignments = assignments
        return self.assignments

    def getAssignmentIds(self):

        self.assignmentIds = map(
            self.assignments, lambda x: x.get("id")
        )
        return self.assignmentIds

    def getStudents(self):
        students = (
            self.courses.students()
            .list(courseId=self.courseId)
            .execute()
            .get("students")
        )

        def f(student):
            name = getStudentInfo(student).get("name")
            if name in self.onlineStudents:
                return True

        students = filter(students, f)
        return students

    def getStudentSubmissions(self, assignmentId):
        return (
            self.studentSubmissions.list(
                courseId=self.courseId,
                courseWorkId=assignmentId,
            )
            .execute()
            .get("studentSubmissions")
        )


p = {
    "490513487908": {
        "Kevin Lee": {
            "attachments": ["clip.js"],
            "submissionId": "Cg4I-sLXhvsPEKSwh6ejDg",
            "studentId": "107883965519367458050",
        }
    },
    "490213642198": {
        "Kevin Lee": {
            "attachments": ["G4 & G5 Handout.pdf"],
            "submissionId": "Cg4I-sLXhvsPENafipiiDg",
            "studentId": "107883965519367458050",
        }
    },
    "28537084958": {
        "Kevin Lee": {
            "attachments": [
                "sf_cwpcc5.pdf",
                "Image_created_with_a_mobile_phone.png",
            ],
            "submissionId": "Cg0I-sLXhvsPEJ64xadq",
            "studentId": "107883965519367458050",
        }
    },
}


def main(
    grades=0,
    deletions=0,
    printStudentInfo=0,
    assignments=0,
    downloadMedia=0,
    classKey="emc",
    uploadMedia=0,
    onlyEmail=0,
):
    assert classKey == "emc"
    room = GoogleClassroom(classKey)

    if onlyEmail:
        return room.onlyEmail(onlyEmail)

    if uploadMedia:
        return room.uploadAndEmail()

    if downloadMedia:
        data = room.getAllSubmissionMedia()
        writeVariable("classroomSubmissionMedia.js", data)
        normOpen("google-classroom.html")

    if grades:
        room.gradeAllSubmissions(grades)

    if deletions:
        room.deleteCourseWork(deletions)

    if printStudentInfo:
        room.printStudentInfo()

    if assignments:
        room.uploadAssignments(assignments)

        # announcements = self.service.announcements()
        # announcements.create(courseId=self.courseId, body)
        # Hello everyone,
        # Course Work for this week has been posted.
        # Here is the link to the homework.
        # Sometimes I have to add additional comments.
        # (Link URL)
        # Posting everything. It is easier for me to grade. It is less work for you.
        # by adding in additional information,
        # it seems to make everything more cohesive
        # if english is not the primary language:
        # the various elements may appear more difficult
        # there will always be a large gap
        # everything is about how energy flows downwards...


def createMaterials(fileId):
    links = []
    materials = [
        {"driveFile": {"driveFile": {"id": fileId}}}
    ]
    for url in toArray(links):
        materials.append(
            {"link": {"title": "vvv", "url": fixUrl(url)}}
        )
    return materials


def getCreds(tokenfile, reset=0):
    global creds
    tokenfile = jsondir + tokenfile
    # print(tokenfile)
    # raise Exception()
    googleScopes = env.googleScopes
    # googleScopes = env.customsearchScopes
    # googleScopes = env.youtubeScopes
    debug = 0
    # debug = 1
    # reset = 1

    def get_creds(f):
        if isfile(f):
            print("returning existing token file", f)
            return Credentials.from_authorized_user_file(
                f, googleScopes
            )
        else:
            if debug:
                input("creating oauth flow credentials")
            flow = (
                InstalledAppFlow.from_client_secrets_file(
                    env.credentialfile, googleScopes
                )
            )

            creds = flow.run_local_server(port=0)
            writeCreds(f, creds)
            return creds

    tokenfile = jsondir + addExtension(
        tail(tokenfile), "json"
    )

    if creds:
        if creds.expired:
            if debug:
                input("the credentials are expired")
            creds.refresh(Request())
        elif isfile(tokenfile):
            if debug:
                input("returning existing credentials")
            return get_creds(tokenfile)
        else:
            return make_creds(tokenfile)

        return creds
    else:
        return get_creds(tokenfile)


def writeCreds(file, creds):
    with open(file, "w") as f:
        f.write(creds.to_json().replace('"2022', '"2023'))


def downloadImages(store, q):
    chdir(dldir)
    names = []
    links = (
        map(store, lambda x: x.get("link"))
        if isObject(store[0])
        else store
    )
    for i, link in enumerate(links):
        e = search("\\b(?:jpg|png|svg)\\b", link)
        if not e:
            print("error couldnt find extension", link)
            continue

        name = addExtension(q + str(i + 1), e)
        try:
            downloadImage(link, name)
            names.push(name)
        except Exception as e:
            print("error", link, e)

    return names


def openYoutube(id):
    s = "http://www.youtube.com/watch?v=" + id
    return ofile(s)


def foo():
    # doesnt need to be here
    tokenfile = jsondir + env.tokenfile

    if not creds and not reset and isfile(tokenfile):
        print("getting credentials")
        creds = Credentials.from_authorized_user_file(
            tokenfile, env.googleScopes
        )

    if not creds or not creds.valid:
        print("getting credentials")
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = (
                InstalledAppFlow.from_client_secrets_file(
                    env.credentialfile, env.googleScopes
                )
            )

            creds = flow.run_local_server(port=0)
            with open(tokenfile, "w") as token:
                print("writing token file", tokenfile)
                token.write(
                    creds.to_json().replace(
                        '"2022', '"2030'
                    )
                )


class GoogleYoutubeSearch:
    def __init__(self, **kwargs):

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        service = getService("youtube", tokenfile="token3")
        self.openYoutubeUrl = 0
        self.youtube = service.search()
        self.video = service.videos()
        self.results = self.search(**kwargs)

    def parse(self, item):
        id = item.get("id").get("videoId")
        kwargs = dict(part="statistics", id=id)
        response = self.video.list(**kwargs).execute()

        if self.openYoutubeUrl:
            openYoutube(id)

        statistics = response.get("items")[0].get(
            "statistics"
        )
        snippet = item.get("snippet")
        return {
            **statistics,
            **snippet,
        }

    def search(self, q=None, amount=50):
        kwargs = {
            "q": q,
            "part": "snippet",
            "maxResults": amount,
        }
        response = self.youtube.list(**kwargs).execute()
        items = response.get("items")
        return [self.parse(item) for item in items]


# def fastEmail():
# from ga import GoogleEmail
# GoogleEmail.


class GoogleEmail:
    def __init__(self):
        service = getService("gmail")
        self.users = service.users()
        self.messages = self.users.messages()

    def createFilter(
        self,
        sender=0,
        labelName="trash",
        size=0,
        subject=0,
        query=0,
    ):
        # starred important
        body = {
            "criteria": {},
            "action": {
                "addLabelIds": [labelName.upper()],
                "removeLabelIds": ["INBOX"],
            },
        }
        if size:
            filter["criteria"]["size"] = size
        if subject:
            filter["criteria"]["subject"] = subject
        if query:
            filter["criteria"]["query"] = query
        if sender:
            filter["criteria"]["from"] = sender

        result = (
            self.users.settings()
            .filters()
            .create(userId="me", body=body)
            .execute()
        )

        print(f'Created filter with id: {result.get("id")}')

    def testing():
        print("not completing working right now")
        for m in self.getMessages():
            self.getMessage(m)
            break

    def getMessage(self, m):
        data = {}
        id = m.get("id")
        message = self.messages.get(
            userId="me", id=id
        ).execute()
        return pprint(message)
        print(
            "not working at the moment because of scope problem"
        )
        payload = message["payload"]
        headers = payload["headers"]

        for h in headers:
            if h["name"] == "Subject":
                data["subject"] = h["value"]

            elif h["name"] == "Date":
                data["date"] = h["value"]

            elif h["name"] == "From":
                data["from"] = h["value"]

        data["snippet"] = message["snippet"]
        return data

    def getMessages(self, labels=["INBOX", "UNREAD"]):
        return (
            self.messages.list(userId="me", labelIds=labels)
            .execute()
            .get("messages")
        )

    def test(self, *files):
        a = jsdir + "test.pdf"
        return self.emailFiles([a, a])

        body = messageWithAttachment(
            env.kdogEmail,
            env.myEmail,
            "test",
            "",
            '<p style="color:red">hi</p>',
            jsdir + "test.pdf",
        )

        kwargs = dict(userId="me", body=body)
        response = self.messages.send(**kwargs).execute()
        pprint(response)

    def emailFiles(self, files):
        drive = GoogleDrive()
        ids = map(files, drive.uploadFile)
        googleAppScript("Action", "emailFiles", ids)

    def email(self):
        message = EmailMessage()
        message.set_content("This is automated draft mail")
        message["From"] = env.kdogEmail
        message["To"] = env.myEmail
        message["Subject"] = "Automated draft"
        em = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()
        body = {"raw": em}
        kwargs = dict(userId="me", body=body)
        response = self.messages.send(**kwargs).execute()
        return response


def google(q="dogs", amount=5, youtube=0):
    if youtube:
        gs = GoogleYoutubeSearch(q=q, amount=amount)
    else:
        gs = GoogleSearch(q=q, amount=amount, image=1)

    if gs.results:
        pprint(gs.results)

    # todo https://developers.google.com/youtube/v3/guides/uploading_a_video #helpnotes


def driveGetter(self, q, pageSize=3, get=1):
    fields = "nextPageToken, files(id, name)"
    items = self.files.list(
        q=q, pageSize=pageSize, fields=fields
    ).execute()
    if get:
        return items.get("files", [])
    else:
        return items


def getMime(s):
    e = getExtension(s)
    return (
        env.mimedict.get(s)
        or env.mimedict.get(e)
        or "application/pdf"
    )


def googleDriveDownloadFile(self, file):
    fileId = file.get("id")
    name = file.get("name")
    mimeType = "application/pdf"
    outpath = npath(dldir, addExtension(name, "pdf"))
    print(outpath)
    fh = io.FileIO(outpath, "wb")
    done = False
    try:
        request = self.files.export_media(
            fileId=fileId, mimeType=mimeType
        )
        downloader = MediaIoBaseDownload(fh, request)
        while done is False:
            status, done = downloader.next_chunk()
    except:
        print("errrror")
        return
        raise Exception("it is not working")
        request = self.files.get_media(fileId=fileId)
        downloader = MediaIoBaseDownload(fh, request)
        while done is False:
            status, done = downloader.next_chunk()

    return outpath


# googleDriveDownloadFile(self, fileId):


def googleDriveGetFiles(self, folderId):
    folder = self.files.get(fileId=folderId).execute()
    files = driveGetter(
        self, q=createq(folder), pageSize=1000
    )
    return files


def googleDriveGetFolders(self, folder=0):
    q = "mimeType = 'application/vnd.google-apps.folder'"
    if folder:
        pageSize = 1
    else:
        pageSize = 1000
    if folder:
        q += f" and name = '{folder}'"
    return driveGetter(self, q=q, pageSize=pageSize)



# GoogleDrive()
# print(googleDriveGetFolders(GoogleDrive()))
def createq(folder=0, id=0):
    q = 0
    if folder:
        id = folder.get("id")
    if id:
        q = "'" + id + "' in parents"
    return q


# gd = GoogleDrive()
# ofile(googleDriveDownloadFile(gd, googleDriveGetFiles(gd, '1N5AjWhyNclXRsjUVMG4OcnkRzILb-7aJmNV_XpYJ9G5bRpYeuI00IKkdLWNqqOwEkwfHUxmA')[0]))

# pprint(students)


def getStudentInfo(student):
    profile = student.get("profile")
    emailAddress = profile.get("emailAddress")
    id = profile.get("id")
    name = profile.get("name").get("fullName")
    return {
        "id": id,
        "name": name,
        "emailAddress": emailAddress,
    }


def appendStudentStuff():
    data = googleAppController('getCourses')
    service = getService(key="classroom", reset=0)
    courses = service.courses()
    # Some how, this is the classroom ref.
    #for id in data:
        #courses.get(id)
    room = GoogleClassroom("5")
    students = room.getStudents()
    appendVariable(map(students, getStudentInfo))



def getTitle(item):
    return (
        item.get("assignmentSubmission")
        .get("attachments")[0]
        .get("driveFile")
        .get("title")
    )


def grader(room=0, grade=100):
    if not room:
        keys = ['4', '5']
        for key in keys:
            room = GoogleClassroom("4")
            grader(room)
        return 

    students = room.getStudents()
    for student in students:
        subs = (
            room.studentSubmissions.list(
                courseId=room.courseId,
                courseWorkId="-",
                userId=student.get("userId"),
                states="TURNED_IN",
            )
            .execute()
            .get("studentSubmissions")
        )

        #subs = getUntil(subs, isRecentSubmission)
        pprint(subs)

        for data in subs[0:3]:
            if data.get("associatedWithDeveloper"):
                if test("quiz|exam|test", getTitle(data)):
                    print("hand grade quiz exam test")
                    pass
                else:
                    result = room.gradeSubmission(
                        data.get("courseWorkId"),
                        data.get("id"),
                        grade,
                    )
                    pprint(result)
            else:
                print("not made from console bypass")


def isRecentSubmission(s):
    if not s.get("associatedWithDeveloper"):
        return False
    n = s.get("creationTime")[0:11]
    year, month, day = getNumbers(n)
    date = datetime(year, month, day)
    today = datetime.now()
    delta = today - date
    if delta.days > 15:
        return False

def isSkippable(name):
    r = 'progress|report|announce'
    if test(r, name, re.I):
        return True

class GoogleApp:
    def __init__(self):
        self.drive = GoogleDrive()

    def openDoc(self, name):
        file = self.drive.getFiles2(name=name)
        url = f"https://docs.google.com/document/d/{file.get('id')}"
        ofile(url)

    def downloadDoc(self, name, outpath=0):
        self.drive.downloadFile(name, outpath)
    
#GoogleApp().openDoc('$1')
#GoogleApp().downloadDoc('$1', '$2')
#pprint(snapshotOfDirectory())
