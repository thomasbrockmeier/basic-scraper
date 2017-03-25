from bs4 import BeautifulSoup
from lxml import html
from functools import reduce
import pandas as pd
import requests

url = "http://distill.pub"
path = "/rss.xml"

def ingredients(*args):
    return reduce(lambda x, y: f"{x}{y}", args)

def soupify(url):
    try:
        r = requests.get(url)
    except HTTPError as e:
        print(e)
        return None
    try:
        return BeautifulSoup(r.content, 'lxml')
    except Exception as e:
        print(e)
        return None
