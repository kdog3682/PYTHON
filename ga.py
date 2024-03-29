from __future__ import print_function
UPLOAD_DESTINATION = "1sD9pfkJVa0WBH_FPygLQ-gCaJQRGaO-B"

from datetime import datetime, timedelta

from pprint import pprint
from base import *
from utils import *

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
import mimetypes
import webbrowser
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


class GoogleDocs():
    def __init__(self):
        service = getService("docs")
        self.documents = service.documents()

    def get(self, id):
        return self.documents.get(documentId=id).execute()

    def create(self, title = "untitled"):
        return self.documents.create(body={'title': title}).execute()

    def batchUpdate(self, x, requests):
        id = self.get_id(x)
        return self.documents.batchUpdate(documentId=id, body={'requests': requests}).execute()

    def get_id(x):
        
        if is_google_id(x):
            return x
        if is_string(x):
            drive = GoogleDrive()
            file = drive.getDriveFile(name = x)
            if file:
                documentId = file.get("id")
                return documentId
            return 
        if has(x, "documentId"):
            return x.get("documentId")
        if has(x, "id"):
            return x.get("id")

    def get_doc(self, x):
        id = self.get_id(x)
        if id:
            return self.get(id)
        return x
        
    def getDocContentAsJson(self, x):
        document = self.get_doc(x)
        return json.dumps(document, indent = 2)


def getService(
    key="classroom", reset=0
):
    global creds
    versionRef = {
        "classroom": {"version": "v1"},
        "drive": {"version": "v3"},
        "sheets": {"version": "v4"},
        "gmail": {"version": "v1", 'token_file': 'march2023credtoken'},
        "docs": {"version": "v1"},
        "youtube": {"version": "v3"},
        "search": {"version": "v1", "name": "customsearch"},
    }

    ref = versionRef.get(key)
    version = ref.get("version")
    token_file = addExtension(ref.get("token_file", 'token'), 'json')
    if ref.get("name"):
        key = ref.get("name")
    creds = getCreds(token_file, reset)
    service = build(key, version, credentials=creds)
    blue_colon("returning successful service", key)
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

    def get_file(self, x):
        if isObject(x):
            return 
        elif is_google_id(x):
            return self.files.get(fileId=x).execute()
        elif isString(x):
            raise "aaa"
            return self.files.get(**create_query(name=x))
        else:
            return self.getDriveFile()

    def get_files(self, **kwargs):
        options = create_query(**kwargs)
        response = self.files.list(**options).execute()
        files = response.get('files', [])
        if kwargs.get("size") == 1:
            return files[0] if files else None
        return files
        
    def getDriveFile(self, **kwargs):
        return self.get_files(size = 1, **kwargs)

    def getDocsFromLastWeek(self):
        return self.get_files(type = "document", after = "7days")

    def downloadFile(self, x=0, outpath=0):
        file = self.get_file(name = x)
        fileId = file.get('id')
        fileName = outpath or removeDateString(file.get('name'))

        if fileName == 'Resume':
            fileName = 'Kevin Lee resume'

        return self._download(fileId, fileName)


    def _download(self, fileId, fileName):

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
        return {
            'id': fileId,
            'name': fileName,
        }
    
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


    def delete(self, x):
        if isArray(x):
            return map(x, self.deleteFile)

        return self.deleteFile(x)

    def deleteFile(self, id):
        id = getId(id)
        self.files.delete(fileId=id).execute()

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

        dprint(file)
        prompt()
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
        outpath = npath(dldir, name)

        if self.doDownloadFile:
            data = self.files.get_media(
                fileId=fileId
            ).execute()
            writeBuffer(outpath, data)

        return name

    def getFileMetaData(self, fileId):
        return self.files.get(fileId=fileId).execute()



