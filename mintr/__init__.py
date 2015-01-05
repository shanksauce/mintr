import requests
import re

auth_headers = {}

def _validate_credentials(fn):
  def wrapper(*args):
    def is_not_populated(d,r):
      return reduce(
        lambda x,y: x or y, 
        map(lambda k: k not in d or not d[k], r)
      )
    if is_not_populated(auth_headers, ('cookie', 'token')):
      raise Exception('Login first')
    return fn(*args)
  return wrapper


def login(username, password):
  if username is None or password is None:
    raise Exception('Use valid credentials')
  a = requests.get('https://wwws.mint.com/login.event')
  b = requests.post(
    'https://wwws.mint.com/loginUserSubmit.xevent', 
    cookies = a.cookies,
    headers = {'Accept': 'application/json'},
    data = {
      'username': username,
      'password': password,
      'task': 'L'
    }
  )

  token = b.json()['CSRFToken']
  session_id = b.cookies.get('MINTJSESSIONID')
  route_id = b.cookies.get('ROUTEID')

  # This case corresponds to cookie parsing failure
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

  auth_headers['token'] = token
  auth_headers['cookie'] = 'MINTJSESSIONID={0}; ROUTEID={1}'.format(session_id, 
    route_id)


@_validate_credentials
def get_account_summaries():
  input_query = '''[
    {
      "args": {
        "types": [
          "BANK",
          "CREDIT",
          "INVESTMENT",
          "LOAN",
          "MORTGAGE",
          "OTHER_PROPERTY",
          "REAL_ESTATE",
          "VEHICLE",
          "UNCLASSIFIED"
        ]
      },
      "service": "MintAccountService",
      "task": "getAccountsSortedByBalanceDescending",
      "id": "420775"
    }
  ]'''

  c = requests.post(
    'https://wwws.mint.com/bundledServiceController.xevent?legacy=false',
    headers = auth_headers,
    data = {'input': input_query}
  )
  accounts = c.json()['response']['420775']['response']
  accounts = map(
    lambda x: (x['fiLoginDisplayName'] + ' - ' + x['name'], x['currentBalance']),
    accounts
  )
  return dict(accounts)


@_validate_credentials
def get_transactions():
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
  return c.json()


@_validate_credentials
def get_transactions_csv():
  c = requests.get(
    'https://wwws.mint.com/transactionDownload.event',
    headers = auth_headers,
    params = {
      'filterType': 'cash',
      'offset': '0',
      'comparableType': '8'
    }
  )
  return c.text
