### IMPORTS

from tradersbot import TradersBot
import math
import time
import argparse
import scipy.optimize
import matplotlib.pyplot as plt
from scipy.stats import norm

### TRADERSBOT INITIALIZATION

parser = argparse.ArgumentParser(description='Run a TradersBot')
parser.add_argument('--addr', help='IP/URL', default='127.0.0.1')
parser.add_argument('--user', help='Username', default='trader0')
parser.add_argument('--pw', help='Password', default='trader0')
args = parser.parse_args()

t = TradersBot(args.addr, args.user, args.pw)

### GLOBAL VARIABLES

case_meta = {}
orderbook = {}
total_time = 450
elapsed_time = 0
implied_vols = {'T100C': 1, 'T110P': 1, 'T105C': 1, 'T105P': 1, 'T110C': 1,
                'T110P': 1, 'T90C': 1, 'T95C': 1, 'T95P': 1}
implied_vols = {ticker: 0.5 for ticker in implied_vols.keys()}
last_vol_update = time.time()

### CALLBACKS

## onAckRegister

def load_case(msg, TradersOrder):
    global case_meta, orderbook
    print('Connected!')
    case_meta = msg['case_meta']
    securities = case_meta['securities']
    orderbook = {key: {'bids': {},
                       'asks': {},
                       'tradeable': securities[key]['tradeable'],
                       'underlyings': securities[key]['underlyings'],
                       'last_price': securities[key]['starting_price']} for key in securities}

t.onAckRegister = load_case

## onAckModifyOrders

## onNews

## onMarketUpdate

def black_scholes(sig, call_or_put, S, K, t, option_price):
    K = float(K)
    d1 = (math.log(S/K) + (sig**2)/2 * t)/(sig * t**0.5)
    d2 = d1 - sig * (t**0.5)
    C = norm.cdf(d1)*S - norm.cdf(d2)*K
    if call_or_put == 'C':
        return C - option_price
    else:
        return C + K - S - option_price


def black_scholes_derivative(sig, call_or_put, S, K, t, option_price):
    K = float(K)
    d1 = (math.log(S/K) + (sig**2)/2 * t)/(sig * t**0.5)
    d2 = d1 - sig * (t**0.5)
    d1_derivative = (t**0.5)/2 - (math.log(S/K)/(t**0.5)) * (1/sig**2)
    d2_derivative = d1_derivative - t**0.5
    return norm.pdf(d1) * S * d1_derivative - norm.pdf(d2) * K * d2_derivative


def plot_vol_curves():
    global implied_vols
    puts = []
    put_vols = []
    calls = []
    call_vols = []
    for ticker in implied_vols:
        put_or_call = ticker[len(ticker) - 1]
        strike = int(ticker[1:len(ticker)-1])
        if put_or_call == 'P':
            puts.append(strike)
            put_vols.append(implied_vols[ticker]*100)
        else:
            calls.append(strike)
            call_vols.append(implied_vols[ticker]*100)
    plt.plot(puts, put_vols)
    plt.savefig('./put_plot.png')
    plt.clf()
    plt.plot(calls, call_vols)
    plt.savefig('./call_plot.png')
    plt.clf()
    log = open('options_log.txt', 'a')
    log.write(implied_vols)
    log.write('\n')
    log.close()


def calculate_implied_volatility():
    global orderbook, implied_vols, elapsed_time, total_time, last_vol_update
    if time.time() - last_vol_update < 3:
        return
    spot_price = orderbook['TMXFUT']['last_price']
    time_left = (total_time - elapsed_time)/float(total_time)
    for ticker in implied_vols:
        call_or_put = ticker[len(ticker)-1]
        strike_price = int(ticker[1:len(ticker)-1])
        option_price = orderbook[ticker]['last_price']
        # estimate implied vol with newton's method
        try:
            implied_vol = scipy.optimize.newton(black_scholes, 0.5, black_scholes_derivative, args=(call_or_put, spot_price, strike_price, time_left, option_price), maxiter=200, tol=0.01)
            if implied_vol >= 0 and implied_vol <= 1:
                implied_vols[ticker] = implied_vol
        except RuntimeError:
            continue
    plot_vol_curves()
    last_vol_update = time.time()


def market_update(msg, TradersOrder):
    global orderbook, elapsed_time
    elapsed_time = msg['elapsed_time']
    market_state = msg['market_state']
    ticker = market_state['ticker']
    orderbook[ticker]['bids'] = market_state['bids']
    orderbook[ticker]['asks'] = market_state['asks']
    orderbook[ticker]['last_price'] = market_state['last_price']
    calculate_implied_volatility()

t.onMarketUpdate = market_update

## onTraderUpdate

## onTrade

### RUN BOT

t.run()
