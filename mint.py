import requests
import json
import re
from pprint import pprint
import config

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

c = requests.post(
  'https://wwws.mint.com/bundledServiceController.xevent?legacy=false',
  headers = {
    'token': login_data['CSRFToken'],
    'cookie': 'MINTJSESSIONID={0}; ROUTEID={1}'.format(session_id, route_id)
  },
  data = {
    'input': '[{"args":{"types":["BANK","CREDIT","INVESTMENT","LOAN","MORTGAGE","OTHER_PROPERTY","REAL_ESTATE","VEHICLE","UNCLASSIFIED"]},"service":"MintAccountService","task":"getAccountsSortedByBalanceDescending","id":"420775"},{"args":{"feature":"loan_transaction"},"service":"MintNewFeatureEnablementService","task":"isEnabled","id":"576602"},{"args":{"feature":"investments"},"service":"MintNewFeatureEnablementService","task":"isEnabled","id":"313054"},{"args":{},"service":"MintUserService","task":"getUserPreferences","id":"510931"},{"args":{},"service":"MintFILoginService","task":"isUserFILoginRefreshing","id":"225162"}]'
  }
)

accounts = c.json()['response']['420775']['response']

accounts = map(
  lambda x: (x['fiLoginDisplayName'] + ' - ' + x['name'], x['currentBalance']),
  accounts
)

pprint(dict(accounts))

#for account in accounts:
#  print account['name'], account['currentBalance']


