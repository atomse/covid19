import request from '@/utils/request'

export function fetchCountries(query) {
  return request({
    url: '/api/v1/allCountries',
    method: 'get',
    params: query
  })
}

export function fetchAllDate(query) {
  return request({
    url: '/api/v1/allDate',
    method: 'get',
    params: query
  })
}

export function fetchDateRange(query) {
  return request({
    url: '/api/v1/dateRange',
    method: 'get',
    params: query
  })
}

export function fetchCovidID19Data(query) {
  return request({
    url: '/api/v1/covid19',
    method: 'get',
    params: query
  })
}

export function fetchCovid19LatestNumbers(query) {
  return request({
    url: '/api/v1/covid19LatestNumbers',
    method: 'get',
    params: query
  })
}
