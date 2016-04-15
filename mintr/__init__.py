import requests
import time
import re
from pprint import pprint

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
  session_id = a.cookies.get('MINTJSESSIONID')
  route_id = a.cookies.get('ROUTEID')

  b = requests.post(
    'https://wwws.mint.com/loginUserSubmit.xevent',
    cookies = a.cookies,
    headers = {
      'Accept': 'application/json',
      'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'Cookie': 'MINTJSESSIONID={0}; ROUTEID={1}'.format(session_id,
        route_id)
    },
    data = {
      'username': username,
      'password': password,
      'task': 'L'
    }
  )

  csrf_token = b.json()['CSRFToken']

  match = re.search('MINTJSESSIONID=(.*?);', b.headers['set-cookie'])
  if match is None:
    raise Exception('No MINTJSESSIONID')
  b_session_id = match.groups(0)[0]


#@_validate_credentials
def get_account_summaries(jwt=None):
  if jwt is None:
    return {}
  try:
    d = requests.get(
      'https://mint.finance.intuit.com/v1/accounts?limit=1000',
      headers = {'Authorization': 'Bearer ' + jwt}
    )
    accounts = dict(map(
      lambda x: (
        x['fiName'] + ' ' + x['cpAccountName'],
        x['currentBalance']
      ),
      filter(
        lambda x: x['accountStatus'] == 'ACTIVE' and x['currentBalance'] > 0,
        d.json()['Account']
      )
    ))
    return accounts
  except Exception as ex:
    return {}
