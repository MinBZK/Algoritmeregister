from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, time
from app import schemas
from app.models.dashboard_models.broken_links import BrokenLinks
from app.schemas.broken_links import BrokenLink, BrokenLinkCount
from app.schemas.misc import Language
from .index import IRepository


class BrokenLinksRepository(IRepository):
    def __init__(self, session: Session):
        self.session = session

    def __del__(self):
        self.session.commit()

    def get_all(self) -> list[schemas.BrokenLink]:
        actions = self.session.query(BrokenLinks).all()
        return [schemas.BrokenLink.model_validate(a) for a in actions]

    def add(self, action: schemas.BrokenLink) -> schemas.BrokenLink:
        action_model = BrokenLink(**action.model_dump())
        self.session.add(action_model)
        self.session.flush()
        return schemas.BrokenLink.model_validate(action_model)

    def get_newest_batch_by_lang(self, lang: Language) -> list[schemas.BrokenLink]:
        max_batch = (
            self.session.query(func.max(BrokenLinks.batch))
            .filter(BrokenLinks.language == lang)
            .scalar()
        )

        broken_links = (
            self.session.query(BrokenLinks)
            .filter(BrokenLinks.language == lang)
            .filter(BrokenLinks.batch == max_batch)
            .order_by(BrokenLinks.create_dt.desc())
        ).all()

        return [BrokenLink.model_validate(link) for link in broken_links]

    def get_newest_batch_two_weeks_by_lang(
        self, lang: Language
    ) -> list[schemas.BrokenLinkCount]:
        fourteen_days_ago = datetime.now() - timedelta(days=14)

        broken_links_count = (
            self.session.query(
                func.count(BrokenLinks.id).label("count"),
                func.date(BrokenLinks.create_dt),
            )
            .filter(BrokenLinks.language == lang)
            .filter(BrokenLinks.create_dt >= fourteen_days_ago)
            .group_by(BrokenLinks.create_dt)
        ).all()

        return [
            BrokenLinkCount(
                count=count, create_dt=datetime.combine(create_dt, time.min)
            )
            for count, create_dt in broken_links_count
        ]
