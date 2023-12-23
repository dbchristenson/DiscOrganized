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


@pytest.mark.asyncio
class TestCRUD:
    async def test_set(self):
        crud = FirestoreCRUD('test', 'set')
        data = {'test': 'set'}

        await crud.create(data=data)
        read_data = await crud.read()

        assert read_data == data

    async def test_update(self):
        '''Updates the data in the test collection.'''
        crud = FirestoreCRUD('test', 'set')  # Same collection and document
        new_data = {'test': 'update'}

        await crud.update(data=new_data)
        read_data = await crud.read()

        assert read_data == new_data

    async def test_delete(self):
        '''Deletes the data in the test collection.'''
        crud = FirestoreCRUD('test', 'set')
        await crud.delete()

        read_data = await crud.read()
        assert read_data is None
