from app.schemas.misc import Language

from etl.figures.utils.utils import (
    pretty_print_today,
)

from etl.figures.visualisations.linechart import (
    generate_linechart_published_algorithmdescriptions_permonth,
    generate_linechart_joined_organisations_permonth,
    generate_linechart_broken_links_perday,
)

from etl.figures.visualisations.barchart import generate_barchart_publication_categories


def create_figure_mapping():

    figure_mapping = {
        "chart_joined_organisations_en": generate_linechart_joined_organisations_permonth(Language.ENG, "Period in months", "Joined organisations"),
        "chart_joined_organisations_nl": generate_linechart_joined_organisations_permonth(Language.NLD, "Periode in maanden", "Aangesloten organisaties"),
        "chart_joined_organisations_fy": generate_linechart_joined_organisations_permonth(Language.FRY, "Perioade yn moannen", "Oansletten organisaasjes"),
        "chart_algorithmdescriptions_en": generate_linechart_published_algorithmdescriptions_permonth(Language.ENG, "Period in months", "Published algorithmdescriptions"),
        "chart_algorithmdescriptions_nl": generate_linechart_published_algorithmdescriptions_permonth(Language.NLD, "Periode in maanden", "Gepubliceerde algoritmebeschrijvingen"),
        "chart_algorithmdescriptions_fy": generate_linechart_published_algorithmdescriptions_permonth(Language.FRY, "Perioade yn moannen", "Publisearre algoritmebeskriuwings"),
        "chart_broken_links_en": generate_linechart_broken_links_perday(Language.ENG, "Period in days", "Broken links"),
        "chart_broken_links_nl": generate_linechart_broken_links_perday(Language.NLD, "Periode in dagen", "Gebroken links", ),
        "chart_broken_links_fy": generate_linechart_broken_links_perday(Language.FRY, "Perioade yn dagen", "Brutsen keppelings"),
        "chart_publication_categories_en": generate_barchart_publication_categories(Language.ENG, "Publicationcategories", "Matches"),
        "chart_publication_categories_nl": generate_barchart_publication_categories(Language.NLD, "Publicatiecategorieën", "Aantal"),
        "chart_publication_categories_fy": generate_barchart_publication_categories(Language.FRY, "Publikaasjekategoryen", "Oantal")

    }

    data = {
        "date_stamp": pretty_print_today()
    }
    return figure_mapping, data


if __name__ == "__main__":
    figure_mapping, data = create_figure_mapping()
