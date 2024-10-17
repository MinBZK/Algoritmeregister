from jinja2 import FileSystemLoader, Environment

from app.repositories.html_figures import HtmlFiguresRepository
from etl.figures.templates.figure_mapping import create_figure_mapping
from app.database.database import SessionLocal


def main():
    figure_mapping, data = create_figure_mapping()
    file_loader = FileSystemLoader("etl/figures/templates")
    env = Environment(loader=file_loader)
    template = env.get_template("dashboard_template.html")
    html = template.render(figure_mapping)

    db = SessionLocal()
    html_repo = HtmlFiguresRepository(db)
    html_repo.delete_most_recent()
    html_repo.add(html, data)
    db.commit()
    db.close()


if __name__ == "__main__":
    main()
