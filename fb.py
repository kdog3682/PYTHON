from base import *
from next import *
from firebase_admin import (
    firestore,
    credentials,
    initialize_app,
)


def getDatabase():
    cred = credentials.Certificate(env.firebaseconfigjson)
    initialize_app(cred)
    db = firestore.client()
    return db


class FireStore:
    def __init__(self):
        self.doc = None
        self.collection = None

        if empty(self, "collectionName"):
            self.collectionName = None

        if empty(self, "docId"):
            self.docId = None

        self.db = getDatabase()
        self.run()

    def get_collection(self, name=None):
        if not name and self.collection:
            return self.collection
        return self.db.collection(name)

    def get_doc(self, docId=None):
        if not docId and self.doc:
            return self.doc
        return self.collection.document(docId)

    def set_collection(self, collectionName=None):
        if not collectionName:
            collectionName = self.collectionName

        if not collectionName:
            return

        self.collection = self.get_collection(
            collectionName
        )

    def set_doc(self, docId=None):
        if not docId:
            docId = self.docId

        if not docId:
            return
        self.doc = self.get_doc(docId)

    @property
    def docs(self):
        docs = self.collection.get()
        return docs

    @property
    def ids(self):
        return [d.id for d in self.docs]

    def __json__(self):
        return [
            {"id": d.id, **d.to_dict()} for d in self.docs
        ]

    def create_collection(self, collection):
        return self.db.collection(collection)

    def delete_collection(self, name=None):
        collection = self.get_collection(name)
        for doc in collection.stream():
            doc.reference.delete()

        collection.delete()
        self.collection = None

    @ensure_object
    def create_doc(self, payload):
        return self.collection.add(payload)

    @ensure_object
    def update_doc(self, payload, key=None):
        return self.get_doc(key).update(payload)

    def delete_doc(self, key=None):
        if isNumber(key):
            key = self.ids[key]

        return self.get_doc(key).delete()

    def run(self, actions=0, collection=None):

        actions = actions or getattr(self, "actions", [])
        if not actions:
            print("no actions, early return")
            return

        self.set_collection()
        for action in to_array(actions):
            name = action.get("name")
            args = to_array(action.get("args", []))
            value = getattr(self, name)(*args)
            if value:
                dprint(name, args, value)
                #dprompt(name, args, value, "got a value")

    def addAll(self, items):
        for item in items:
            self.add(item)

    def deleteAll(self):
        for id in self.ids:
            self.delete(id)

    # alias
    def add(self, *args, **kwargs):
        return self.create_doc(*args, **kwargs)

    # alias
    def delete(self, *args, **kwargs):
        return self.delete_doc(*args, **kwargs)

    # alias
    def update(self, *args, **kwargs):
        return self.update_doc(*args, **kwargs)

    # alias
    def json(self, *args, **kwargs):
        return self.__json__(*args, **kwargs)

    # ####### ########## ########## ########## ##########
    # magical ########## ########## ########## ##########
    # ####### ########## ########## ########## ##########
    # ####### ########## ########## ########## ##########

    def delete_everything(self, fn=0):

        def wrapper(db):
            for collection in db.collections():
                runner(collection)


        def runner(collection):
            for doc in collection.stream():
                wrapper(doc.reference)
                print('deleting doc', doc.id)
                doc.reference.delete()
            print('deleting collection', collection.id)
            #collection.delete()

        return wrapper(self.db)

    def recursive(self, data):
        db = self.db

        def runner(data, parent):
            for item in data:

                t = item.get("type")
                value = item.get("value")
                name = item.get("name")
                merge = item.get("merge")

                action = item.get("action")
                args = item.get("args")

                if t == "collection":
                    collection = parent.collection(name)
                    for item in value:
                        runner(item, collection)

                elif t == "document":
                    doc = parent.document(name)
                    if isArray(value):
                        for item in value:
                            runner(item, doc)
                    else:
                        doc.set(value)

                elif t == "data":
                    parent.set(data, merge=merge)

                elif t == "action":
                    getattr(parent, action)(*args)

                else:
                    ndy()

        with db.batch() as batch:
            runner(data, batch)

    def get_all_docs_v2(self):

        def root_wrapper(db):
            collections = db.collections()
            out = {}
            for collection in collections:
                id, docs = runner(collection)
                out[id] = docs
            return out

        def doc_wrapper(doc):
            id = doc.id
            data = doc.to_dict()

            for subcollection in doc.reference.collections():
                subId, subData = runner(subcollection)
                data[subId] = subData

            return id, data
        
        def runner(collection):
            id = collection.id
            out = {}

            for doc in collection.stream():
                docId, docData = doc_wrapper(doc)
                out[docId] = docData

            return id, out

        return root_wrapper(self.db)


    def get_all_docs(self):

        def runner(collection):
            store = {
                'id': collection.id,
                'type': 'collection',
                'docs': []
            }
            docs = collection.stream()
            for doc in docs:
                data = {'id': doc.id, 'type': 'document', 'data': doc.to_dict()}
                subcols = []
                subcollections = doc.reference.collections()
                for subcollection in subcollections:
                    subcols.append(runner(subcollection))

                if subcols:
                    data['sub_collections'] = subcols
                store['docs'].append(data)

            return store

        db = self.db
        collections = db.collections()
        data = map(collections, runner)
        return data


    def recursive_upload(self, data):
        def isRoot(parent):
            name = t2s(parent)
            return name == "Client" or name == "WriteBatch"

        def isFlat(data):
            for k, v in data.items():
                if isObject(v) or isObjectArray(v):
                    return False

            return True

        def isDoc(parent):
            name = t2s(parent)
            return name == "DocumentReference"

        def isCollection(parent):
            name = t2s(parent)
            return name == "CollectionReference"

        def runner(data, parent):
            docParent = None

            for k, v in data.items():
                if isObject(v):
                    if isRoot(parent):
                        collection = parent.collection(k)
                        runner(v, collection)

                    elif isDoc(parent):
                        if isFlat(v):
                            parent.set({k: v}, merge=True)
                        else:
                            collection = parent.collection(
                                k
                            )
                            runner(v, collection)
                    elif isCollection(parent):
                        doc = parent.document(k)
                        runner(v, doc)
                    else:
                        print("this will never be touched")
                        ndy()

                elif isObjectArray(v):
                    collection = parent.collection(k)
                    for item in v:
                        runner(item, collection)
                else:

                    if isDoc(parent):
                        parent.set({k: v}, merge=True)

                    else:
                        if (
                            isCollection(parent)
                            and not docParent
                        ):
                            docParent = parent.document()

                        docParent.set({k: v}, merge=True)

        # db = self.db
        # with self.db.batch() as batch:
        # runner(self.db, batch)
        runner(data, self.db)


