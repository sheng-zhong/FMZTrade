import pandas as pd

class Exchange:

    def __init__(self, trade_symbols, leverage=20, commission=0.00005, initial_balance=10000, log=True):
        self.initial_balance = initial_balance  # 初始的资产
        self.commission = commission
        self.leverage = leverage
        self.trade_symbols = trade_symbols
        self.date = ''
        self.log = log
        self.df = pd.DataFrame(columns=['margin', 'total', 'leverage', 'realised_profit', 'unrealised_profit'])
        self.account = {'USDT': {'realised_profit': 0, 'margin': 0, 'unrealised_profit': 0, 'total': initial_balance,
                                 'leverage': 0}}
        for symbol in trade_symbols:
            self.account[symbol] = {'amount': 0, 'hold_price': 0, 'value': 0, 'price': 0, 'realised_profit': 0,
                                    'margin': 0, 'unrealised_profit': 0}

    def Trade(self, symbol, direction, price, amount, msg=''):
        if self.date and self.log:
            print('%-20s%-5s%-5s%-10.8s%-8.6s %s' % (
            str(self.date), symbol, 'buy' if direction == 1 else 'sell', price, amount, msg))

        cover_amount = 0 if direction * self.account[symbol]['amount'] >= 0 else min(
            abs(self.account[symbol]['amount']), amount)
        open_amount = amount - cover_amount

        self.account['USDT']['realised_profit'] -= price * amount * self.commission  # 扣除手续费

        if cover_amount > 0:  # 先平仓
            self.account['USDT']['realised_profit'] += -direction * (
                        price - self.account[symbol]['hold_price']) * cover_amount  # 利润
            self.account['USDT']['margin'] -= cover_amount * self.account[symbol]['hold_price'] / self.leverage  # 释放保证金

            self.account[symbol]['realised_profit'] += -direction * (
                        price - self.account[symbol]['hold_price']) * cover_amount
            self.account[symbol]['amount'] -= -direction * cover_amount
            self.account[symbol]['margin'] -= cover_amount * self.account[symbol]['hold_price'] / self.leverage
            self.account[symbol]['hold_price'] = 0 if self.account[symbol]['amount'] == 0 else self.account[symbol][
                'hold_price']

        if open_amount > 0:
            total_cost = self.account[symbol]['hold_price'] * direction * self.account[symbol][
                'amount'] + price * open_amount
            total_amount = direction * self.account[symbol]['amount'] + open_amount

            self.account['USDT']['margin'] += open_amount * price / self.leverage
            self.account[symbol]['hold_price'] = total_cost / total_amount
            self.account[symbol]['amount'] += direction * open_amount
            self.account[symbol]['margin'] += open_amount * price / self.leverage

        self.account[symbol]['unrealised_profit'] = (price - self.account[symbol]['hold_price']) * self.account[symbol][
            'amount']
        self.account[symbol]['price'] = price
        self.account[symbol]['value'] = abs(self.account[symbol]['amount']) * price

        return True

    def Buy(self, symbol, price, amount, msg=''):
        self.Trade(symbol, 1, price, amount, msg)

    def Sell(self, symbol, price, amount, msg=''):
        self.Trade(symbol, -1, price, amount, msg)

    def Update(self, date, close_price):  # 对资产进行更新
        self.date = date
        self.close = close_price
        self.account['USDT']['unrealised_profit'] = 0
        for symbol in self.trade_symbols:
            if np.isnan(close_price[symbol]):
                continue
            self.account[symbol]['unrealised_profit'] = (close_price[symbol] - self.account[symbol]['hold_price']) * \
                                                        self.account[symbol]['amount']
            self.account[symbol]['price'] = close_price[symbol]
            self.account[symbol]['value'] = abs(self.account[symbol]['amount']) * close_price[symbol]
            self.account['USDT']['unrealised_profit'] += self.account[symbol]['unrealised_profit']
            if self.date.hour in [0, 8, 16]:
                pass
                self.account['USDT']['realised_profit'] += -self.account[symbol]['amount'] * close_price[
                    symbol] * 0.01 / 100

        self.account['USDT']['total'] = round(
            self.account['USDT']['realised_profit'] + self.initial_balance + self.account['USDT']['unrealised_profit'],
            6)
        self.account['USDT']['leverage'] = round(self.account['USDT']['margin'] / self.account['USDT']['total'],
                                                 4) * self.leverage
        self.df.loc[self.date] = [self.account['USDT']['margin'], self.account['USDT']['total'],
                                  self.account['USDT']['leverage'], self.account['USDT']['realised_profit'],
                                  self.account['USDT']['unrealised_profit']]


