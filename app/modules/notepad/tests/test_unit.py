import pytest

from app import db
from app.modules.auth.models import User
from app.modules.conftest import login, logout
from app.modules.profile.models import UserProfile
from app.modules.notepad.models import Notepad


@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        user_test = User(email="user@example.com", password="test1234")
        db.session.add(user_test)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Name", surname="Surname")
        db.session.add(profile)
        db.session.commit()

    yield test_client


def test_sample_assertion(test_client):
    """
    Sample test to verify that the test framework and environment are working correctly.
    It does not communicate with the Flask application; it only performs a simple assertion to
    confirm that the tests in this module can be executed.
    """
    greeting = "Hello, World!"
    assert greeting == "Hello, World!", "The greeting does not coincide with 'Hello, World!'"


def test_list_empty_notepad_get(test_client):
    """
    Tests access to the empty notepad list via GET request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get("/notepad")
    assert response.status_code == 200, "The notepad page could not be accessed."
    assert b"You have no notepads." in response.data, "The expected content is not present on the page"

    logout(test_client)
   
    
def test_create_notepad_page_get(test_client):
    """
    Tests access to the notepad creation page via GET request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get("/notepad/create")
    assert response.status_code == 200, "The notepad creation page could not be accessed."
    assert b"Title" in response.data, "The expected content is not present on the page"
    assert b"Body" in response.data, "The expected content is not present on the page"
    assert b"Save notepad" in response.data, "The expected content is not present on the page"

    logout(test_client)
    
    
@pytest.fixture
def notepad_for_viewing(test_client):
    """
    Fixture para crear un notepad de prueba.
    """
    # No necesitamos crear un nuevo contexto, ya existe uno del fixture test_client
    # Obtener el usuario que se creó en el fixture test_client
    user = User.query.filter_by(email="user@example.com").first()
    
    notepad = Notepad(
        title="Sample Notepad", 
        body="This is a sample notepad body.", 
        user_id=user.id
    )
    db.session.add(notepad)
    db.session.commit()
    
    yield notepad

    # Cleanup
    db.session.delete(notepad)
    db.session.commit()


def test_view_notepad_page_get(test_client, notepad_for_viewing):
    """
    Tests access to the notepad viewing page via GET request.
    """
        
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get(f"/notepad/{notepad_for_viewing.id}")
    assert response.status_code == 200, "The notepad viewing page could not be accessed."
    
    logout(test_client)
    