### IMPORTS

from tradersbot import TradersBot
import argparse
import time

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
cash = {'USD': 100000, 'JPY': 0, 'EUR': 0, 'CHF': 0, 'CAD': 0}
cycles = [['EURCHF', 'CHFJPY', 'EURJPY'], ['USDCAD', 'EURUSD', 'EURCAD'], ['CHFJPY', 'USDCHF', 'USDJPY']]
time_last_order = time.time() # prevent order overflow
time_last_clear = time.time()
arb_threshold = 0.005
pnl_deltas = [0 for _ in range(10)]
current_pnl = 1
transaction_fee = 0.0001

### FLAGS

DELTASHIFT = 1

### HELPER FUNCTIONS

# Arbitrage opportunity?
def check_cycle(cycle):
    global orderbook, arb_threshold
    bids = [orderbook[ticker]['bids'] for ticker in cycle]
    asks = [orderbook[ticker]['asks'] for ticker in cycle]
    for i in range(3):
        bids_dict = bids[i]
        max_bid = 0
        order_size = 0
        if bids_dict == {}: # no updates
            return ('NO', 0)
        for bid, sz in bids_dict.items():
            if float(bid) > max_bid:
                max_bid, order_size = float(bid), sz
        bids[i] = (max_bid, order_size)
    for i in range(3):
        asks_dict = asks[i]
        min_ask = 1000
        order_size = 0
        for ask, sz in asks_dict.items():
            if float(ask) < min_ask:
                min_ask, order_size = float(bid), sz
        asks[i] = (min_ask, order_size)

    # print(bids[0][0] * bids[1][0]/asks[2][0])
    # print(asks[0][0] * asks[1][0]/bids[2][0])
    if ((bids[0][0] + transaction_fee) * (bids[1][0] + transaction_fee)/(asks[2][0] + transaction_fee)) < 1 - arb_threshold:
        sz = min(bids[0][1], bids[1][1], asks[2][1])
        if sz >= 10:
            # print('Buy ' + cycle[0] + ' ' + cycle[1] + ', Sell ' + cycle[2])
            return ('BUY', bids[0][0], bids[1][0], asks[2][0], sz)
        else:
            return ('NO', 0)
    elif ((asks[0][0] + transaction_fee) * (asks[1][0] + transaction_fee)/(bids[2][0] + transaction_fee)) > 1 + arb_threshold:
        sz = min(asks[0][1], asks[1][1], bids[2][1])
        if sz >= 10:
            # print('Sell ' + cycle[0] + ' ' + cycle[1] + ', Buy ' + cycle[2])
            return ('SELL', asks[0][0], asks[1][0], bids[2][0], sz)
        else:
            return ('NO', 0)
    else:
        return ('NO', 0)


### CALLBACKS

## onAckRegister

def load_case(msg, TradersOrder):
    global case_meta, orderbook
    print('Connected!')
    case_meta = msg['case_meta']
    securities = case_meta['securities'].keys()
    orderbook = {ticker: {'bids': {}, 'asks': {}, 'last_price': case_meta['securities'][ticker]['starting_price'], 'time': 0} for ticker in securities}

t.onAckRegister = load_case

## onAckModifyOrders

def order_confirmation(msg, TradersOrder):
    # print('Order accepted!')
    return

t.onAckModifyOrders = order_confirmation

## onNews

## onMarketUpdate

def market_update(msg, TradersOrder):
    global orderbook, time_last_order
    market_state = msg['market_state']
    ticker = market_state['ticker']
    orderbook[ticker]['bids'] = market_state['bids']
    orderbook[ticker]['asks'] = market_state['asks']
    orderbook[ticker]['last_price'] = market_state['last_price']
    orderbook[ticker]['time'] = market_state['time']
    if (time.time() - time_last_order < 1):
        return
    for cycle in cycles:
        resp = check_cycle(cycle)
        if resp[0] == 'BUY':
            order_size = resp[4]
            TradersOrder.addBuy(cycle[0], order_size)#, price=resp[1])
            TradersOrder.addBuy(cycle[1], order_size)#, price=resp[2])
            TradersOrder.addSell(cycle[2], order_size)#, price=resp[3])
            time_last_order = time.time()
        elif resp[0] == 'SELL':
            order_size = resp[4]
            TradersOrder.addSell(cycle[0], order_size)#, price=resp[1])
            TradersOrder.addSell(cycle[1], order_size)#, price=resp[2])
            TradersOrder.addBuy(cycle[2], order_size)#, price=resp[3])
            time_last_order = time.time()
    return

t.onMarketUpdate = market_update

## onTraderUpdate

def cancel_old_orders(msg, TradersOrder):
    global orderbook, time_last_clear, current_pnl, pnl_deltas, arb_threshold, DELTASHIFT
    counter = 0
    # clear 10 old orders every 3 seconds
    if (time.time() - time_last_clear > 3):
       if 'open_orders' in msg:
            for order in msg['open_orders']:
                if counter > 10:
                    break
                order_id = order.split(':')
                ticker = order_id[0]
                id_num = order_id[1]
                TradersOrder.addCancel(ticker, id_num)
                counter += 1
            print('Orders cleared!')
    time_last_clear = time.time()
    if current_pnl != 0:
        pnl_deltas.append((msg['trader_state']['default_pnl'] - current_pnl)/current_pnl)
    else:
        pnl_deltas.append(0)
    pnl_deltas = pnl_deltas[1:]
    avg_delta = sum(pnl_deltas)/10
    current_pnl = msg['trader_state']['default_pnl']
    if DELTASHIFT == 1:
        if avg_delta < .005 and avg_delta > -0.005:
            # not making enough money, narrow in
            arb_threshold /= 2
            print(arb_threshold)
        if avg_delta < -.005:
            # losing too much money, push out
            arb_threshold *= 2
            print(arb_threshold)

t.onTraderUpdate = cancel_old_orders

## onTrade

def update_orderbook(msg, TradersOrder):
    global orderbook

### RUN BOT

t.run()
