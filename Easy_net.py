'''backtest
start: 2015-02-22 00:00:00
end: 2019-12-06 00:00:00
period: 1h
exchanges: [{"eid":"Futures_OKCoin","currency":"BTC_USD"}]
'''
import sys
from fmz import *
task = VCtx(__doc__)

init_counter = exchange.GetPosition()[0]
max_price = 7000
min_price = 6000
mid_price = min_price + (max_price - min_price)/2
net_sum = 20
net_price = ((max_price - min_price)/2)/net_sum
net_position = (init_counter * 3) / (100 * net_sum)
if (max_price - min_price)/min_price > 0.2:
    print("[-- 价格区间设置错误，区间差价大于20% --]")
    sys.exit(0)
exchange.SetMarginLevel(5)
exchange.SetContractType("swap")

kongtou_trade_list = []
duotou_trade_list = []
while True:
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
    Sleep(1000*3)