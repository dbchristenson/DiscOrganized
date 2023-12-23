# Library
import firebase_admin
from firebase_admin import firestore
import pytest

# Internal
from src.database.database import FirestoreCRUD


class TestConnection:
    '''Tests the connection to the Firestore database'''
    def test_noapp(self):
        '''Tests the connection without a properly authenticated app.'''
        app = firebase_admin.initialize_app(name='test_noapp', credential=None)

        with pytest.raises(BaseException):
            firestore.client(app=app)

    def test_connection(self):
        '''Tests the connection with a properly authenticated app.'''
        crud = FirestoreCRUD('test', 'connection')

        assert crud.db is not None
        assert crud.app is not None


class TestCRUD:
    @pytest.mark.asyncio
    async def test_set(self):
        '''Tests the creation of a new document in the test collection.'''
        crud = FirestoreCRUD('test', 'set')
        data = {'test': 'set'}

        await crud.create(data=data)
        read_data = await crud.read()

        assert read_data == data

    @pytest.mark.asyncio
    async def test_update(self):
        '''Tests updating the data in the test collection.'''
        crud = FirestoreCRUD('test', 'set')  # Same collection and document
        new_data = {'test': 'update'}

        await crud.update(data=new_data)
        read_data = await crud.read()

        assert read_data == new_data

    @pytest.mark.asyncio
    async def test_delete(self):
        '''Tests deleting the data in the test collection.'''
        crud = FirestoreCRUD('test', 'set')
        await crud.delete()

        read_data = await crud.read()
        assert read_data is None

    @pytest.mark.asyncio
    async def test_ref_assertion(self):
        '''Tests the assertion that a valid reference to a document exists.'''
        crud = FirestoreCRUD('test')

        with pytest.raises(AssertionError):
            await crud.create(data={'test': 'ref_assertion'})
