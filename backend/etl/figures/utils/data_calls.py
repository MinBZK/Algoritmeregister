import pandas as pd
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta

from app.database.database import SessionLocal
from app.repositories.algoritme_version import AlgoritmeVersionRepository
from app.schemas.algoritme_version import AlgoritmeVersionEarliestPublish
from app.schemas.algoritme_version import PublicationCategoryCount
from app.schemas.broken_links import BrokenLinkCount
from app.repositories.broken_links import BrokenLinksRepository
from app.schemas.organization import OrganisationJoinedDate
from app.schemas.misc import Language
from etl.figures.controllers.joined_organisations import (
    get_all_organisations_joined_date,
)


def create_dataframe(
    data: list[AlgoritmeVersionEarliestPublish] | list[OrganisationJoinedDate],
    columnName: str,
) -> tuple[pd.DataFrame, int]:
    daily_dic = {}

    # Build occurence per day dictionary
    for row in data:
        dt = row.create_dt
        _id = f"{dt.day}-{dt.month}-{dt.year}"
        if _id not in daily_dic:
            daily_dic[_id] = {columnName: [], "aantal": 0}
        daily_dic[_id]["aantal"] += 1

    # dict from df
    df = pd.DataFrame.from_dict(daily_dic, orient="index", columns=["aantal"])
    df.index = pd.to_datetime(df.index, format="%d-%m-%Y", dayfirst=True).to_period(freq="D")
    df = df.sort_index()

    # Start_date of the dataset must be at least twelve months ago.
    twelve_months_ago_dt = datetime.now(timezone.utc) - relativedelta(months=11)
    twelve_months_ago_str = twelve_months_ago_dt.strftime("%d-%m-%Y")
    twelve_months_ago = pd.to_datetime(twelve_months_ago_str, format="%d-%m-%Y", dayfirst=True).to_period(freq="D")  
    earliest_date = df.index.min()
    if earliest_date < twelve_months_ago:
        start_date = earliest_date
    else:
        start_date = twelve_months_ago
    
    current_date_str = datetime.now().strftime("%d-%m-%Y")
    current_date = pd.to_datetime(current_date_str, format="%d-%m-%Y", dayfirst=True).to_period(freq="D")

    df = df.reindex(
        pd.period_range(start_date, current_date, freq="D")
    )

    df["aantal"] = df["aantal"].infer_objects().fillna(0)
    df["aantal"] = df["aantal"].cumsum()

    if isinstance(df.index, pd.PeriodIndex):
        df.index = df.index.strftime('%d-%m-%Y')

    df2 = df.set_index(df.index.values.astype(str))

    max_count = df2["aantal"].max().astype(int)

    twelve_months_ago_str = twelve_months_ago_dt.strftime("01-%m-%Y")
    twelve_months_ago = pd.to_datetime(twelve_months_ago_str, format="%d-%m-%Y", dayfirst=True)

    df2.index = pd.to_datetime(df2.index, format="%d-%m-%Y", dayfirst=True)

    # Filter the DataFrame for the last twelve months
    df_12_months = df2[df2.index >= twelve_months_ago]
    return (df_12_months, max_count)


def create_dataframe_broken_links(data: list[BrokenLinkCount]) -> tuple[pd.DataFrame, int]:
    daily_dic = {}
    # Build occurence per day dictionary
    for row in data:
        dt = row.create_dt
        _id = f"{dt.day}-{dt.month}-{dt.year}"
        daily_dic[_id] = {"aantal": row.count}

    # dict from df
    df = pd.DataFrame.from_dict(daily_dic, orient="index", columns=["aantal"])
    df.index = pd.to_datetime(df.index, format="%d-%m-%Y").to_period(freq="D")
    df = df.sort_index()

    # Start_date of the dataset must be at least 14 days ago.
    fourteen_days_ago_dt = datetime.now(timezone.utc) - relativedelta(days=14)
    fourteen_days_ago = pd.Period(fourteen_days_ago_dt.strftime("%Y-%m-%d"), freq="D")
    earliest_date = df.index.min()
    if earliest_date < fourteen_days_ago:
        start_date = earliest_date
    else:
        start_date = fourteen_days_ago
    current_date = datetime.now().strftime("%Y-%m-%d")
    df = df.reindex(
        pd.period_range(start_date, pd.Period(current_date, freq="D"), freq="D")
    )

    df["aantal"] = df["aantal"].infer_objects().fillna(0)

    
    if isinstance(df.index, pd.PeriodIndex):
        df.index = df.index.strftime('%d-%m')

    df2 = df.set_index(df.index.values.astype(str))

    max_count = df["aantal"].max().astype(int)
    return (df2, max_count)


def create_dataframe_publicationcategories(data: list[PublicationCategoryCount], pg_title: str, count_title: str) -> tuple[pd.DataFrame, int]: 
    dic = [{pg_title: obj.category, count_title: obj.count} for obj in data]
    df = pd.DataFrame(dic)

    return df, df[pg_title].max()
    

def published_algorithmdescriptions_permonth() -> tuple[pd.DataFrame, int]:
    db = SessionLocal()
    algo_repo = AlgoritmeVersionRepository(db)
    algorithms = algo_repo.get_all_published_first_version()
    return create_dataframe(algorithms, "algoritmes")


def organisations_permonth() -> tuple[pd.DataFrame, int]:
    db = SessionLocal()
    orgs = get_all_organisations_joined_date(db)
    return create_dataframe(orgs, "organisaties")


def broken_links_perday(lang: Language) -> tuple[pd.DataFrame, int]:
    db = SessionLocal()
    brokenlink_repo = BrokenLinksRepository(db)
    broken_links = brokenlink_repo.get_newest_batch_two_weeks_by_lang(lang)
    return create_dataframe_broken_links(broken_links)


def publication_categories(lang: Language, x_axis_title: str, y_axis_title: str) -> tuple[pd.DataFrame, int]:
    db = SessionLocal()
    algo_repo = AlgoritmeVersionRepository(db)
    publication_categories = algo_repo.get_all_published_by_pubcat(lang)
    return create_dataframe_publicationcategories(publication_categories, x_axis_title, y_axis_title)
