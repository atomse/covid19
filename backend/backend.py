from flask import Flask
from flask import request, jsonify
import pandas as pd
from datetime import datetime
import dateutil.parser
import threading
import time

app = Flask(__name__)

apiHead = '/api/v1'

global df


"""
Reload / checkUpdate

"""


def reloadDataFrame():
    # global df
    df = pd.read_csv("WHO-COVID-19-global-data.csv")
    df.columns = [_.strip() for _ in df.columns.values]
    return df


df = reloadDataFrame()


def isLatestData():
    global df
    utcnow = datetime.utcnow()
    dataLast = max(df.Date_reported)
    dataLast = dateutil.parser.parse(dataLast)
    if utcnow.year == dataLast.year and utcnow.month == dataLast.month:
        if abs(dataLast.day - utcnow.day) <= 0:
            return True
    return False


def downloadData():
    if app.debug:
        print("Updating Data")
    import requests
    url = "https://covid19.who.int/WHO-COVID-19-global-data.csv"
    response = requests.get(url)
    text = response.content.decode('utf-8-sig')
    with open("WHO-COVID-19-global-data.csv", 'w') as fd:
        fd.write(text)


def checkUpdate():
    global df
    if not isLatestData():
        downloadData()
        df = reloadDataFrame()
        return True
    return False
    # return pd.read_csv("WHO-COVID-19-global-data.csv")


def checkUpdateHourly():
    while True:
        checkUpdate()
        time.sleep(600)


class CheckUpdateThread(threading.Thread):
    def run(self):
        checkUpdateHourly()


AllCountries = list(set(df.Country))
updateThread = CheckUpdateThread()

"""

Get Data


"""


def getCovid19Data(startDate=None, endDate=None, country=None):
    global df
    tempdf = df
    importantCounties = ['China', 'United States of America']
    if country is None:
        country = importantCounties
    elif isinstance(country, str):
        country = [country]
    assert all([_ in AllCountries for _ in country]), 'Invalid country name'
    if startDate and endDate:
        assert startDate <= endDate
    if country:
        tempdf = tempdf[tempdf.Country.isin(country)]
    if startDate:
        tempdf = tempdf[tempdf.Date_reported >= startDate]
    if endDate:
        tempdf = tempdf[tempdf.Date_reported <= endDate]
    items = ['New_cases', 'Cumulative_cases',
             'New_deaths', 'Cumulative_deaths']
    xData = tempdf.Date_reported.tolist()
    yData = {}
    for i in items:
        yData[i] = tempdf[i].tolist()
    response = {
        'xData': xData,
        'yData': yData
    }
    return response


def packData(code, msg, data):
    return {
        'code': code,
        'msg': msg,
        'data': data,
    }


"""


Routers


"""


@app.route(apiHead + '/allCountries')
def allCountries():
    return packData(20000, 'success', AllCountries)


@app.route(apiHead + '/allDate')
def allDate():
    global df
    return packData(20000, 'success', sorted(list(set(df.Date_reported))))


@app.route(apiHead + '/dateRange')
def dateRange():
    global df
    return packData(20000, 'success', {
        'min': min(df.Date_reported),
        'max': max(df.Date_reported)
    })


@app.route(apiHead + '/covid19')
def covid19():
    """
    Using restful
    """
    reqData = request.args or {}
    # import pdb; pdb.set_trace()
    covidData = getCovid19Data(reqData.get("startDate", None), reqData.get(
        "endDate", None), reqData.get("country", None))
    return packData(20000, 'success', covidData)


@app.route('/user/login', methods=['GET', 'POST'])
def login():
    return packData(20000, 'success', {"token": "admin-token"})


@app.route('/user/info', methods=['GET', 'POST'])
def userinfo():
    return packData(20000, 'success', {
        "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
        "introduction": "I am a super administrator",
        "name": "Super Admin",
        "roles": ["admin"]
    })


@app.route('/user/logout', methods=['GET', 'POST'])
def logout():
    return packData(20000, 'success', 'success')


if __name__ == '__main__':
    updateThread.start()
    app.run(port=8080, debug=True)