kongtou_trade_list = []
duotou_trade_list = []

    ticker = exchange.GetTicker()
    price = ticker['Last']
    if (price >= mid_price) and (price < max_price):  # 空头
        if len(kongtou_trade_list) > 0:
            last_trade = kongtou_trade_list[-1]
            if price - last_trade['open_price'] >= net_price:  # 开空
                exchange.SetDirection("sell")
                exchange.Sell(price - 10, net_position)
                Log("[== 开空头仓 ==]: 开仓价格：{}   网格id：{}".format((price+0.2), len(kongtou_trade_list)))
                kongtou_trade_list.append({"open_price: ": (price + 0.2),
                                           "net_id: ": len(kongtou_trade_list),
                                           "direction: ": "kong"})
            if last_trade['open_price'] - price > net_price:  # 平空
                exchange.SetDirection("closesell")
                exchange.Buy((price+0.2), net_position)
                Log("[== 平空头仓 ==]：平仓价格：{}   网格id：{}".format((price+0.2), len(kongtou_trade_list)))
                del kongtou_trade_list[-1]
        if len(kongtou_trade_list) == 0:
            if (price - mid_price) > net_price:
                exchange.SetDirection("sell")
                exchange.Sell(price - 0.2, net_position)
                Log("[== 开空头仓 ==]: 开仓价格：{}   网格id：{}".format((price-0.2), len(kongtou_trade_list)))

    if (price < mid_price) and (price > min_price):  # 多头
        if len(duotou_trade_list) > 0:
            last_trade = duotou_trade_list[-1]
            if last_trade['open_price'] - price >= net_price:  # 开多
                exchange.SetDirection("buy")
                exchange.Buy(price+0.2, net_position)
                Log("[== 开多头仓 ==]: 开仓价格：{}   网格id：{}".format((price+0.2), len(duotou_trade_list)))
                duotou_trade_list.append({"open_price: ": (price + 0.2),
                                           "net_id: ": len(duotou_trade_list),
                                           "direction: ": "duo"})
            if price - last_trade['open_price'] > net_price:  # 平多
                exchange.SetDirection("closebuy")
                exchange.Sell(price-0.2, net_position)
                Log("[== 平多头仓 ==]：平仓价格：{}   网格id：{}".format((price-0.2), len(duotou_trade_list)))
                del duotou_trade_list[-1]
        if len(duotou_trade_list) == 0:
            if (mid_price - price) > net_price:
                exchange.SetDirection("buy")
                exchange.Buy(price+0.2, net_position)
                Log("[== 开多头仓 ==]: 开仓价格：{}   网格id：{}".format((price+0.2), len(duotou_trade_list)))

    if (price > max_price) or (price < min_price):
        Log("[-- 价格已经突破了区间，所有仓位都将平掉。程序也将退出 --]")
        if len(kongtou_trade_list) > 0:
            exchange.SetDirection("closesell")
            exchange.Buy((price + 10), net_position*len(kongtou_trade_list))
        if len(duotou_trade_list) > 0:
            exchange.SetDirection("closebuy")
            exchange.Sell(price - 10, net_position*len(duotou_trade_list))
        sys.exit(0)