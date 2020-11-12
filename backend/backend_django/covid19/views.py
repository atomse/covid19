import json
from django.http import HttpResponse
# from django.shortcuts import render

# Create your views here.
from django.db.models import Q
from .models import Covid19
import pandas as pd
from django.views.decorators.csrf import csrf_exempt


COVID19_FILENAME = '/tmp/WHO-COVID-19-global-data.csv'


def pack_data(code, msg, data):
    """
    docs
    """
    return HttpResponse(json.dumps({
        'code': code,
        'msg': msg,
        'data': data,
    }))


def get_all_countries():
    countries = Covid19.objects.all().values('country')
    countries = list(set([_['country'] for _ in countries]))
    # import pdb; pdb.set_trace()
    return sorted(countries)


@csrf_exempt
def all_countries(request):
    """
    docs
    """
    countries = get_all_countries()
    return pack_data(20000, 'success', countries)


def get_all_date():
    data = Covid19.objects.all().values('date')
    data = list(set([_['date'].strftime('%Y-%m-%d') for _ in data]))
    return sorted(data)


def all_date(request):
    """
    docs
    """
    data = get_all_date()
    return pack_data(20000, 'success', data)


@csrf_exempt
def date_range(request):
    """
    docs
    """
    date = get_all_date()
    return pack_data(20000, 'success', {
        'min': min(date),
        'max': max(date)
    })


def get_covid19_data(start_date=None, end_date=None, country=None):
    """
    docs
    """
    important_counties = ['China']
    if country is None:
        country = important_counties
    elif isinstance(country, str):
        country = [country]
    assert all([_ in get_all_countries()
                for _ in country]), 'Invalid country name'
    if start_date and end_date:
        assert start_date <= end_date
    qset = Q(country__in=country)
    if start_date:
        qset = qset & Q(date__gte=start_date)
    if end_date:
        qset = qset & Q(date__lte=end_date)
    data = list(Covid19.objects.filter(qset).order_by('date').values())
    # import pdb; pdb.set_trace()
    items = [
        "cumulative_cases", "new_cases",
        "cumulative_deaths", "new_deaths"
    ]
    temp_df = pd.DataFrame(data)
    x_data = [_.strftime('%Y-%m-%d') for _ in temp_df['date'].tolist()]
    y_data = {}
    for i in items:
        y_data[i] = temp_df[i].tolist()
    response = {
        'xData': x_data,
        'yData': y_data
    }
    return response


def covid19(request):
    """
    Using restful
    """
    req_data = request.GET or {}
    # import pdb; pdb.set_trace()
    start_date = req_data.get("startDate", None)
    end_date = req_data.get("endDate", None)
    country = req_data.get("country", None)
    # print(start_date, end_date, country)
    covid_data = get_covid19_data(start_date, end_date, country)
    return pack_data(20000, 'success', covid_data)


def covid19_latest_numbers(request):
    top_n = int(request.GET.get('topN', 10))
    max_date = max(get_all_date())
    qset = Q(date=max_date)
    data = list(Covid19.objects.filter(
        qset).order_by('-new_cases').values())
    temp_df = pd.DataFrame(data)
    x_data = temp_df['country'].tolist()
    x_data = x_data[:top_n] + ['Others']
    items = [
        "cumulative_cases", "new_cases",
        "cumulative_deaths", "new_deaths"
    ]
    y_data = {}
    for i in items:
        item_data = temp_df[i].tolist()
        y_data[i] = item_data[:top_n] + [sum(item_data[top_n:])]
    return pack_data(20000, 'success', {
        'xData': x_data,
        'yData': y_data
    })


def download_data():
    """
    docs
    """
    import requests
    url = "https://covid19.who.int/WHO-COVID-19-global-data.csv"
    response = requests.get(url)
    text = response.content.decode('utf-8-sig')
    filename = COVID19_FILENAME
    with open(filename, 'w') as fd:
        fd.write(text)


def update_covid19(request):
    """
    docs
    """
    download_data()
    who_file_path = COVID19_FILENAME
    df = pd.read_csv(who_file_path)
    df.columns = [_.strip() for _ in df.columns.values]
    max_date = max(get_all_date())
    df = df.loc[df.Date_reported > max_date]
    for i in range(len(df)):
        data = df.iloc[i]
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
    return pack_data(20000, 'success', 'success')


@csrf_exempt
def login(request):
    """
    docs
    """
    return pack_data(20000, 'success', {"token": "admin-token"})


@csrf_exempt
def userinfo(request):
    """
    docs
    """
    avatar_url = "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif"
    return pack_data(20000, 'success', {
        "avatar": avatar_url,
        "introduction": "I am a super administrator",
        "name": "Super Admin",
        "roles": ["admin"]
    })


@csrf_exempt
def logout(request):
    """
    docs
    """
    return pack_data(20000, 'success', 'success')
