from django.db import models

# Create your models here.


class Covid19(models.Model):
    """
    WHO data format:
    Date_reported, Country_code, Country, WHO_region, New_cases, Cumulative_cases, New_deaths, Cumulative_deaths
    2020-01-03,AF,Afghanistan,EMRO,0,0,0,0
    2020-01-04,AF,Afghanistan,EMRO,0,0,0,0
    2020-01-05,AF,Afghanistan,EMRO,0,0,0,0
    """
    date = models.DateField()
    country = models.CharField(max_length=50)
    country_code = models.CharField(max_length=50)
    who_region = models.CharField(max_length=50)
    new_cases = models.IntegerField()
    cumulative_cases = models.IntegerField()
    new_deaths = models.IntegerField()
    cumulative_deaths = models.IntegerField()


class Covid19Country(models.Model):
    country = models.CharField(max_length=50)
    country_code = models.CharField(max_length=50)


class Covid19Latest(models.Model):
    country = models.CharField(max_length=50)
    country_code = models.CharField(max_length=50)
    who_region = models.CharField(max_length=50)
    new_cases = models.IntegerField()
    cumulative_cases = models.IntegerField()
    new_deaths = models.IntegerField()
    cumulative_deaths = models.IntegerField()


class Covid19Date(models.Model):
    min_date = models.DateField()
    max_date = models.DateField()
