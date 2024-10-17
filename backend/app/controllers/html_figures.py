from sqlalchemy.orm import Session
from app import schemas
from app.repositories.html_figures import HtmlFiguresRepository


def get_html_figures_recent(db: Session) -> schemas.HtmlFigures:
    html_figures_repo = HtmlFiguresRepository(db)
    return html_figures_repo.get_most_recent()
