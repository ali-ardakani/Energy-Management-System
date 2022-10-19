# utils.py
# Get the report from the url(http://reports.ieso.ca/public/Demand) if not already in the database and save it
import requests
from bs4 import BeautifulSoup
import io
import pandas as pd

def download_csv(url: str) -> pd.DataFrame:
    print(url)
    response = requests.get(url)   
    
    df = pd.read_csv(
        io.StringIO(response.content.decode('utf-8')),
        skiprows=4,
        names=['date', 'hour', 'market_demand', 'ontario_demand'],
        dtype={'hour': int, 'market_demand': int, 'ontario_demand': int})
    return df

def get_report():
    """
    It downloads the IESO's demand report webpage, finds all the links to CSV files, and then downloads
    each CSV file and concatenates them into a single dataframe
    :return: A dataframe with the date, hour, market demand, and ontario demand.
    """
    url = 'http://reports.ieso.ca/public/Demand'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    reports = soup.find_all('a', href=True)
    df = pd.DataFrame(
        columns=['date', 'hour', 'market_demand', 'ontario_demand'])
    for report in reports:
        if '.csv' in report.text.lower():
            report_url = "http://reports.ieso.ca/public/Demand/" + report[
                'href']
            df = pd.concat([df, download_csv(report_url)], ignore_index=True)
    df.index = pd.to_datetime(df['date']) + pd.to_timedelta(df['hour'], unit='h')
    df.sort_index(inplace=True)
    return df
