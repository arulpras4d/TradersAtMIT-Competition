### IMPORTS

from tradersbot import TradersBot
import argparse

### TRADERSBOT INITIALIZATION

parser = argparse.ArgumentParser(description='Run a TradersBot')
parser.add_argument('--addr', help='IP/URL', default='127.0.0.1')
parser.add_argument('--user', help='Username', default='trader0')
parser.add_argument('--pw', help='Password', default='trader0')
args = parser.parse_args()

t = TradersBot(args.addr, args.user, args.pw)

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