class GoogleClassroom:
    def view(self, x):

        if isArray(x):
            return map(x, self.view)

        openUrl = True
        item = x


        if hasKey(x, 'materials'):
            x = x.get('materials')[0].get('driveFile')

        if hasKey(x, 'driveFile'):
            x = x.get('driveFile')

        if hasKey(x, 'assignment'):
            item = x.get('assignment').get('studentWorkFolder')
            pprint('viewing student course work')

        if x.get('alternateLink') and openUrl:
            url = x.get('alternateLink')
            webbrowser.open(url)
            return url
        elif x.get('id'):
            id = x.get("id")
            name = x.get("name") or x.get('title')
    
    def getCourseWork(self, x):

        if hasKey(x, 'courseWorkId'):
            id = x.get('courseWorkId')
        elif hasKey(x, 'id'):
            id = x.get('id')
        elif isString(x):
            id = x
        else:
            raise Exception('no id')

        courseWork = self.courseWork.get(courseId=self.courseId, id=id)
        return courseWork.execute()
    
    def createResource(self, file, fileId=None, student=None):
        if not fileId:
            fileId = self.drive.uploadFile(file)
        materials = createMaterials(fileId)
        resource = self.getResourceMetaInfo(file)
        resource["materials"] = materials
        if student:
            print('creating resource for individual student', student)
            id = self.getStudentId(student)
            assert id
            resource['assigneeMode'] = 'INDIVIDUAL_STUDENTS'
            resource['individualStudentsOptions'] = {
                'studentIds': [id]
            }
            if itest('handout|note', file):
                newName = removeExtension(tail(file))
                if not test(student, newName):
                    newName = student + ' - ' + newName

                resource['title'] = newName

        return resource

    def getStudentId(self, name):
        if not hasattr(self, 'studentList'):
            self.studentList = self.getStudents()

        def condition(x):
            studentName = x.get('profile').get('name').get('fullName')
            return studentName == name

        student = find(self.studentList, condition)
        if student:
            return student.get('userId')
            return student.get('profile').get('id')

    def createCourseWork(self, resource):
        return self.courseWork.create(
            courseId=self.courseId, body=resource,
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

    def uploadAssignment(self, file=0, student=0):

        if self.debug:
            file = env.testAssignmentFile

        name = removeExtension(tail(file))
        if student and not test(student, name):
            name = student + ' - ' + name

        skipClassroom = self.skipClassroom or isSkippable(name)
        if self.debug:
            fileId = env.testAssignmentFileId
        else:
            fileId = self.drive.uploadFile(file)
            print('Uploaded File to GoogleDrive:', name, fileId)

        if skipClassroom:
            print('Skipping Classroom', name)
        else:
            resource = self.createResource(file, fileId, student)
            self.createCourseWork(resource)
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
        elif itest("note|handout|cw|classwork", fileName):
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
        self.debug = True if classKey == 'emc' else False

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
            if not self.onlineStudents:
                return True
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

    tokenfile1 = 'token.json'              # the default token file
    tokenfile2 = 'march2023credtoken.json' # gmail everything scope

    ref = {
        tokenfile1: env.googleScopes,
        tokenfile2: env.newGoogleScopes,
        tokenfile2: env.onlyEmailScope,
    }

    tokendir = '/home/kdog3682/RESOURCES/'
    googleScopes = ref.get(tokenfile)
    tokenfile = tokendir + tokenfile

    def get_creds(f):
        if isfile(f) and not reset:
            print("returning existing token file", f)
            return Credentials.from_authorized_user_file(
                f, googleScopes
            )
        else:
            flow = (
                InstalledAppFlow.from_client_secrets_file(
                    env.credentialfile, googleScopes
                )
            )

            creds = flow.run_local_server(port=0)
            writeCreds(f, creds)
            return creds

    tokenfile = "/home/kdog3682/2024/token.json"

    if creds:
        if creds.expired:
            if debug:
                input("the credentials are expired")
            creds.refresh(Request())
        elif isfile(tokenfile):
            return get_creds(tokenfile)
        else:
            return make_creds(tokenfile)

        return creds
    else:
        return get_creds(tokenfile)


def writeCreds(file, creds):
    with open(file, "w") as f:
        year = getYearNumber()
        nextYear = year + 1
        a = '"' + str(year)
        b = '"' + str(nextYear)
        data = creds.to_json().replace(a, b)
        f.write(data)


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
        self.threads = self.users.threads()

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

    def getEmails(self):
        write('my-email-data.json', self.getFirstThreads())
    
    def getThreadMessage(self, threadId):
        thread = self.getThread(threadId)
        message = thread.get('messages')[0]
        return parseEmailMessage(message)
    
    def cleanupEmails(self):
        store = []
        for t in self.getThreads():
            threadId = t.get('id')
            message = self.getThreadMessage(threadId)
            if shouldDeleteEmail(message):
                s = f"{message.get('sender')} ... {message.get('sender')}"
                store.append(s)
                ids.append(threadId)
        
        prompt(deletions=store)
        for id in ids:
            self.deleteThread(id)

    def getFirstThreads(self):
        store = []
        for t in self.getThreads():
            threadId = t.get('id')
            thread = self.getThread(threadId)
            message = thread.get('messages')[0]
            data = parseEmailMessage(message)
            data['threadId'] = threadId
            store.append(data)

        return store

    def testing(self):
        # it works
        threads = self.getThreads()
        for thread in threads:
            firstMessage = self.getThread(thread)
            break

    def getFirstMessages(self):
        
        threads = self.getThreads()
        messageStore = []
        for thread in threads:
            id = thread.get('id')
            thread = self.getThread(id)
            messages = self.getThread(id)
            if len(messages > 1):
                continue
            message = parseEmailMessage(messages[0])
            message['id'] = id
            messageStore.append(message)

        return messageStore

    

    def deleteThread(self, id):
        if isObject(id): id = id.get('id')

        self.threads.delete(
            userId="me", id=id
        ).execute()
    

    def deleteMessage(self, id):
        if isObject(id): id = id.get('id')

        self.messages.delete(
            userId="me", id=id
        ).execute()
        print("deleting message", id)
    
    def getMessage(self, m):
        id = m.get("id")
        message = self.messages.get(
            userId="me", id=id
        ).execute()
        return parseEmailMessage(message)



    def getThread(self, id):
        if isObject(id): id = id.get('id')
        return self.threads.get(userId="me", id=id).execute()
    
    def getThreads(self, labels=["INBOX"]):
        return (
            self.threads.list(userId="me", labelIds=labels)
            .execute()
            .get("threads", [])
        )

    def getMessages(self, labels=["INBOX"]):
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

    def email(self, message='automated message to self'):
        message = EmailMessage()
        message.set_content(message)
        message["From"] = env.EmailContacts.get('self')
        message["To"] = env.EmailContacts.get('self')
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


def googleDriveDownloadFile(drive, file):
    fileId = file.get("id")
    name = file.get("name")
    mimeType = "application/pdf"
    outpath = npath(dldir, addExtension(name, "pdf"))
    fh = io.FileIO(outpath, "wb")
    done = False
    try:
        if isImage(name):
            request = drive.files.get_media(
                fileId=fileId
            )
        else:
            request = drive.files.export_media(
                fileId=fileId, mimeType=mimeType
            )
        downloader = MediaIoBaseDownload(fh, request)
        while done is False:
            status, done = downloader.next_chunk()
    except Exception as e:
        print("errrror", e, outpath)
        return

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



def getSubmissionTitle(item):
    attachments = item.get("assignmentSubmission").get("attachments")
    if attachments:
        return attachments[0].get("driveFile").get("title")
    return 'no-title'


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

    def move(self, id, folder):
        file = self.get(fileId=id, fields='parents, webViewLink')
        folderId = self.getdir(folder)
        parents = ",".join(file.get("parents"))

        file = self.update(
            fileId=id,
            addParents=folderId,
            removeParents=parents,
            fields="id, parents, webViewLink"
        )
        self.viewParent(file)

    def viewParent(self, file):
        parentObj = self.get(fileId=file.get('parents')[0], fields='webViewLink')
        webbrowser.open(parentObj.get('webViewLink'))

    
    #def pdf(self, id):
        #file = self.get(fileId=id)
    
    def view(self, id):
        raise Exception('doesnt work')

    def update(self, **kwargs):
        return self.drive.files.update(**kwargs).execute()

    def get(self, **kwargs):
        return self.drive.files.get(**kwargs).execute()
    
    def getdir(self, name):
        if name == 'root':
            return self.drive.files.get_root().execute().get('id')
        query = "mimeType='application/vnd.google-apps.folder' and trashed = false and name='%s'" % name 
        response = self.drive.files.list(q=query, fields='files(id)').execute()
        if len(response.get('files', [])) > 0:
            folder_id = response.get('files', [])[0].get('id')
            return folder_id
        if prompt(name + ' was not found ... do you want to make the dir?'):
            self.mkdir(name)
        else:
            raise Exception('not found')
    
    def mkdir(self, name, parentId='root'):
        body = {
            'name': name,
            'parents': [parentId],
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = self.drive.files.create(body=body, fields='id').execute()
        print(f'Folder "{name}" created with ID: "{folder.get("id")}".')
        return folder.get('id')
    
    def move(self, x):
        return map(coerceArray(x), self.move_file_to_new_folder)
    
    def move_file_to_new_folder(self, id, folderId):
       file = self.drive.files.get(fileId=id, fields='parents').execute()
       previous_parents = ",".join(file.get('parents'))
       file = self.drive.files.update(fileId=id,
                           addParents=folderId,
                           removeParents=previous_parents,
                           fields='id, parents'
       ).execute()
       print(f'{id} has been moved to folder {folderId}.')
       return id
 
    
    def app_get_files(self, query, pageSize=None):
        query += " and trashed = false"
        orderBy = 'modifiedTime desc'
        response = self.drive.files.list(q=query, orderBy=orderBy, pageSize=pageSize, fields="files(id, name)").execute().get('files')
        return response
        
    
    def get_all_files(self, pageSize=None, info=None, q=0, fields=0, root=0):
        """
            

        """
        if root:
            q = "mimeType='application/vnd.google-apps.document' and trashed = false and 'root' in parents and not 'appDataFolder' in parents"

        if not fields:
            fields = "id, name, modifiedTime, createdTime, shared, owners"
        fields = f"nextPageToken, files({fields})"
        if not q:
            q = "mimeType='application/vnd.google-apps.document'"
        pageToken = None
        store = []

        while True:
            response = self.drive.files.list(
                q=q,
                pageSize=pageSize,
                pageToken=pageToken,
                fields=fields,
                #fields="nextPageToken, files(id, name, modifiedTime, createdTime, size, fileExtension, mimeType, shared, owners)",
            ).execute()
            files = response.get("files", [])
            print('got files', len(files))
            store.extend(files)
            pageToken = response.get("nextPageToken")

            if not pageToken or pageSize == 1:
                break

        
        if info:
            docs = GoogleDocs()
            def parser(item):
                doc = docs.get(item)
                text = getDocText(doc)
                size = len(text)
                elapsed = get_elapsed_time(item)
                author = doc.get('author')
                name = item.get('name')
                id = item.get('id')
                owner = item.get('owners')[0].get('displayName')
                dt = datetime.fromisoformat(item.get('createdTime').rstrip('Z'))
                deleteIt = size < 100 or size < 1000 and test('untitled', name, flags=re.I) or not test('kevin', owner, flags=re.I)
                if deleteIt:
                    pprint(dict(delete=True, size=size, owner=owner, name=name))
                else:
                    print('saving', name)

                payload = {
                    'id': id,
                    'delete': deleteIt,
                    'owner': owner,
                    'title': name,
                    'size': size,
                    'author': author,
                    'text': text,
                    'elapsed': elapsed,
                    'date': datestamp(dt),
                    'year': dt.year,
                }

                return payload

            store = map(store, parser)

        return store
        print('going')
        print(exists(store))
        clip(store)

    
    def find_cover_letters(self, r = 'cover', pageSize=1):
        query = f"name matches '{r}'"
        return self.app_get_files(query, pageSize=pageSize)
    
    def doJobApplication(self):

        files = self.drive.getLastDocFiles(2)
        #prompt(files)
        resume = 0
        cv = 0
        for file in files:
            fileId = file.get('id')
            name = removeDateString(file.get('name'))

            if test('resume', name, flags=re.I):
                if resume:
                    continue
                else:
                    resume = 1
                    name = 'Kevin Lee Resume'

            elif test('cv|cover letter', name):
                if cv:
                    continue
                else:
                    cv=1
                    name = 'Kevin Lee Cover Letter'

            self.drive._download(fileId, name)
    
    def __init__(self):
        self.drive = GoogleDrive()

    def openDoc(self, name):
        file = self.drive.getFiles2(name=name)
        url = f"https://docs.google.com/document/d/{file.get('id')}"
        ofile(url)

    def downloadDoc(self, name=0, outpath=0):
        self.drive.downloadFile(name, outpath)
    

def individualAssignment(files=0, student='Ella Wu'):
    ref = {
        'Ella Wu': '5',
    }

    files = toArray(files) if files else [glf()]
    classKey = ref.get(student)
    room = GoogleClassroom(classKey)
    for file in files:
        room.uploadAssignment(file, student=student)
    room.openLink()


#GoogleEmail().testing()
def parseEmailMessage(message):
    data = {}
    headers = message["payload"]["headers"]
    for h in headers:
        if h["name"] == "Subject":
            data["subject"] = h["value"]

        elif h["name"] == "Date":
            data["date"] = h["value"]

        elif h["name"] == "From":
            data["sender"] = h["value"]

    data["snippet"] = message["snippet"]
    return data


def gradeClassroom(room, grade=100):
    students = room.getStudents()
    for student in students:
        submissions = (
            room.studentSubmissions.list(
                courseId=room.courseId,
                courseWorkId="-",
                pageSize=10,
                userId=student.get("userId"),
                states="TURNED_IN",
            )
            .execute()
            .get("studentSubmissions")
        )

        if not submissions:
            pprint('no submissions @ student')
            continue

        for submission in submissions:
            gradeSubmission(room, submission, 100)

def gradeSubmission(room, submission, grade=100):

    title = getSubmissionTitle(submission)
    if not submission.get("associatedWithDeveloper"):
        pprint('!associated with developer', title)
        return 

    if test("quiz|exam|test", title, flags=re.I):
        viewSubmission(room, submission)
        grade = prompt('assign a grade for this item')

    try:
        result = room.gradeSubmission(
            submission.get("courseWorkId"),
            submission.get("id"),
            grade,
        )
        print(result, "graded assignment", title)
    except Exception as e:
        prompt(str(e), title, 'ERROR_PROMPT')
    

def viewSubmission(room, submission):
        
    courseWork = room.getCourseWork(submission)
    print("viewing courseWork assignment")
    room.view(courseWork)

    attachments = submission.get(
        "assignmentSubmission"
    ).get("attachments")

    print("viewing student submission pictures")
    room.view(attachments)

def doGrades():
    keys = ['g4', 'g5']
    for key in keys:
        r = GoogleClassroom(key)
        gradeClassroom(r)

#doGrades()
#GoogleApp().doJobApplication()
#pprint(GoogleApp().find_cover_letters('resume'))

def getDocText(document):
    text = ''
    for element in document.get("body").get("content"):
        if 'paragraph' in element:
            for run in element.get("paragraph").get("elements"):
                if 'textRun' in run:
                    s = run.get("textRun").get("content")
                    text += s
    return text





def getId(x):
    return x if isString(x) else x.get('documentId') or x.get('id')

def get_doc_url(x):
    id = getId(x)
    return f"https://docs.google.com/document/d/{id}/edit"


def get_elapsed_time(doc):
    start_time_str = doc.get('createdTime')
    end_time_str = doc.get('modifiedTime')
    start_time = datetime.fromisoformat(start_time_str.rstrip('Z'))
    end_time = datetime.fromisoformat(end_time_str.rstrip('Z'))
    elapsed_time = end_time - start_time
    elapsed_seconds = int(elapsed_time.total_seconds())
    if elapsed_seconds >= 86400 * 30 * 12:
        elapsed_months = elapsed_seconds // 86400 * 30 * 12
        return {"type": "years", "value": elapsed_months}


    if elapsed_seconds >= 86400 * 30:
        elapsed_months = elapsed_seconds // 86400 * 30
        return {"type": "months", "value": elapsed_months}

    if elapsed_seconds >= 86400:
        elapsed_days = elapsed_seconds // 86400
        return {"type": "days", "value": elapsed_days}
    elif elapsed_seconds >= 3600:
        elapsed_hours = elapsed_seconds // 3600
        return {"type": "hours", "value": elapsed_hours}
    else:
        elapsed_minutes = elapsed_seconds // 60
        return {"type": "minutes", "value": elapsed_minutes}


def is_google_id(s):
    r = '[\d-_][a-zA-Z]'
    return isString(s) and len(s) > 20 and len(re.findall(r, s)) >= 4
        


def downloadCoverLettersAndResumesAndMerge():
    raise Exception('todo')
    from pdf import mergepdf
    items = googleDocsJson()
    ids = obj_filter(items, title='cv|\bcover\b|resume', owner='kevin', delete=False, get='id, date, title')
    app = GoogleApp()
    assert(every(ids, is_google_id))
    #prompt(good=ids)
    paths = map(ids, app.drive.downloadFile)
    prompt(pathsToMerge=paths)
    try:
        mergepdf(paths, outpath='Kevin Lee - Resumes & Cover Letters.pdf')
        return 1
    except Exception as e:
        clip(paths)
        return 0
    

#pprint(downloadCoverLettersAndResumesAndMerge())


def send_goc_to_pdf():
    app = GoogleApp()
    obj = app.drive.downloadFile()

    metaData = {
        "name": tail(obj.get('name')),
        "parents": [UPLOAD_DESTINATION],
    }

    media = MediaFileUpload(
        file, mimetype=mimeTypeFromFile(file)
    )

    fileResponse = self.files.create(
        body=metaData, media_body=media, fields="id"
    ).execute()
#-------------------------------------------------

def shouldDeleteEmail(email):
    sender = email.get('sender')
    if test('(?:no|donot)\W*reply', sender, flags=re.I):
        return True
    for email in env.deleteEmails:
        if email in sender:
            return True


class GoogleYoutube:
    def __init__(self, **kwargs):

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        service = getService("youtube")
        self.youtube = service.search()

    def getUserChannel(self, user):
        response = self.youtube.channels().list(
            part='contentDetails',
            forUsername=user
        ).execute()
        pprint(response)
        return response

    def getUserChannelId(self, user):
        response = self.getUserChannel(user)
        return getResponseId(response)

    def getUserPlayList(self, user):
        response = self.youtube.list(
            part='id',
            channelId=self.getUserChannelId(user)
        ).execute()
        id = getResponseId(response)

        videos = []
        next_page_token = None

        while True:
            response = youtube.playlistItems().list(
                part='snippet',
                playlistId=id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()
            videos.extend(response['items'])
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
            print('keep going')
            break

        return videos

def getResponseId(response):
    id = response['items'][0]['id']
    return id

#yt = GoogleYoutube()
#pprint(yt.getUserPlayList('kevinlee8512'))

# client_secrets.json
# g.py-oauth2.json
# credentials.json





class GoogleDocsManager:
    def __init__(self):
        self.service = getService("docs")

    def createParagraphRequest(self, text, index):
        return {
            'insertText': {
                'location': {
                    'index': index,
                },
                'text': text + '\n'
            }
        }

    def createTableRequest(self, rows, start_index, column_widths=None, cell_styles=None):
        requests = [{
            'insertTable': {
                'rows': len(rows),
                'columns': len(rows[0]),
                'location': {'index': start_index}
            }
        }]

        # Moving the index to the first cell after the table is created
        index = start_index + 1

        for row_index, row in enumerate(rows):
            for col_index, cell in enumerate(row):
                cell_insert_index = index + 1  # Adjusting for the newline character at the end of each cell
                requests.append({
                    'insertText': {
                        'location': {'index': cell_insert_index},
                        'text': cell
                    }
                })

                # Updating index for the next cell or row
                index = cell_insert_index + len(cell)

                # Adding cell style if provided
                if cell_styles and cell_styles[row_index][col_index]:
                    requests.append({
                        'updateTextStyle': {
                            'range': {
                                'startIndex': cell_insert_index,
                                'endIndex': cell_insert_index + len(cell)
                            },
                            'textStyle': cell_styles[row_index][col_index],
                            'fields': ','.join(cell_styles[row_index][col_index].keys())
                        }
                    })

                # Adding column width if provided
                if column_widths and column_widths[col_index]:
                    requests.append({
                        'updateTableColumnProperties': {
                            'tableStartLocation': {'index': start_index},
                            'columnIndices': [col_index],
                            'tableColumnProperties': {
                                'width': column_widths[col_index]
                            },
                            'fields': 'width'
                        }
                    })

            # Adjusting index for the end of the row
            index += 2  # Skipping past the end of row character

        return requests, index

    # ... other methods ...

    def xxcreateTableRequest(self, rows, start_index, column_widths=None, cell_styles=None):
        requests = [{
            'insertTable': {
                'rows': len(rows),
                'columns': len(rows[0]),
                'location': {'index': start_index}
            }
        }]
        index = start_index + 1

        for row_index, row in enumerate(rows):
            for col_index, cell in enumerate(row):
                requests.append({
                    'insertText': {
                        'location': {'index': index},
                        'text': cell
                    }
                })
                index += len(cell) + 1

                if cell_styles and cell_styles[row_index][col_index]:
                    requests.append({
                        'updateTextStyle': {
                            'range': {
                                'startIndex': index - len(cell) - 1,
                                'endIndex': index - 1
                            },
                            'textStyle': cell_styles[row_index][col_index],
                            'fields': ','.join(cell_styles[row_index][col_index].keys())
                        }
                    })

                if column_widths and column_widths[col_index]:
                    requests.append({
                        'updateTableColumnProperties': {
                            'tableStartLocation': {'index': start_index},
                            'columnIndices': [col_index],
                            'tableColumnProperties': {
                                'width': column_widths[col_index]
                            },
                            'fields': 'width'
                        }
                    })
            index += 1  # Skip over the end of the row
        return requests, index

    def insertImageRequest(self, image_url, index=1):
        return {
            'insertInlineImage': {
                'location': {
                    'index': index
                },
                'uri': image_url,
                'objectSize': {
                    'height': {'magnitude': 50, 'unit': 'PT'},
                    'width': {'magnitude': 50, 'unit': 'PT'}
                }
            }
        }

    def createDocumentFromJson(self, json_data, title='Untitled'):
        document = self.service.documents().create(body={'title': title}).execute()
        doc_id = document['documentId']

        requests = []
        index = 1
        for item in json_data['content']:
            if item['type'] == 'paragraph':
                requests.append(self.createParagraphRequest(item['text'], index))
                index += len(item['text']) + 1
            elif item['type'] == 'table':
                table_requests, table_end_index = self.createTableRequest(item['rows'], index, item.get('column_widths'), item.get('cell_styles'))
                requests.extend(table_requests)
                index = table_end_index
            elif item['type'] == 'image':
                requests.append(self.insertImageRequest(item['url'], index))
                index += 2  # Update index as needed for the inserted image

        self.service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
        doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
        return doc_url

json_data = {
    "content": [
        {"type": "paragraph", "text": "Hello, this is a sample paragraph."},
        {"type": "paragraph", "text": "Hello, this is a sample paragraph."},
        {"type": "paragraph", "text": "Hello, this is a sample paragraph."},
        {"type": "image", "url": "https://picsum.photos/id/237/200/300"},
        {"type": "image", "url": "https://picsum.photos/id/237/200/200"},
        {"type": "image", "url": "https://picsum.photos/id/237/400/400"},
        # {
            # "type": "table",
            # "rows": [["Cell 1", "Cell 2"], ["Cell 3", "Cell 4"]],
            # "column_widths": [None, {'magnitude': 100, 'unit': 'PT'}],
            # "cell_styles": [[{'bold': True}, None], [None, {'backgroundColor': {'color': {'rgbColor': {'red': 0.8, 'green': 0.8, 'blue': 0.8}}}}]]
        # }
    ]
}

def abc():
    manager = GoogleDocsManager()
    doc_url = manager.createDocumentFromJson(json_data, title="Document with Images and Tables")
    print("Document created:", doc_url)
    ofile(doc_url)



def get_drive_file(service, x):
    if has(x, "id"):
        return x
        return x
    if x.replace('-', '').isalnum() and len(x) > 15:
        return service.files().get(fileId=x).execute()

    results = service.files().list(q=f"name = '{x}'", fields="files(id, name)").execute()
    files = results.get('files', [])
    return files

# docs = GoogleDocs()
# append_self()

def parse_date_string(date_str):
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

def create_query(after = 0, type = 0, before = 0, name = 0, size = 0, ascending = 0, descending = 0):

    fields = [ "id", "name" ]
    reqs = []
    reqs.append("trashed = false")

    if type == "document":
        reqs.append("mimeType='application/vnd.google-apps.document'")
    elif type == "spreadsheet":
        reqs.append("mimeType='application/vnd.google-apps.sheet'")

    if name:
        reqs.append(f"name contains '{name}'")
    if after or before:
        date = parse_date_string(after or before)
        sign = ">" if after else "<"
        d = datetime.utcnow() - timedelta(**date)
        s = d.isoformat() + 'Z'
        reqs.append(f"modifiedTime {sign} '{s}'")


    query = " and ".join(reqs)
    fieldString = ','.join(fields)
    if size != 1:
        fields = f"files({fieldString})"
    else:
        # fields = fieldString
        fields = f"files({fieldString})"
    payload =  { "q": query, "fields": fields }

    if ascending:
        payload["orderBy"] = 'modifiedTime desc'
    elif descending:
        payload["orderBy"] = 'modifiedTime desc'
    if size:
        payload["pageSize"] = size

    # prompt("opts", payload)
    return payload


def abc():
    drive = GoogleDrive()
    files = drive.getDocsFromLastWeek()
    id = files[0].get("id")

    file = drive.getDriveFile(name = "doctes")
    id2 = file.get("id")
    assert id == id2

    docs = GoogleDocs()
    json = docs.getDocContentAsJson(id)
    clip(json)

def abc():
    drive = GoogleDrive()
    file = drive.getDriveFile(name = "doctes")
    docs = GoogleDocs()
    json = docs.getDocContentAsJson(file)
    clip(json)


def abc():
    docs = GoogleDocs()
    document = docs.create("dialogue_template")

def create_formatted_table(document_id, service):
    requests = [
        {
            'insertTable': {
                'rows': 2,
                'columns': 2,
                'location': {'index': 1}
            }
        },
        # Set the text in the first column to be bold
        {
            'updateTextStyle': {
                'textStyle': {'bold': True},
                'range': {
                    'startIndex': 1,
                    'endIndex': 4  # Adjust this range based on your actual table content
                },
                'fields': 'bold'
            }
        },
        # Set column widths
        {
            'updateTableColumnProperties': {
                'tableColumnProperties': {
                    'width': {
                        'magnitude': 72,  # 1 inch in points
                        'unit': 'PT'
                    }
                },
                'columnIndices': [0],  # First column
                'tableStartLocation': {'index': 1},
                'fields': 'width'
            }
        },
        {
            'updateTableColumnProperties': {
                'tableColumnProperties': {
                    'width': {
                        'magnitude': 72 * ,  # 2 inches in points
                        'unit': 'PT'
                    }
                },
                'columnIndices': [1],  # Second column
                'tableStartLocation': {'index': 1},
                'fields': 'width'
            }
        }
    ]

    service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()

