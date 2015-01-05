import config
import csv
import mintr
from StringIO import StringIO
from pprint import pprint

mintr.login(config.USERNAME, config.PASSWORD)
pprint(mintr.get_account_summaries())
pprint(mintr.get_transactions())
for row in csv.reader(StringIO(mintr.get_transactions_csv())):
  pprint(row)
  break
