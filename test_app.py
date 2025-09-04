import pytest
from unittest.mock import patch, MagicMock
from app import app, User


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.app_context():
        with app.test_client() as client:
            yield client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Aplicação Flask conectada ao Postgres!" in response.get_data(as_text=True)


@patch("app.db.session")
def test_create_user(mock_session, client):
    mock_user = User(id=1, name="João")

    # Mocka add e commit para não acessar o banco real
    mock_session.add = MagicMock()
    mock_session.commit = MagicMock()

    response = client.post("/create_user", json={"name": "João"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "João"
    assert "id" in data


def test_create_user_without_name(client):
    response = client.post("/create_user", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


@patch("app.User.query")
def test_list_users(mock_query, client):
    # Mocka o retorno da query
    mock_query.all.return_value = [User(id=1, name="Maria")]

    with app.app_context():
        response = client.get("/list_users")
        assert response.status_code == 200
        users = response.get_json()
        assert len(users) == 1
        assert users[0]["name"] == "Maria"
