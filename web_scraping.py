import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

## OBTAIN URLS

n_pages = 200
URLS = []
URL_MAIN = 'https://www.euraxess.org.uk/jobs/search'
for root in range(n_pages):
    index = 'https://www.euraxess.org.uk/jobs/search?page=' + str(root + 1)
    URLS.append(index)

URLS.insert(0, URL_MAIN)

## GET TOPICS and DATES FROM THE URLs

foo_topics = []
foo_dates = []
for URL in URLS:
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36"})
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    topics_html = soup.find_all('h2')
    dates_html = soup.find_all('div', class_="value iblock")
    topics = []
    dates = []
    for i in range(len(topics_html)):
        topic = topics_html[i].text
        topics.append(topic)
    for i in range(len(dates_html)):
        date = dates_html[i].text
        dates.append(date)
    topics = topics[2:]
    foo_topics.append(topics)
    foo_dates.append(dates)

## GET DEADLINES, FIELDS, LOCATIONS, INSTITUTES

foo_deadlines = []
foo_fields = []
foo_locations = []
foo_institutes = []
for URL in URLS:
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36"})
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    classes_html = soup.find_all('div', class_='col-xs-12 col-sm-7 col-md-6 value')
    deadlines = []
    fields = []
    locations = []
    institutes = []
    for i in range(int(len(classes_html)/4)):
        deadline = classes_html[i*4].text
        field = classes_html[i*4 + 1].text
        location = classes_html[i*4 + 2].text
        institute = classes_html[i*4 + 3].text
        deadlines.append(deadline)
        fields.append(field)
        locations.append(location)
        institutes.append(institute)
    foo_deadlines.append(deadlines)
    foo_fields.append(fields)
    foo_locations.append(locations)
    foo_institutes.append(institutes)

## OBTAIN ALL TOPICS IN ONE ARRAY

all_topics = []
all_dates = []
all_deadlines = []
all_fields = []
all_locations = []
all_institutes = []
for arr in foo_topics:
    for i in arr:
        all_topics.append(i)
for arr in foo_dates:
    for i in arr:
        all_dates.append(i)
for arr in foo_deadlines:
    for i in arr:
        all_deadlines.append(i)
for arr in foo_fields:
    for i in arr:
        all_fields.append(i)
for arr in foo_locations:
    for i in arr:
        all_locations.append(i)
for arr in foo_institutes:
    for i in arr:
        all_institutes.append(i)

## OBTAIN DATA FRAME

df = pd.DataFrame(list(zip(
    all_dates,
    all_topics,
    all_deadlines,
    all_fields,
    all_locations,
    all_institutes)),
    columns=['Date', 'Topics', 'Deadlines', 'Fields', 'Locations', 'Institutes'])

## OBTAIN PHDs ON DATA SCIENCE, DATA ANALYSIS, MACHINE LEARNING and COMPUTER VISION


def get_df(df, subject):
    data = df['Topics'].str.find(subject)
    data_index = data[data  != -1]
    data_index = data_index.index.values.tolist()
    result = df.iloc[data_index, :]
    return result


df_phd = get_df(df, 'PhD')
df_phd = df_phd.reset_index().drop(columns='index')
df_ml = get_df(df_phd, 'Machine Learning')
df_cv = get_df(df_phd, 'Computer Vision')
df_data = get_df(df_phd, 'Data')

print(df_phd)
print('\n')
print(df_ml)
print('\n')
print(df_cv)
print('\n')
print(df_data)