from app import app


def test_index_route() -> None:
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["service"] == "transparent-api-service"
