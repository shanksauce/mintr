Mint.com API Client
===================
# Usage
See the __main__ code in mint.py. First decide how you will manage your Mint.com credentials. For instance, if you place them in a module called config, you might write:

```
import mint
mint.login(config.USERNAME, config.PASSWORD)
account_summaries = mint.get_account_summaries()
# etc...
```
