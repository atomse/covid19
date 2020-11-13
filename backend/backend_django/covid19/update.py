"""

Update Model

Execution: 
    python manage.py  shell -c 'import covid19.update; covid19.update.update_covid19()'

"""

import pandas as pd
from django.db.models import Q
from .models import Covid19, Covid19Country, Covid19Latest, Covid19Date


COVID19_FILENAME = '/tmp/WHO-COVID-19-global-data.csv'
DF_COLUMNS_VALUES = [
    'Date_reported', 'Country_code', 'Country', 'WHO_region',
    'Cumulative_cases', 'New_cases',
    'Cumulative_deaths', 'New_deaths']
DB_HEADERS = [
    "date", "country_code", "country", "who_region",
    "cumulative_cases", "new_cases",
    "cumulative_deaths", "new_deaths"]


def get_all_date():
    """
    get all data from db
    """
    data = Covid19.objects.all().values('date')
    data = list(set([_['date'].strftime('%Y-%m-%d') for _ in data]))
    return sorted(data)


def download_data():
    """
    download data from WHO as csv to `/tmp/`
    """
    import requests
    url = "https://covid19.who.int/WHO-COVID-19-global-data.csv"
    response = requests.get(url)
    text = response.content.decode('utf-8-sig')
    filename = COVID19_FILENAME
    with open(filename, 'w') as f_fd:
        f_fd.write(text)


def update_covid19_country():
    """
    update all countries
    country, country_code
    """
    dtype = {
        'Country_code': str,
    }
    covid_df = pd.read_csv(COVID19_FILENAME, dtype=dtype)
    covid_df.columns = [_.strip() for _ in covid_df.columns.values]

    df = covid_df.groupby("Country")["Country_code"].last().reset_index()
    for i in range(len(df)):
        data = df.iloc[i]
        country_code = data['Country_code']
        country = data['Country']
        if not Covid19Country.objects.filter(Q(country=country)):
            Covid19Country.objects.create(
                country=country, country_code=country_code)


def update_covid19_latest():
    """
    country_code, country, who_region, new_cases, cumulative_cases, new_deaths, cumulative_deaths
    """
    dtype = {
        'Country_code': str,
    }
    covid_df = pd.read_csv(COVID19_FILENAME, dtype=dtype)
    covid_df.columns = [_.strip() for _ in covid_df.columns.values]
    covid_df = covid_df.groupby('Country').last().reset_index()
    for i in range(len(covid_df)):
        data = covid_df.iloc[i]
        country = data['Country']
        kwargs = {}
        for dfi, dbi in zip(DF_COLUMNS_VALUES, DB_HEADERS):
            if dbi == 'date':
                continue
            kwargs[dbi] = data[dfi]
        query = Covid19Latest.objects.filter(Q(country=country))
        if query:
            query.update(**kwargs)
        else:
            Covid19Latest.objects.create(**kwargs)


def update_covid19_date():
    """
    update_covid19_date
    """
    dtype = {
        'Country_code': str,
    }
    covid_df = pd.read_csv(COVID19_FILENAME, dtype=dtype)
    covid_df.columns = [_.strip() for _ in covid_df.columns.values]

    min_date = covid_df.Date_reported.min()
    max_date = covid_df.Date_reported.max()

    if not Covid19Date.objects.all():
        Covid19Date.objects.create(
            min_date=min_date, max_date=max_date)
    else:
        Covid19Date.objects.filter(id=1).update(
            min_date=min_date, max_date=max_date)



def update_covid19_db():
    """
    update_covid19_db
    """
    dtype = {
        'Country_code': str,
    }
    covid_df = pd.read_csv(COVID19_FILENAME, dtype=dtype)
    covid_df.columns = [_.strip() for _ in covid_df.columns.values]

    max_date = get_all_date()[-5]
    covid_df = covid_df.loc[covid_df.Date_reported > max_date]
    for i in range(len(covid_df)):
        data = covid_df.iloc[i]
        date = data['Date_reported']
        country = data['Country']
        qset = Q(country=country, date=date)
        if not Covid19.objects.filter(qset):
            kwargs = {}
            for dfi, dbi in zip(DF_COLUMNS_VALUES, DB_HEADERS):
                kwargs[dbi] = data[dfi]
            Covid19.objects.create(**kwargs)


def update_covid19():
    """
    download data and update covid19 data from WHO and import to DB
    response to /control/update_covid19
    """
    download_data()
    update_covid19_db()
    update_covid19_country()
    update_covid19_latest()
    update_covid19_date()
    # return pack_data(20000, 'success', 'success')


if __name__ == '__main__':
    update_covid19()
