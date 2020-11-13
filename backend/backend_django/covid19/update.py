"""

Update Model

Execution: 
    python manage.py  shell -c 'import covid19.update; covid19.update.update_covid19()'

"""

import pandas as pd
from django.db.models import Q
from .models import Covid19


COVID19_FILENAME = '/tmp/WHO-COVID-19-global-data.csv'


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


def update_covid19():
    """
    download data and update covid19 data from WHO and import to DB
    response to /control/update_covid19
    """
    download_data()
    who_file_path = COVID19_FILENAME
    dtype = {
        'Country_code': str,
    }
    covid_df = pd.read_csv(who_file_path, dtype=dtype)
    covid_df.columns = [_.strip() for _ in covid_df.columns.values]
    max_date = get_all_date()[-5]
    covid_df = covid_df.loc[covid_df.Date_reported > max_date]
    columns_values = [
        'Date_reported', 'Country_code', 'Country', 'WHO_region',
        'Cumulative_cases', 'New_cases',
        'Cumulative_deaths', 'New_deaths']
    db_headers = [
        "date", "country_code", "country", "who_region",
        "cumulative_cases", "new_cases",
        "cumulative_deaths", "new_deaths"]
    for i in range(len(covid_df)):
        data = covid_df.iloc[i]
        columns_values = [
            'Date_reported', 'Country_code', 'Country', 'WHO_region',
            'Cumulative_cases', 'New_cases',
            'Cumulative_deaths', 'New_deaths']
        db_headers = [
            "date", "country_code", "country", "who_region",
            "cumulative_cases", "new_cases",
            "cumulative_deaths", "new_deaths"]
        date = data['Date_reported']
        country = data['Country']
        qset = Q(country=country, date=date)
        # import pdb; pdb.set_trace()
        if not Covid19.objects.filter(qset):
            kwargs = {}
            for dfi, dbi in zip(columns_values, db_headers):
                kwargs[dbi] = data[dfi]
            Covid19.objects.create(**kwargs)
    # return pack_data(20000, 'success', 'success')


if __name__ == '__main__':
    update_covid19()
