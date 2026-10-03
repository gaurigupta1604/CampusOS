def test_login_returns_token_pair(client):
    response=client.post("/api/v1/auth/login",json={"email":"student@test.edu","password":"Student123!"})
    assert response.status_code==200
    assert response.json()["access_token"] and response.json()["refresh_token"]
def test_invalid_password_is_rejected(client):
    assert client.post("/api/v1/auth/login",json={"email":"student@test.edu","password":"WrongPass!"}).status_code==401
