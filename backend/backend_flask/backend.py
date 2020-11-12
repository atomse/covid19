"""

This is the backend of Covid19 visualization project


"""

import threading
import time
from datetime import datetime
import dateutil.parser
from flask import Flask
from flask import request
import pandas as pd

app = Flask(__name__)

API_HEAD = '/api/v1'

global COVID19_DF


"""
Reload / checkUpdate

"""


def reload_data_frame():
    """
    Reload DataFrame df from WHO-COVID-19-global-data.csv
    """
    covid19_df = pd.read_csv("WHO-COVID-19-global-data.csv")
    covid19_df.columns = [_.strip() for _ in covid19_df.columns.values]
    return covid19_df


COVID19_DF = reload_data_frame()


def is_latest_data():
    """
    Check if the df is the lastest by checking if latest date if the
    utc now date
    """
    global COVID19_DF
    utcnow = datetime.utcnow()
    data_last = max(COVID19_DF.Date_reported)
    data_last = dateutil.parser.parse(data_last)
    if utcnow.year == data_last.year and utcnow.month == data_last.month:
        if abs(data_last.day - utcnow.day) <= 0:
            return True
    return False


def download_data():
    """
    docs
    """
    if app.debug:
        print("Updating Data")
    import requests
    url = "https://covid19.who.int/WHO-COVID-19-global-data.csv"
    response = requests.get(url)
    text = response.content.decode('utf-8-sig')
    with open("WHO-COVID-19-global-data.csv", 'w') as fd:
        fd.write(text)


def check_update():
    """
    docs
    """
    global COVID19_DF
    if not is_latest_data():
        download_data()
        COVID19_DF = reload_data_frame()
        return True
    return False
    # return pd.read_csv("WHO-COVID-19-global-data.csv")


def check_update_hourly():
    """
    docs
    """
    while True:
        check_update()
        time.sleep(600)


class CheckUpdateThread(threading.Thread):
    """
    CheckUpdateThread
    """

    def run(self):
        check_update_hourly()


ALL_COUNTRIES = list(set(COVID19_DF.Country))
UPDATE_THREAD = CheckUpdateThread()

"""

Get Data


"""


def get_covid19_data(start_date=None, end_date=None, country=None):
    """
    docs
    """
    global COVID19_DF
    temp_df = COVID19_DF
    important_counties = ['China', 'United States of America']
    if country is None:
        country = important_counties
    elif isinstance(country, str):
        country = [country]
    assert all([_ in ALL_COUNTRIES for _ in country]), 'Invalid country name'
    if start_date and end_date:
        assert start_date <= end_date
    if country:
        temp_df = temp_df[temp_df.Country.isin(country)]
    if start_date:
        temp_df = temp_df[temp_df.Date_reported >= start_date]
    if end_date:
        temp_df = temp_df[temp_df.Date_reported <= end_date]
    items = ['New_cases', 'Cumulative_cases',
             'New_deaths', 'Cumulative_deaths']
    x_data = temp_df.Date_reported.tolist()
    y_data = {}
    for i in items:
        y_data[i] = temp_df[i].tolist()
    response = {
        'xData': x_data,
        'yData': y_data
    }
    return response


def pack_data(code, msg, data):
    """
    docs
    """
    return {
        'code': code,
        'msg': msg,
        'data': data,
    }


@app.route(API_HEAD + '/allCountries')
def all_countries():
    """
    docs
    """
    return pack_data(20000, 'success', ALL_COUNTRIES)


@app.route(API_HEAD + '/allDate')
def all_date():
    """
    docs
    """
    global COVID19_DF
    return pack_data(20000, 'success', sorted(list(set(COVID19_DF.Date_reported))))


@app.route(API_HEAD + '/dateRange')
def date_range():
    """
    docs
    """
    global COVID19_DF
    return pack_data(20000, 'success', {
        'min': min(COVID19_DF.Date_reported),
        'max': max(COVID19_DF.Date_reported)
    })


@app.route(API_HEAD + '/covid19')
def covid19():
    """
    docs
    """
    """
    Using restful
    """
    req_data = request.args or {}
    # import pdb; pdb.set_trace()
    covid_data = get_covid19_data(req_data.get("startDate", None), req_data.get(
        "endDate", None), req_data.get("country", None))
    return pack_data(20000, 'success', covid_data)


@app.route('/user/login', methods=['GET', 'POST'])
def login():
    """
    docs
    """
    return pack_data(20000, 'success', {"token": "admin-token"})


@app.route('/user/info', methods=['GET', 'POST'])
def userinfo():
    """
    docs
    """
    return pack_data(20000, 'success', {
        "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
        "introduction": "I am a super administrator",
        "name": "Super Admin",
        "roles": ["admin"]
    })


@app.route('/user/logout', methods=['GET', 'POST'])
def logout():
    """
    docs
    """
    return pack_data(20000, 'success', 'success')


if __name__ == '__main__':
    UPDATE_THREAD.start()
    app.run(port=8080, debug=True)
