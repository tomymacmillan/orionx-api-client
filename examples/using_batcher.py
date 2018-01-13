from orionxapi.connection_manager import batch_client, as_completed
from gql import gql


client = batch_client(headers_filename='cache/headers.json',
                cookies_filename='cache/cookies.json')

results = []
# marketOrderBook
query = gql('''
  query getOrderBook($marketCode: ID!) {
    orderBook: marketOrderBook(marketCode: $marketCode, limit: 50) {
      buy {
        limitPrice
        amount
        __typename
      }
      sell {
        limitPrice
        amount
        __typename
      }
      spread
      __typename
    }
  }
''')

params = {
  "marketCode": "CHACLP"
}

operation_name = "getOrderBook"

results.append(client.execute(query, variable_values=params))

# marketStats
query = gql('''
  query getMarketStats($marketCode: ID!, $aggregation: MarketStatsAggregation!) {
    marketStats(marketCode: $marketCode, aggregation: $aggregation) {
      _id
      open
      close
      high
      low
      volume
      count
      fromDate
      toDate
      __typename
    }
  }
''')

params = {
  "marketCode": "CHACLP",
  "aggregation": "h1"
}

operation_name = "getMarketStats"

results.append(client.execute(query, variable_values=params))

# market
query = gql('''
  query getMarketIdleData($code: ID) {
    market(code: $code) {
      code
      lastTrade {
        price
        __typename
      }
      secondaryCurrency {
        code
        units
        format
        longFormat
        __typename
      }
      __typename
    }
  }
''')

params = {
  "code": "CHACLP"
}

operation_name = "getMarketIdleData"

results.append(client.execute(query, variable_values=params))

for result in as_completed(results):
  if result.errors:
    print("error:", result.errors[0])
  else:
    print('data:', result.data)