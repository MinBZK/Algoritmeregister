import pytest
from fastapi import HTTPException
from app.middleware.authorisation.schemas import Role
from app.middleware.middleware import get_db
from app.schemas.misc import OrgType, PreComputedValues
from app.util.logger import get_logger
from app import controllers, schemas, models
from app.services.keycloak import KeycloakUser
from app.schemas.misc import Language
import json

"""Test all controllers"""

logger = get_logger(__name__)


class TestControllers:
    def setup_class(self):
        self.user_sandbox = KeycloakUser(
            username="test",
            groups=["sandbox"],
            roles=[Role.Administrator],
            id="0",
            first_name="",
            last_name="",
        )
        self.user_no_org = KeycloakUser(
            username="test",
            groups=[],
            roles=[Role.Administrator],
            id="1",
            first_name="",
            last_name="",
        )
        self.db = next(get_db())

        self.db.query(models.Organisation).delete()
        self.db.query(models.PrecomputedValues).delete()
        self.db.commit()

        # Store default body
        filename = "tests/files/algorithm_1_v1_0.json"
        with open(filename, "r") as file:
            data = json.load(file)
        self.body = schemas.AlgoritmeVersionContent(**data)

        sandbox_org = models.Organisation(
            code="sandbox", org_id="sandbox", type=OrgType.gemeente
        )
        self.db.add(sandbox_org)
        self.db.commit()
        # Post one algorithm to share among tests
        post_response = controllers.post_one(
            "sandbox", self.body, self.db, self.user_sandbox
        )
        self.lars_code = post_response.lars_code

    def teardown_class(self):
        self.db.query(models.Organisation).delete()
        self.db.query(models.PrecomputedValues).delete()
        self.db.commit()
        self.db.close()

    def test_base(self):
        get_all_data = controllers.get_algorithm_summary("sandbox", self.db)
        assert len(get_all_data) == 1

    def test_update_new_version(self):
        filename = "tests/files/algorithm_2_v1_0.json"
        with open(filename, "r") as file:
            data = json.load(file)
        body = schemas.AlgoritmeVersionContent(**dict(data))

        # Update
        put_response = controllers.update_new_version(
            body, self.lars_code, self.db, self.user_sandbox
        )
        assert put_response is None

        # Update without change in data
        put_response = controllers.update_new_version(
            body, self.lars_code, self.db, self.user_sandbox
        )
        assert hasattr(put_response, "message")

        # Update non-existing version
        with pytest.raises(HTTPException):
            controllers.update_new_version(body, "00000001", self.db, self.user_sandbox)

        # Verify put
        get_response = controllers.get_one_newest(self.lars_code, self.db)
        assert getattr(get_response, "goal") == "test_new_goal"

    def test_preview_link(self):
        preview_response = controllers.get_preview_link(
            self.lars_code, self.db, self.user_sandbox
        )
        assert hasattr(preview_response, "url")

        # Verify background task
        controllers.wait_then_disable_preview(self.lars_code, self.db)
        controllers.disable_preview(
            self.lars_code,
            self.db,
            "",
            reason=schemas.OperationEnum.preview_activated,
        )

        # Verify can't disable if not active
        controllers.disable_preview(
            self.lars_code,
            self.db,
            "",
            reason=schemas.OperationEnum.preview_activated,
        )

    def test_preview_link_wrong_lars(self):
        # Verify wrong lars code gives error
        with pytest.raises(HTTPException):
            controllers.get_preview_link("00000001", self.db, self.user_sandbox)

    def test_post_and_get(self):
        post_response = controllers.post_one(
            "sandbox", self.body, self.db, self.user_sandbox
        )
        assert hasattr(post_response, "lars_code")
        assert len(post_response.lars_code) == 8

        # Verify post
        get_one_data = controllers.get_one_newest(post_response.lars_code, self.db)
        assert getattr(get_one_data, "name") == "test_name"
        assert getattr(get_one_data, "organization") == "test_organization"
        assert getattr(get_one_data, "standard_version") == "1.0"

    def test_remove(self):
        remove_response = controllers.remove_one(self.lars_code, self.db)
        assert remove_response is None

        # Test if actually removed
        with pytest.raises(HTTPException):
            controllers.get_one_newest(self.lars_code, self.db)

        # Verify remove when nothing there
        with pytest.raises(HTTPException):
            controllers.remove_one(self.lars_code, self.db)

    def test_set_highlighted_algorithms(self):
        controllers.set_highlighted_algorithms(self.db)
        results = (
            self.db.query(models.PrecomputedValues)
            .filter_by(key=PreComputedValues.highlighted_algorithms)
            .all()
        )
        stored_languages = {r.language for r in results}
        expected_languages = {lang for lang in Language}
        for r in results:
            assert r.key == PreComputedValues.highlighted_algorithms
            
        assert len(results) == len(Language)
        assert stored_languages == expected_languages
        
