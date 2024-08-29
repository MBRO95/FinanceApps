# Created on Matthew’s iPad.
if __name__ == "__main__":
  import argparse
  import pandas as pd
  from datetime import date
  from typing import Dict, List, NewType
  today = date.today()
  parser = argparse.ArgumentParser(description='Calculate TLH Findings')
  portfolio = pd.read_csv('./Portfolio.csv',header=0)
  securities = portfolio["symbol"].unique().tolist()
  parser.add_argument('-s', '--security', nargs=1, choices=securities)
  args = parser.parse_args()
  # print(args.security)
  # print(securities)
  # print(portfolio)
  holdings = []
  if args.security == None:
    print("Must specify a security ticker with the -s or --security flag")
    exit()
  else:  
    holdings = portfolio.loc[portfolio["symbol"] == args.security[0]]

def generateLots(holdings : List) -> List:
  lots = []
  lotNumber = 1
  for index, row in holdings.iterrows():
    lotDetails = {}
    tradeDateString = str(row['trd_dt'])
    tradeDate = date(int(tradeDateString[0:4]),int(tradeDateString[4:6]),int(tradeDateString[6:8]))
    daysSinceTrade = today - tradeDate
    cost = float(row['purch_price']) * float(row['qty'])
    currentValue = float(row['cur_price']) * float(row['qty'])
    # print(daysSinceTrade)
    lotDetails["lot"] = lotNumber
    lotDetails["daysSinceTrade"] = daysSinceTrade.days
    lotDetails["cost"] = cost
    lotDetails["currentValue"] = currentValue
    lotNumber += 1
    lots.append(lotDetails)
  return lots

def washSaleCheck(days : int) -> bool:
  if days > 30:
    return False
  else:
    return True

def capitalGainsCheck(days : int, cost : float, value : float) -> Dict:
  capitalDetails = {}

  if days > 365:
    capitalDetails['capitalType'] = "LT"
  else:
    capitalDetails['capitalType'] = "ST"
  
  if value > cost:
    capitalDetails['capitalGain'] = True
    capitalDetails['capitalLoss'] = False
    capitalDetails['capitalValue'] = value - cost
  else:
    capitalDetails['capitalGain'] = False
    capitalDetails['capitalLoss'] = True
    capitalDetails['capitalValue'] = -abs(cost - value)
  return capitalDetails

def estimateHarvest(lots : List[Dict]) -> Dict:
  harvest = {}
  for lot in lots:
    lotDetails = {}
    if washSaleCheck(lot["daysSinceTrade"]):
      lotDetails['washSale'] = True
    else:
      lotDetails['washSale'] = False
      capitalDetails = capitalGainsCheck(lot["daysSinceTrade"], lot["cost"], lot["currentValue"])
      lotDetails['capitalGain'] = capitalDetails['capitalGain']
      lotDetails['capitalLoss'] = capitalDetails['capitalLoss']
      lotDetails['capitalType'] = capitalDetails['capitalType']
      lotDetails['capitalValue'] = capitalDetails['capitalValue']
    harvest[lot['lot']] = lotDetails
  return harvest

print(estimateHarvest(generateLots(holdings)))