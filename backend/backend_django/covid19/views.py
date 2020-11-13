"""


Main functions for covid19 backend


"""


import json
import pandas as pd
from django.http import HttpResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .models import Covid19, Covid19Country, Covid19Latest, Covid19Date


def pack_data(code, msg, data):
    """
    pack data from request function to a HttpResponse object
    """
    return HttpResponse(json.dumps({
        'code': code,
        'msg': msg,
        'data': data,
    }))


def get_all_countries():
    """
    get all countries names from db
    """
    countries = list(Covid19Country.objects.all().values())
    countries = [_['country'] for _ in countries]
    # import pdb; pdb.set_trace()
    return sorted(countries)


@csrf_exempt
def all_countries(request):
    """
    response /api/v1/allCountries request
    """
    countries = get_all_countries()
    return pack_data(20000, 'success', countries)


def get_all_date():
    """
    get all data from db
    """
    data = Covid19.objects.all().values('date')
    data = list(set([_['date'].strftime('%Y-%m-%d') for _ in data]))
    return sorted(data)


def get_min_max_date():
    obj = Covid19Date.objects.filter(id=1).values()
    obj = list(obj)[0]
    min_date = obj['min_date'].strftime('%Y-%m-%d')
    max_date = obj['max_date'].strftime('%Y-%m-%d')
    return min_date, max_date


@csrf_exempt
def date_range(request):
    """
    response /api/v1/dateRange request
    """
    min_date, max_date = get_min_max_date()
    return pack_data(20000, 'success', {
        'min': min_date,
        'max': max_date,
    })


def get_covid19_data(start_date=None, end_date=None, country=None):
    """
    get covid19 data from DB with start_date, end_date and country
    args:
        start_date:
            DB start date
            format: date string, e.g. "2020-01-01"
        end_date:
            DB end date
            format: date string, e.g. "2020-01-01"
        country:
            default: 'China'
            format: str
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


@csrf_exempt
def covid19(request):
    """
    response /api/v1/covid19 request
        args: startDate, endDate, country
    """
    req_data = request.GET or {}
    start_date = req_data.get("startDate", None)
    end_date = req_data.get("endDate", None)
    country = req_data.get("country", None)
    # print(start_date, end_date, country)
    covid_data = get_covid19_data(start_date, end_date, country)
    return pack_data(20000, 'success', covid_data)


@csrf_exempt
def covid19_latest_numbers(request):
    """
    response /api/v1/covid19LatestNumbers request
        args: topN
        return: xData, countryCode, yData
    """
    top_n = request.GET.get('topN', None)
    if top_n:
        top_n = int(top_n)
    # import pdb; pdb.set_trace()
    data = list(Covid19Latest.objects.all().order_by('-cumulative_cases').values())
    temp_df = pd.DataFrame(data)
    x_data = temp_df['country'].tolist()
    country_code = temp_df['country_code'].tolist()
    if top_n:
        x_data = x_data[:top_n] + ['Others']
        country_code = country_code[:top_n] + ['Others']
    items = [
        "cumulative_cases", "new_cases",
        "cumulative_deaths", "new_deaths",
    ]
    y_data = {}
    for i in items:
        item_data = temp_df[i].tolist()
        if top_n:
            y_data[i] = item_data[:top_n] + [sum(item_data[top_n:])]
        else:
            y_data[i] = item_data
    return pack_data(20000, 'success', {
        'xData': x_data,
        'countryCode': country_code,
        'yData': y_data,
    })


@csrf_exempt
def user_login(request):
    """
    auxilary request method to /user/login for vue-element-admin
    """
    return pack_data(20000, 'success', {"token": "admin-token"})


@csrf_exempt
def user_info(request):
    """
    auxilary request method to /user/info for vue-element-admin
    """
    avatar_url = "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif"
    return pack_data(20000, 'success', {
        "avatar": avatar_url,
        "introduction": "I am a super administrator",
        "name": "Super Admin",
        "roles": ["admin"]
    })


@csrf_exempt
def user_logout(request):
    """
    auxilary request method to /user/logout for vue-element-admin
    """
    return pack_data(20000, 'success', 'success')
