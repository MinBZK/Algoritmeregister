from fastapi.testclient import TestClient
import requests
from app.middleware.middleware import get_db
from app import models
from app.main import app


def login(username: str, password: str) -> str:
    LOGIN_URL = "<LOGIN_URL>"
    REALM = "algreg_dev"
    CLIENT = "authentication-client"

    user_info = {
        "client_id": CLIENT,
        "username": username,
        "password": password,
        "grant_type": "password",
        "totp": "",
    }
    response = requests.post(
        LOGIN_URL + "realms/" + REALM + "/protocol/openid-connect/token",
        data=user_info,
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        return token
    else:
        return ""


class TestEndpoints:
    def setup_class(self):
        self.VERSIONS = ["v0_1", "v0_4"]
        self.client = TestClient(app)
        self.db = next(get_db())
        self.token = "Bearer " + login(username="sandbox", password="sandbox")

        org = models.Organisation(**{"name": "sandbox", "code": "sandbox", "org_id": "sandbox"})
        self.db.add(org)
        self.db.commit()
        body = {
            "name": "test",
            "organization": "test",
            "standard_version": "0.1",
        }
        response = self.client.post(
            "aanleverapi/v0_1/organizations/sandbox/algorithms",
            json=body,
            headers={"Authorization": self.token},
        )
        self.lars_code = response.json()["lars_code"]

    def teardown_class(self):
        self.db.query(models.Organisation).delete()
        self.db.commit()
        self.db.close()

    def test_openapi(self):
        for v in self.VERSIONS:
            response = self.client.get(f"aanleverapi/{v}/openapi.json")
            assert response.status_code == 200

    def test_get_all_algorithms(self):
        for v in self.VERSIONS:
            response = self.client.get(
                f"aanleverapi/{v}/organizations/sandbox/algorithms",
                headers={"Authorization": self.token},
            )
            assert response.status_code == 200

    def test_post_one_algorithm(self):
        json = {"name": "test", "organization": "Sandbox"}
        for v in self.VERSIONS:
            json_with_version = {"standard_version": v.replace("_", ".")[1:], **json}
            response = self.client.post(
                f"aanleverapi/{v}/organizations/sandbox/algorithms",
                json=json_with_version,
                headers={"Authorization": self.token},
            )
            assert response.status_code == 200

            response = self.client.post(
                f"aanleverapi/{v}/organizations/sandbox/algorithms",
                headers={"Authorization": self.token},
                json=json,
            )
            lars_code = response.json()["lars_code"]
            assert len(lars_code) == 8
            assert response.status_code == 200

            # Test remove
            response = self.client.delete(
                f"aanleverapi/{v}/organizations/sandbox/algorithms/{lars_code}/remove",
                headers={"Authorization": self.token},
            )
            assert response.status_code == 200

    def test_get_one_algorithm(self):
        for v in self.VERSIONS:
            response = self.client.get(
                f"aanleverapi/{v}/organizations/sandbox/algorithms/{self.lars_code}",
                headers={"Authorization": self.token},
            )
            assert response.status_code == 200

    def test_update_one_algorithm(self):
        json = {"name": "test_put", "organization": "Sandbox"}
        for v in self.VERSIONS:
            json_with_version = {"standard_version": v.replace("_", ".")[1:], **json}
            response = self.client.put(
                f"aanleverapi/{v}/organizations/sandbox/algorithms/{self.lars_code}",
                json=json_with_version,
                headers={"Authorization": self.token},
            )
            assert response.status_code == 200

            response = self.client.put(
                f"aanleverapi/{v}/organizations/sandbox/algorithms/{self.lars_code}",
                json=json,
                headers={"Authorization": self.token},
            )
            assert response.status_code == 200

    def test_get_one_preview_url(self):
        for v in self.VERSIONS:
            response = self.client.get(
                f"aanleverapi/{v}/organizations/sandbox/algorithms/{self.lars_code}/preview",
                headers={"Authorization": self.token},
            )
            assert response.status_code == 200

    def test_publish_flow(self, mocker):
        mock_smtp = mocker.MagicMock(name="app.mailing.mailing.smtplib.SMTP")
        mocker.patch("app.mailing.mailing.smtplib.SMTP", new=mock_smtp)
        for v in self.VERSIONS:
            response = self.client.put(
                f"aanleverapi/{v}/organizations/sandbox/algorithms/{self.lars_code}/release",
                headers={"Authorization": self.token},
            )
            assert response.status_code == 200

            response = self.client.put(
                f"aanleverapi/{v}/organizations/sandbox/algorithms/{self.lars_code}/publish",
                headers={"Authorization": self.token},
            )
            assert response.status_code == 200

            response = self.client.get(
                f"aanleverapi/{v}/organizations/sandbox/published-algorithms/{self.lars_code}",
                headers={"Authorization": self.token},
            )
            assert response.status_code == 200

            response = self.client.delete(
                f"aanleverapi/{v}/organizations/sandbox/published-algorithms/{self.lars_code}/retract",
                headers={"Authorization": self.token},
            )
            assert response.status_code == 200
