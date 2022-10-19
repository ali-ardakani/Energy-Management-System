from celery import shared_task
from celery.utils.log import get_task_logger

from power.models import DemandReport
from power.utils import get_report
import pandas as pd

logger = get_task_logger(__name__)


def add_peaks(df: pd.DataFrame) -> pd.DataFrame:
    """
    > Select the maximum market demand and ontario demand for each day and hour
    
    :param df: pd.DataFrame
    :type df: pd.DataFrame
    :return: A dataframe with the following columns:
        - market_peak_day
        - ontario_peak_day
        - market_peak_month
        - ontario_peak_month
    """
    df['market_peak_day'] = df.groupby(
        df.index.date)['market_demand'].transform(lambda x: x == x.max())
    df['ontario_peak_day'] = df.groupby(
        df.index.date)['ontario_demand'].transform(lambda x: x == x.max())
    df['market_peak_month'] = df.groupby(
        df.index.month)['market_demand'].transform(lambda x: x == x.max())
    df['ontario_peak_month'] = df.groupby(
        df.index.month)['ontario_demand'].transform(lambda x: x == x.max())
    return df


@shared_task
def update_demand_report():
    """
    It takes the last report from the database, and then selects the rows from the report that are after
    the last report
    """
    report = get_report()
    last_obj = DemandReport.objects.last()
    # Selecting the rows that are after the last report
    if last_obj is not None:
        # Converting the last report's date and hour into a datetime object.
        last_report = pd.to_datetime(last_obj.date) + pd.to_timedelta(last_obj.hour, unit='h')
        report = report[report.index > last_report]

    report = add_peaks(report)
    report = report.to_dict('records')
    DemandReport.objects.bulk_create([DemandReport(**row) for row in report])
