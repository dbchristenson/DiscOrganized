# General
import os

# Library
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore_async

load_dotenv()
cred_path = os.getenv('FIREBASE_CRED_PATH')

if cred_path and os.path.exists(cred_path):
    # Use credentials from the file
    cred = credentials.Certificate(cred_path)
    app = firebase_admin.initialize_app(cred)
else:
    # Proceed with the default initialization (e.g. on GCS)
    app = firebase_admin.initialize_app()

# Shared instances of the Firebase app and Firestore client
db = firestore_async.client(app=app)


class FirestoreCRUD:
    '''
    A class to handle CRUD operations on a specified Firestore collection
    and document. It uses shared instances of the Firebase app and Firestore
    client for efficient resource usage, while allowing optional overrides
    for flexibility in testing or other specific scenarios.
    '''
    def __init__(self, collection: str, document: str = None, app=app, db=db):
        '''
        :param collection: The collection to point to
        :param document: The document to point to
        :param app: The app to use
        :param db: The database to use
        '''
        self.app = app
        self.db = db

        self.collection = collection
        self.document = document

        try:
            self.ref = db.collection(collection).document(document)
        except ValueError:
            self.ref = None

    async def set_document(self, document: str):
        '''Changes the document to point to'''
        self.document = document
        self.ref = db.collection(self.collection).document(document)

    def check_ref(self):
        '''Checks if the reference is valid'''
        if not self.ref:
            return False
        else:
            return True

    async def create(self, data: dict):
        '''Creates a new document in the collection'''
        assert self.check_ref()

        await self.ref.set(data)

    async def read(self):
        '''Reads the document from the collection'''
        assert self.check_ref()

        query = await self.ref.get()
        return query.to_dict()

    async def update(self, data: dict):
        '''Updates the document with the given data'''
        assert self.check_ref()

        await self.ref.update(data)

    async def delete(self):
        '''Deletes the document from the collection'''
        assert self.check_ref()

        await self.ref.delete()

        # Set the reference to None
        self.ref = None