recursiveData2 = data = {
    "books": {
        "userId2": {
            "name": "John Doe",
            "age": 30,
            "posts": [
                {
                    "title": "My First Post",
                    "content": "Lorem ipsum dolor sit amet",
                },
            ],
        }
    }
}
recursiveData = data = {
    "books": {
        "userId1": {
            "name": "John Doe",
            "age": 30,
            "posts": [
                {
                    "title": "My First Post",
                    "content": "Lorem ipsum dolor sit amet",
                },
                {
                    "title": "My Second Post",
                    "content": "Consectetur adipiscing elit",
                },
            ],
            "comments": [
                {
                    "post": "postId1",
                    "text": "Great post, John!",
                },
                {
                    "post": "postId2",
                    "text": "I really enjoyed this one too",
                },
            ],
        },
        "userId2": {
            "name": "Jane Smith",
            "age": 25,
            "posts": [
                {
                    "title": "My First Post From Jane",
                    "content": "Lorem ipsum dolor sit amet",
                }
            ],
            "comments": [
                {
                    "post": "postId1",
                    "text": "Thanks for sharing, Jane!",
                }
            ],
        },
    }
}


recursiveData = {
    "javascript": {
        'js1': {
            'value': 'bogzor()'
        }
    }
}

userAccounts = {
  "users": {
    "kevinlee": {
      "name": "Kevin",
      "password": "1234",
      "role": "teacher",
      "email": "kevin@hammymath.com",
    },
    "hammy": {
      "name": "hammy",
      "role": "hammy",
      "age": 10,
      "email": "hammy@hammymath.com"
    },
    "bobj": {
      "name": "Bob Johnson",
      "age": 40,
      "email": "bobjohnson@example.com"
    }
  }
}

assignments = {
  "assignments": [
    {
      "title": "Algebraic Expressions",
      "description": "Simplify and evaluate algebraic expressions",
      "dueDate": "2023-05-01T23:59:59Z",
      "points": 20,
      "questions": [
        {
          "text": "Simplify: 3x + 5 - 2x + 7",
          "answer": "x + 12"
        },
        {
          "text": "Evaluate: 2x^2 - 3x + 1, when x = 4",
          "answer": "21"
        },
        {
          "text": "Simplify: (x + 2)(x - 3) + (x + 2)(4 - x)",
          "answer": "-2x - 10"
        }
      ]
    },
    {
      "title": "Functions and Graphs",
      "description": "Graph and analyze functions",
      "dueDate": "2023-05-08T23:59:59Z",
      "points": 30,
      "questions": [
        {
          "text": "Graph the function y = 2x + 1",
          "answer": "(insert graph image here)"
        },
        {
          "text": "Find the domain and range of the function f(x) = x^2 - 4",
          "answer": "Domain: all real numbers; Range: y ≤ -4 or y ≥ 0"
        },
        {
          "text": "Find the x-intercept(s) of the function y = x^3 - 3x^2 - 9x",
          "answer": "x = -3, 0"
        }
      ]
    },
    {
      "title": "Trigonometry",
      "description": "Solve problems using trigonometric functions",
      "dueDate": "2023-05-15T23:59:59Z",
      "points": 40,
      "questions": [
        {
          "text": "Find the value of sin 60°",
          "answer": "0.866"
        },
        {
          "text": "Find the length of the side opposite the angle θ in the right triangle below: (insert image of right triangle)",
          "answer": "8"
        },
        {
          "text": "Solve for x: tan x = 1",
          "answer": "x = π/4 or 45°"
        }
      ]
    }
  ]
}

def get_hammy_data():
    data = assignments
    prompt(data=data, message='Proceed to HammyMathClass data upload?')
    return data

class HammyMathClass(FireStore):
    actions = [
        {"name": "recursive_upload", "args": [get_hammy_data()]},
        {"name": "get_all_docs_v2"}, 
    ]
        
HammyMathClass()
