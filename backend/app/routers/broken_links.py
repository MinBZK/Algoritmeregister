from fastapi import APIRouter, Depends, Path
from app import repositories
from app.middleware.middleware import get_db
from sqlalchemy.orm import Session
from app.schemas.broken_links import BrokenLink
from app.schemas.misc import Language
from app.middleware.authorisation.authoriser import AuthType, Authoriser


router = APIRouter()


@router.get(
    "/broken-links/{language}",
    response_model=list[BrokenLink],
    dependencies=[Depends(Authoriser(AuthType.BaseOnly))],
)
async def get_broken_links(
    db: Session = Depends(get_db),
    language: Language = Path(alias="language"),
) -> list[BrokenLink]:
    brokenlink_repo = repositories.BrokenLinksRepository(db)
    return brokenlink_repo.get_newest_batch_by_lang(language)
