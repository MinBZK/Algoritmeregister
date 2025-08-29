from typing import Any
from bs4 import BeautifulSoup
from sqlalchemy import delete
from sqlalchemy.orm import Session
from app import models, schemas
from .index import IRepository

from app.util.html import get_static_html
from fastapi import HTTPException


class HtmlFiguresRepository(IRepository):
    def __init__(self, session: Session):
        self.session = session

    def __del__(self):
        self.session.commit()

    def get_all(self):
        pass

    def get_most_recent(self) -> schemas.HtmlFiguresOut:
        html_figures = (
            self.session.query(models.HtmlFigures)
            .filter(models.HtmlFigures.most_recent)
            .one_or_none()
        )
        if not html_figures:
            raise HTTPException(404)

        static_content = get_static_html(html_figures.html)
        static_data = html_figures.static_data or {}

        return schemas.HtmlFiguresOut(
            date=html_figures.date,
            html=html_figures.html,
            static=static_content,
            static_data=static_data,
        )

    def delete_most_recent(self) -> None:
        stmt = delete(models.HtmlFigures).where(models.HtmlFigures.most_recent)
        self.session.execute(stmt)

    def add(self, html: str, static_data: Any) -> schemas.HtmlFigures:
        # Remove hrefs for the archived version
        archived_html = BeautifulSoup(html, "lxml")
        for a in archived_html.findAll("a"):
            del a["href"]

        new_record = models.HtmlFigures(
            html=html, static_data=static_data, most_recent=True
        )
        archived_record = models.HtmlFigures(
            html=str(archived_html), static_data=static_data, most_recent=False
        )
        self.session.add(new_record)
        self.session.add(archived_record)
        self.session.flush()

        return schemas.HtmlFigures.model_validate(new_record)
