from app.middleware.authorisation.schemas import Role
from app.middleware.middleware import get_db
from app.schemas.misc import OrgType
from app.util.logger import get_logger
from app import controllers, schemas, models
from app.services.keycloak import KeycloakUser
from app.controllers.smart_search import get_impact_assessment_filters
from sqlalchemy import select
import json


logger = get_logger(__name__)


class TestImpactGrouping:
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
        self.db.commit()

        # Store default body
        filename = "tests/files/algorithm_4_v1_0.json"
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
        self.db.commit()
        self.db.close()

    def test_impact_assessment_filter_none(self):
        filters = get_impact_assessment_filters(
            schemas.ImpactAssessments.NONE, self.db, schemas.Language.NLD
        )
        stmt = select(models.AlgoritmeVersion).filter(*filters)
        results = self.db.execute(stmt).scalars().all()
        assert isinstance(results, list)
        assert all(
            r.impacttoetsen_grouping is None or "{" not in str(r.impacttoetsen_grouping)
            for r in results
        )

    def test_impact_assessment_filter_correct(self):
        filters = get_impact_assessment_filters(
            schemas.ImpactAssessments.UTHIEK, self.db, schemas.Language.NLD
        )
        stmt = select(models.AlgoritmeVersion).filter(*filters)
        results = self.db.execute(stmt).scalars().all()
        reverse_mapping = schemas.misc.reverse_impact_assessment_titles_mapping[
            schemas.Language.NLD
        ]
        assert isinstance(results, list)
        for r in results:
            assert r.impacttoetsen_grouping is not None
            for assessment in r.impacttoetsen_grouping:
                title = assessment.get("title")
                assert isinstance(title, str)
                enum_key = reverse_mapping.get(title)
                assert enum_key in schemas.misc.standard_impact_assessment_titles
