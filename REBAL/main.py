import pandas as pd
import numpy as np
import os
from colorama import Fore, Back, Style

print(os.getcwd())
#Stock Prices From Top Ten From Vanguard 500 Index Fund (VFINX) As of Market Open 7/20/2018
#Read-in data from .csv
data = pd.read_csv('./REBAL/marketData.csv', index_col = 0)
df = pd.DataFrame(data)
stockList = list(df.index)


# Initialize portfolio to 0 across the board
#   STOCK  |      Quantity     |  Balance  |   Percent   |
portfolio_AAPL = [0, 0, 0]
portfolio_MSFT = [0, 0, 0]
portfolio_AMZN = [0, 0, 0]
portfolio_GOOGL = [0, 0, 0]
portfolio_FB = [0, 0, 0]
portfolio_BRKA = [0, 0, 0]
portfolio_JPM = [0, 0, 0]
portfolio_XOM = [0, 0, 0]
portfolio_JNJ = [0, 0, 0]
portfolio_BAC = [0, 0, 0]
# Structure: {STOCK : [QTY, BALANCE, PERCENT], ...}
my_Portfolio = {"AAPL":portfolio_AAPL, "MSFT":portfolio_MSFT, "AMZN":portfolio_AMZN, "GOOGL":portfolio_GOOGL, "FB":portfolio_FB, "BRKA":portfolio_BRKA, "JPM":portfolio_JPM, "XOM":portfolio_XOM, "JNJ":portfolio_JNJ, "BAC":portfolio_BAC}

# Randomly calculate a Portfolio
# Total Assets of $150,000
randoms = {"AAPL":0, "MSFT":0, "AMZN":0, "GOOGL":0, "FB":0, "BRKA":0, "JPM":0, "XOM":0, "JNJ":0, "BAC":0}
sum_randoms = 0
sum_stocks = 0

# Lets assign a random holding percentage for each stock
for stock in my_Portfolio:
  randoms[stock] = np.random.random()
  sum_randoms += randoms[stock]

# we are going to pull-in the global-scope 'sum_stocks' and 
# 'my_Portfolio' variables and then operate on them to calculate
# a random example portfolio totaling $150,000.
def verifyRatios():
  global sum_stocks
  global randoms
  global sum_randoms
  # print("RANDOM ANOMALY ERROR - PLEASE RESTART")
  for stock in my_Portfolio:
    sum_stocks += randoms[stock]/sum_randoms

# Loop through the created mock Index and print it out to the console
def displayIndex():
  global df
  global stockList
  total_QTY = 0
  total_BAL = 0
  total_PER = 0
  print()
  print(Fore.MAGENTA + "Index Benchmark")
  print(Fore.WHITE)
  print("{:^5}|{:^10}|{:^14}|{:^19}|".format("STOCK","QUANTITY","BALANCE","HOLDING PERCENT"))
  print("----------------------------------------------------")
  for stock in stockList:
    total_PER += df['PER'][stock]
    total_BAL += df['BAL'][stock]
    total_QTY += df['QTY'][stock]
    print("{:5}|{:10.2f}|${:13,.2f}|{:19.2f}|".format(stock,df['QTY'][stock],df['BAL'][stock],df['PER'][stock]*100))
  print("----------------------------------------------------")
  print(Fore.GREEN + "{:^5}|{:10.2f}|${:13,.2f}|{:19.2f}|".format("TOTAL",total_QTY,total_BAL,total_PER*100))

