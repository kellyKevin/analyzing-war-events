import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"WAR EVENTS INTELLIGENCE" in response.data

def test_map_route(client):
    response = client.get('/map')
    assert response.status_code == 200
    assert response.mimetype == 'text/html'
    assert b"leaflet" in response.data.lower()

def test_ask_ai_route(client):
    response = client.post('/api/ask', json={'question': 'Who is the leader of Ukraine?'})
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'response' in json_data
    assert 'Zelenskyy' in json_data['response'] or 'Ukraine' in json_data['response']
