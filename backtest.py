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
        self.account = {"balance": self.initial_balance, ""}
        self.trading_log =  {"open_price": [], ""}

    def update_account(self):
        pass

    def OpenBuy(self, price, ammount):
        pass

    def CloseBuy(self):
        pass

    def OpenSell(self):
        pass

    def CloseSell(self):
        pass