# Utilize the calculated random percents to calulate the rest of the values
# for each stock in the portfolio
def calculatePortfolio():
  global sum_stocks
  global my_Portfolio
  global randoms
  global sum_randoms
  total_QTY = 0
  total_BAL = 0
  total_PER = 0
  print(Fore.WHITE)
  print(Fore.MAGENTA + "Random Generated Portfolio")
  print(Fore.WHITE)
  print("{:^5}|{:^10}|{:^14}|{:^19}|".format("STOCK","QUANTITY","BALANCE","PORTFOLIO PERCENT"))
  print("----------------------------------------------------")
  for stock in my_Portfolio:
    my_Portfolio[stock][2] = randoms[stock]/sum_randoms
    total_PER += my_Portfolio[stock][2]
    my_Portfolio[stock][1] = float(my_Portfolio[stock][2])*150000
    total_BAL += my_Portfolio[stock][1]
    my_Portfolio[stock][0] = float(my_Portfolio[stock][1])/df['PRICE'][stock]
    total_QTY += my_Portfolio[stock][0]
    print("{:5}|{:10.2f}|${:13,.2f}|{:19.2f}|".format(stock,my_Portfolio[stock][0],my_Portfolio[stock][1],my_Portfolio[stock][2]*100))
  print("----------------------------------------------------")
  print(Fore.GREEN + "{:^5}|{:10.2f}|${:13,.2f}|{:19.2f}|".format("TOTAL",total_QTY,total_BAL,total_PER*100))

  # Loop through the generated portfolio and print it out to the console
def displayPortfolio():
  global my_Portfolio
  total_QTY = 0
  total_BAL = 0
  total_PER = 0
  print(Fore.WHITE)
  print(Fore.MAGENTA + "Rebalanced Portfolio")
  print(Fore.WHITE)
  print("{:^5}|{:^10}|{:^14}|{:^19}|".format("STOCK","QUANTITY","BALANCE","PORTFOLIO PERCENT"))
  print("----------------------------------------------------")
  for stock in my_Portfolio:
    total_PER += my_Portfolio[stock][2]
    total_BAL += my_Portfolio[stock][1]
    total_QTY += my_Portfolio[stock][0]
    print("{:5}|{:10.2f}|${:13,.2f}|{:19.2f}|".format(stock,my_Portfolio[stock][0],my_Portfolio[stock][1],my_Portfolio[stock][2]*100))
  print("----------------------------------------------------")
  print(Fore.GREEN + "{:^5}|{:10.2f}|${:13,.2f}|{:19.2f}|".format("TOTAL",total_QTY,total_BAL,total_PER*100))

# Negative values in reconciliation[] imply a need to sell
# a security from the portfolio. Positive values, therefore, 
# imply a need to buy a security. Zero vlaues mean that there
# is no tracking error
def reconcilePortfolio():
  # PER - [0] - Percent reconciliation
  # BAL - [1] - Balance (cash) reconciliation
  # QTY - [2] - Quantity (shares) reconciliation
  reconciliation = {"AAPL":[0,0,0], "MSFT":[0,0,0], "AMZN":[0,0,0], "GOOGL":[0,0,0], "FB":[0,0,0], "BRKA":[0,0,0], "JPM":[0,0,0], "XOM":[0,0,0], "JNJ":[0,0,0], "BAC":[0,0,0]}
  global df
  global my_Portfolio

  for stock in my_Portfolio:
    # Need to buy security
    if df['PER'][stock] > my_Portfolio[stock][2]:
      reconciliation[stock][0] = abs(my_Portfolio[stock][2] - df['PER'][stock])
      reconciliation[stock][1] = abs((my_Portfolio[stock][2] - df['PER'][stock])*150000)
      reconciliation[stock][2] = abs((my_Portfolio[stock][2] - df['PER'][stock])*150000/df['PRICE'][stock])
    # Need to sell security
    elif df['PER'][stock] < my_Portfolio[stock][2]:
      reconciliation[stock][0] = df['PER'][stock] - my_Portfolio[stock][2]
      reconciliation[stock][1] = (df['PER'][stock] - my_Portfolio[stock][2])*150000
      reconciliation[stock][2] = (df['PER'][stock] - my_Portfolio[stock][2])*150000/df['PRICE'][stock]
    # Already balanced
    else:
      reconciliation[stock][0] = 0
      reconciliation[stock][1] = 0
      reconciliation[stock][2] = 0
  # We want to sort the list of reconciliations from smallest to largest percent/PER/[0].
  # We want to do this so that when the rebalancing starts, it sells before it buys.
  # This is to avoid excess funding being required during the rebalance.
  # We can do this with itemgetter() or lambda
  # OR sorted(reconciliation.items(), key=itemgetter(1))
  reconciliation = sorted(reconciliation.items(), key=lambda k: k[1][0])
  return reconciliation

