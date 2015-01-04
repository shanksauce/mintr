import requests
import json
import re
import csv
from StringIO import StringIO
from pprint import pprint
import config

if __name__ == '__main__':
  print 'Checking Mint...'

  a = requests.get('https://wwws.mint.com/login.event')

  b = requests.post(
    'https://wwws.mint.com/loginUserSubmit.xevent', 
    cookies = a.cookies,
    headers = {'Accept': 'application/json'},
    data = {
      'username': config.USERNAME,
      'password': config.PASSWORD,
      'task': 'L'
    }
  )

  session_id = b.cookies.get('MINTJSESSIONID')
  route_id = b.cookies.get('ROUTEID')

  # This case corresponds to a cookie parsing failure
  if session_id is None or route_id is None:
    raw_cookies = filter(
      lambda x: (re.search('MINTJSESSIONID', x) is not None or
        re.search('ROUTEID', x) is not None),
      reduce(
        lambda x,y: map(str.strip, x) + map(str.strip, y),
        map(
          lambda x: x.strip().split(','),
          b.headers['set-cookie'].replace('Path=/,', '').split(';')
        )
      )
    )

    raw_cookies = dict(map(lambda x: x.split('='), raw_cookies))

    session_id = raw_cookies['MINTJSESSIONID']

    route_id = a.cookies.get('ROUTEID')
    if 'ROUTEID' in raw_cookies:
      route_id = raw_cookies['ROUTEID']

  login_data = b.json()

  auth_headers = {
    'token': login_data['CSRFToken'],
    'cookie': 'MINTJSESSIONID={0}; ROUTEID={1}'.format(session_id, route_id)
  }


  ## Get account summaries
  c = requests.post(
    'https://wwws.mint.com/bundledServiceController.xevent?legacy=false',
    headers = auth_headers,
    data = {
      'input': '[{"args":{"types":["BANK","CREDIT","INVESTMENT","LOAN","MORTGAGE","OTHER_PROPERTY","REAL_ESTATE","VEHICLE","UNCLASSIFIED"]},"service":"MintAccountService","task":"getAccountsSortedByBalanceDescending","id":"420775"},{"args":{"feature":"loan_transaction"},"service":"MintNewFeatureEnablementService","task":"isEnabled","id":"576602"},{"args":{"feature":"investments"},"service":"MintNewFeatureEnablementService","task":"isEnabled","id":"313054"}]'
    }
  )

  accounts = c.json()['response']['420775']['response']

  accounts = map(
    lambda x: (x['fiLoginDisplayName'] + ' - ' + x['name'], x['currentBalance']),
    accounts
  )

  pprint(dict(accounts))


  ## Transactions as JSON
  c = requests.get(
    'https://wwws.mint.com/app/getJsonData.xevent',
    headers = auth_headers,
    params = {
      'accountId': '0',
      'filterType': 'cash',
      'offset': '0',
      'comparableType': '8',
      'acctChanged': 'T',
      'task': 'transactions,txnfilters',
      'rnd': '106'  
    }
  )

  pprint(c.json())

  ## Export to CSV
  c = requests.get(
    'https://wwws.mint.com/transactionDownload.event',
    headers = auth_headers,
    params = {
      'filterType': 'cash',
      'offset': '0',
      'comparableType': '8'
    }
  )

  ## Do something with the data
  for row in csv.reader(StringIO(c.text)):
    pprint(row)
