from bs4 import BeautifulSoup
from datetime import datetime
from functools import reduce
from lxml import html
import pandas as pd
import requests

url = "http://distill.pub"
path = "/rss.xml"

def ingredients(*args):
    return reduce(lambda x, y: f"{x}{y}", args)

def soupify(url, xml=True):
    try:
        r = requests.get(url)
    except HTTPError as e:
        print(e)
        return None
    try:
        return BeautifulSoup(r.content, f"lxml{'-xml' if xml else ''}")
    except Exception as e:
        print(e)
        return None

def channel_to_df(channel):
    titles, urls, publish_dates = [list(map(lambda x: getattr(x, col).text, channel.find_all('item'))) for col in ['title', 'guid', 'pubDate']]
    df = pd.DataFrame({'title': titles, 'url': urls, 'publish_date': publish_dates})
    df['publish_date'] = pd.to_datetime(df['publish_date'], utc = True)
    return df

def process(soup):
    return [channel_to_df(channel) for channel in soup.find_all('channel')]

channels = process(soupify(ingredients(url, path)))
