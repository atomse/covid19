"""


Covid 19 update module

insert into crontab with



"""


import time
from datetime import datetime
import dateutil.parser


def is_latest_data():
    """
    Check if the df is the lastest by checking if latest date if the
    utc now date
    """
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
    import requests
    url = "https://covid19.who.int/WHO-COVID-19-global-data.csv"
    response = requests.get(url)
    text = response.content.decode('utf-8-sig')
    filename = os.path.join(BASEDIR, os.path.basename(url))
    with open(filename, 'w') as fd:
        fd.write(text)


def check_update():
    """
    docs
    """
    if not is_latest_data():
        download_data()
        return True
    return False
    # return pd.read_csv("WHO-COVID-19-global-data.csv")


if __name__ == '__main__':
    check_update()
