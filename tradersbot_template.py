### IMPORTS

from tradersbot import TradersBot

### TRADERSBOT INITIALIZATION

t = TradersBot('127.0.0.1', 'trader0', 'trader0')

### GLOBAL VARIABLES

case_meta = {}

### CALLBACKS

## onAckRegister

def load_case(msg, TradersOrder):
    print('Connected!')
    case_meta = msg['case_meta']
    print(case_meta)

t.onAckRegister = load_case

## onAckModifyOrders

## onNews

## onMarketUpdate

## onTraderUpdate

## onTrade

### RUN BOT

t.run()
