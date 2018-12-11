import json
from oandapyV20 import API    # the client
import oandapyV20.endpoints.trades as trades

access_token = "101-004-9968359-001"
accountID = "6b6e99ca0c43b2e1bf31c26fd94f37a4-a17db531e4dd8b15e0bbc464cbadf809"
client = API(access_token=access_token)

# request trades list
r = trades.TradesList(accountID)
rv = client.request(r)
print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))

# # Oanda API setup
# accountid = "101-004-9968359-001"
# token = "6b6e99ca0c43b2e1bf31c26fd94f37a4-a17db531e4dd8b15e0bbc464cbadf809"

