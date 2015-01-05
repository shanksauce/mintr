import config
import csv
import mint
from StringIO import StringIO
from pprint import pprint

mint.login(config.USERNAME, config.PASSWORD)
pprint(mint.get_account_summaries())
pprint(mint.get_transactions())
for row in csv.reader(StringIO(mint.get_transactions_csv())):
  pprint(row)
