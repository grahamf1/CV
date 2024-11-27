import pytest
from flask import Flask
from cv.my_cv import bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_empty_name_submission(client):
    response = client.post('/', data={'name': '', 'email': 'test@example.com', 'comment': 'Test comment'})
    assert b'Name is required.' in response.data
    assert response.status_code == 200