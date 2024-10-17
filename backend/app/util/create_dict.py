from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta


def create_dict(data):
    twelve_months_ago = datetime.now() - relativedelta(months=12)

    monthly_counts = defaultdict(int)

    for row in data:
        dt = row.create_dt
        date_id = f"{dt.month}-{dt.year}"
        monthly_counts[date_id] += 1

    current_date = datetime.now()
    while twelve_months_ago <= current_date:
        date_id = f"{twelve_months_ago.month}-{twelve_months_ago.year}"
        if date_id not in monthly_counts:
            monthly_counts[date_id] = 0
        twelve_months_ago += relativedelta(months=1)

    sorted_months = sorted(
        monthly_counts.keys(), key=lambda x: datetime.strptime(x, "%m-%Y")
    )

    cumulative_count = 0
    for month in sorted_months:
        cumulative_count += monthly_counts[month]
        monthly_counts[month] = cumulative_count

    monthly_data = [
        {"date": month, "count": monthly_counts[month]} for month in sorted_months
    ]
    twelve_months_data = monthly_data[-12:]

    return twelve_months_data
