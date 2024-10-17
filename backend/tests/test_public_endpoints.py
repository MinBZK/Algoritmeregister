from fastapi.testclient import TestClient
from app.main import app


class TestPublicEndpoints:
    def setup_class(self):
        self.client = TestClient(app)

    def test_get_all_algorithms(self):
        body = {"filters": [], "page": 1, "limit": 10, "search": ""}
        endpoint = "api/algoritme/NLD"
        response = self.client.post(endpoint, json=body)
        assert response.status_code == 200
        assert response.json()["results"] == []

        body = {"filters": [], "page": 1, "limit": 10, "search": "parkeer"}
        response = self.client.post(endpoint, json=body)
        assert response.status_code == 200
        assert response.json()["results"] == []

        body = {
            "filters": [{"attribute": "organization", "value": "Sandbox"}],
            "page": 1,
            "limit": 10,
            "search": "",
        }
        response = self.client.post(endpoint, json=body)
        assert response.status_code == 200
        assert response.json()["results"] == []

    def test_get_one_algorithm(self):
        response = self.client.get("api/algoritme/NLD/00000001")
        assert response.status_code == 404

        # Verify concept version
        response = self.client.get("api/algoritme/NLD/C00000001")
        assert response.status_code == 404

    def test_get_file_download(self):
        response = self.client.get("api/downloads/NLD?filetype=excel")
        assert response.status_code == 404

    def test_get_json_download(self):
        response = self.client.get("api/json/algoritme")
        assert response.status_code == 404

    def test_get_columns(self):
        response = self.client.get("api/columns")
        assert response.status_code == 200

    def test_get_total_count(self):
        response = self.client.get("api/algoritme/total-count")
        assert response.status_code == 200

    def test_get_count_per_type(self):
        response = self.client.get("api/db-count/name")
        assert response.status_code == 200

    def test_get_count_with_filled_columns(self):
        response = self.client.get("api/completeness?columns=*")
        assert response.status_code == 200

        response = self.client.get("api/completeness?columns=name")
        assert response.status_code == 200

        response = self.client.get(
            "api/completeness/?columns=name&columns=organization"
        )
        assert response.status_code == 200

    def test_get_search_suggestion(self):
        response = self.client.get("api/suggestion/NLD/test")
        assert response.status_code == 200
        assert response.json()["algorithms"] == []
