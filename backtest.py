"""
交易回测引擎：
  初始化账户设置
  开仓：方向，数量，价格
    计算占用保证金
    更新账户
  平仓：方向，数量，价格
    计算盈利
    更新账户
"""
class BackTest(object):
    # 交易回测引擎
    def __init__(self, leverage=1, commission=0.00005, initial_balance=10000):
        self.leverage = leverage
        self.commission = commission
        self.initial_balance = initial_balance
        self.account = {"balance": self.initial_balance, "amount": 0, "profit": 0, "commission": 0}
        self.trading_log =  {"open_price": [], "direction": [], "close_price": [], "amount": [],
                             "profit": [], "commission": [], "margin": []}

    def update_account(self, price, direction, using_margin, amount, commissions, profit=0):
        self.account['balance'] = self.account['balance'] - using_margin - commissions
        self.account['amount'] = amount
        self.account['profit'] += profit
        self.account['commission'] += commissions
        self.trading_log['open_price'].append(price)
        self.trading_log['direction'].append(direction)
        self.trading_log['amount'].append(amount)
        self.trading_log['commission'].append(commissions)

    def OpenBuy(self, price, amount):
        using_margin = price * amount / self.leverage
        if self.account['balance'] >= using_margin:
            commissions = price * amount * self.commission
            self.update_account(price, direction, using_margin, amount, commissions)
        else:
            print("[-- 保证金不足，无法开仓 --]")

    def CloseBuy(self):
        pass

    def OpenSell(self):
        pass

    def CloseSell(self):
        pass