def rebalancePortfolio():
  global my_Portfolio
  global reconciled
  cash = 0
  print(Fore.WHITE)
  print(Fore.MAGENTA + "REBALANCING INITIATED")
  print(Fore.WHITE)
  for stock in reconciled:
    print()
    if stock[1][0] < 0:
      # Print a message explaining the action taken to correct an overweighted outlier
      # Absolute value taken to show quanity not direction
      print(Fore.CYAN + "Since " + stock[0] + " is overweighted in our portfolio by " + "%.2f" % (abs(stock[1][0]*100)) + "%, we need to sell " + "%.2f" % (abs(stock[1][2])) + " shares, totaling " + "${:,.2f}".format(abs(stock[1][1])) + ".")
      # Plus Equals because these values are negative
      # Update Quantity - my_Portfolio[stock][0] & reconciled[stock][2]
      my_Portfolio[stock[0]][0] += stock[1][2]
      # Update Balance - my_Portfolio[stock][1] & reconciled[stock][1]
      my_Portfolio[stock[0]][1] += stock[1][1]
      # Update Percent - my_Portfolio[stock][2] & reconciled[stock][0]
      my_Portfolio[stock[0]][2] += stock[1][0]
      cash += abs(stock[1][1])
    elif stock[1][0] > 0:
      # Print a message explaining the action taken to correct an underweighted outlier
      print(Fore.CYAN + "Since " + stock[0] + " is underweighted in our portfolio by " + "%.2f" % (stock[1][0]*100) + "%, we need to buy " + "%.2f" % (stock[1][2]) + " shares, totaling " + "${:,.2f}".format(stock[1][1]) + ".")
      # Update Quantity - my_Portfolio[stock][0] & reconciled[stock][2]
      my_Portfolio[stock[0]][0] += stock[1][2]
      # Update Balance - my_Portfolio[stock][1] & reconciled[stock][1]
      my_Portfolio[stock[0]][1] += stock[1][1]
      # Update Percent - my_Portfolio[stock][2] & reconciled[stock][0]
      my_Portfolio[stock[0]][2] += stock[1][0]
      cash -= stock[1][1]
    else:
      # Print a message explaining no action taken
      print(Fore.CYAN + "Since " + stock[0] + " matches the weighting in the Index, no action is necessary.")
    print(Fore.WHITE)
    input(Fore.YELLOW + "Press Enter to execute this rebalance...")
    displayPortfolio()
    print(Fore.WHITE)
    print("Money Market Balance: " + Fore.GREEN + "${:,.2f}".format(cash))
    print(Fore.WHITE)
    input(Fore.YELLOW + "Press Enter to continue rebalancing...")
    print(Fore.WHITE)

# sum_stocks should be 1.0 for a perfectly distibuted portfolio
# due to the random function, we may get just below or just above
# this from time to time. Let's make sure our ratios add to 100% or 1.0.
# we will do this by recalculating until this is true.
while True:
  if sum_stocks == 1.0:
    break
  else:
    verifyRatios()
displayIndex()
print()
calculatePortfolio()
print()
reconciled = reconcilePortfolio()
input(Fore.YELLOW + "Press Enter to start rebalancing...")
rebalancePortfolio()
displayIndex()
print()
print(Fore.WHITE + "The portfolio is now rebalanced to match the weights within the given Index.")