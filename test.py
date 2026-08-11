import requests


BASE_URL = "http://localhost:8000"


def test_root():

    response = requests.get(
        f"{BASE_URL}/"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "LLM API opérationnelle"

    print("✅ / fonctionne")


def test_health():

    response = requests.get(
        f"{BASE_URL}/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"

    print("✅ /health fonctionne")


def get_token():

    response = requests.post(
        f"{BASE_URL}/login",
        data={
            "username": "henock",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data

    print("✅ /login fonctionne")

    return data["access_token"]


def test_protected():

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"{BASE_URL}/protected",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["authenticated"] is True

    print("✅ /protected fonctionne")


def test_generate():

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(
        f"{BASE_URL}/generate",
        headers=headers,
        json={
            "prompt": "Explique ce qu'est une API en deux phrases."
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["prompt"] == "Explique ce qu'est une API en deux phrases."
    assert "response" in data
    assert len(data["response"]) > 0

    print("✅ /generate fonctionne")
    print("🤖 Réponse :", data["response"])


if __name__ == "__main__":

    test_root()
    test_health()
    test_protected()
    test_generate()

    print("\n🎉 Tous les tests sont passés avec succès !")