from datetime import datetime
from bs4 import BeautifulSoup
import base64


def pretty_print_today():
    today = datetime.today()
    day_of_week = (today.weekday() + 1) % 7 + 1
    return f"{day_of_week} {today.day} {today.month} {today.year}"


def add_scope_to_table(table):
    try:
        soup = BeautifulSoup(str(table), "lxml")
        for th in soup.find_all("th"):
            th["scope"] = "col"
        return str(soup)
    except:
        return table


def plotly_fig_to_png(fig):
    img_bytes = fig.to_image(format="png")
    base64_bytes = base64.b64encode(img_bytes)
    return base64_bytes.decode()
