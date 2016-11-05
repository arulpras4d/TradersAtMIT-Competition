### IMPORTS

from tradersbot import TradersBot
import argparse
import csv
import pandas as pd
import statsmodels.formula.api as smf
import math

### TRADERSBOT INITIALIZATION

parser = argparse.ArgumentParser(description='Run a TradersBot')
parser.add_argument('--addr', help='IP/URL', default='127.0.0.1')
parser.add_argument('--user', help='Username', default='trader0')
parser.add_argument('--pw', help='Password', default='trader0')
args = parser.parse_args()

t = TradersBot(args.addr, args.user, args.pw)

### GLOBAL VARIABLES

case_meta = {}
model = {}
res = {}
outcry_data = []
pred_counter = 1

### HELPER FUNCTIONS

def center_data(lst):
    # center data to mean 0, variance 1
    mean = sum(lst)/float(len(lst))
    lst = [x - mean for x in lst]
    var = sum([x**2 for x in lst])/float(len(lst))
    std = var**0.5
    lst = [x/std for x in lst]
    return lst

def linear_change(lst):
    # x_t - x_{t-1}
    change = [0]
    for i in range(1, len(lst)):
        change.append(lst[i] - lst[i-1])
    return change

def proportional_change(lst):
    # log(x_t) - log(x_{t-1})
    return_lst = []
    for x in lst:
        if x <= 0:
            return lst
        else:
            return_lst.append(math.log(x))
    return linear_change(return_lst)

### CALLBACKS

## onAckRegister

def load_case(msg, TradersOrder):
    global model, res, case_meta, outcry_data
    print('Connected!')
    case_meta = msg['case_meta']
    outcry_data = pd.read_csv('./outcry_data.csv')
    for name in outcry_data.columns:
        outcry_data[name] = proportional_change(outcry_data[name])
    model = smf.ols(formula = 'TAMIT ~ GDP + CPI + RS + HS + PPI + MTIS + U + MS + PI', data=outcry_data)
    res = model.fit()

t.onAckRegister = load_case

## onAckModifyOrders

## onNews

def get_data(msg, TradersOrder):
    global res, model, outcry_data, pred_counter
    news = msg['news']['body']
    news_items = news.split(';')
    news_items = [item.split() for item in news_items]
    names = [item[0] for item in news_items]
    numbers = [[float(item[4])] for item in news_items]
    reading = zip(names, numbers)
    reading = pd.DataFrame.from_items(reading)
    outcry_data = pd.concat([outcry_data, reading])
    model = smf.ols(formula = 'TAMIT ~ GDP + CPI + RS + HS + PPI + MTIS + U + MS + PI', data=outcry_data)
    res = model.fit()
    tamit_pred = res.predict(reading)
    logfile = open("outcry_log.txt", "a")
    logfile.write("Prediction " + str(pred_counter) + ": " + str(tamit_pred) + "\n")
    logfile.close()
    pred_counter += 1

t.onNews = get_data

## onMarketUpdate

## onTraderUpdate

## onTrade

### RUN BOT

t.run()
