'''
start: 2019-08-28 00:00:00
end: 2019-09-26 00:00:00
period: 1H
exchanges: [{"eid":"OKEX","currency":"BTC_USDT","stocks":0}]
'''
#上面注释是回测设置

from fmz import *
task = VCtx(__doc__)
import talib as TA
import time

# params = type('obj', (object,), {"MACD_range": "12", "RSI_range": "12", "EMA_range": "22",
#                                 "BOLL_range": "20", "middle_range": PERIOD_M15, "long_range": PERIOD_M75})
# 多头代号1，空头代号0

def calculate_limit():
    # 计算止盈止损price_limit
    pass

def manage_account():
    # 仓位管理功能，计算开仓数量、资金划转
    pass

def account_station():
    # 如果持有仓位，持续观察价格变化是否达到止盈止损

    # 多头止盈 -- 15m线的KDJ读数超过70
    # 多头止损 -- 止损位置一： 交易当天或前一天的低价
    #            止损位置二： 损益两平的价格
    #            止损位置三、四。。。： 保护50%的账面获利
    # 空头止盈 -- 15m线的KDJ读数小于20
    # 空头止损 -- 止损位置一： 交易当天或前一天的最高价
    #            止损位置二： 损益两平的价格
    #            止损位置三、四。。。： 保护50%的账面获利
    pass

def second_filter(direction):
    # 根据EMA22、BOLL、RSI获取中介时间节点的入场机会

    # 设置期货杠杆大小、合约类型（永续）
    exchange.SetMarginLevel(2)
    exchange.SetContractType("swap")

    counter = 1
    while True:
        r = exchange.GetRecords(PERIOD_M10)
        rsi = TA.RSI(r, 1)
        ticker = exchange.GetTicker()
        if direction:
            # 多头吃单交易
            if rsi < 20:
                # 吃单，开2张多头
                exchange.SetDirection("buy")
                id = exchange.Buy(ticker['Last'] + 10, 2)
                Log("[+] 多头开仓成功： ", id)
                break
        else:
            # 空头吃单交易
            if rsi > 80:
                # 吃单，开2张空头
                exchange.SetDirection("sell")
                id = exchange.Sell(ticker['Last'] + 10, 2)
                Log("[+] 空头开仓成功： ", id)
                break
        Sleep(10)
    price_limit = calculate_limit()
    return price_limit

def first_filter(before_midLine, before_ma):
    # 判断长期趋势 -- MA和BOLL
    recoders = exchange.GetRecords(PERIOD_M30)
    ma = TA.MA(recoders, 14)
    if recoders and len(recoders) > 20:
        boll = TA.BOLL(recoders, 20, 2)
        boll_midLine = boll[1]
        if boll_midLine > before_midLine and ma > before_ma: # 长期多
            Log("[50min趋势]： 向上，开始在10min级别寻找交易机会！")
            # trade_result = second_filter(1)
            # Log("[交易结果]: {}".format(trade_result))
        elif boll_midLine < before_midLine and ma < before_ma: # 长期空
            Log("[50min趋势]： 向下，开始在10min级别寻找交易机会！")
            # trade_result = second_filter(0)
            # Log("[交易结果]: {}".format(trade_result))
        else:
            Log("[50min趋势]， 趋势难以判断，等待机会。")
    else:
        Log("[-- 数据量不足以计算BOLL数值，等待中 --]")
        ma = -1
        boll_midLine = -1
    return ma, boll_midLine

flag = 1
while True:
    if flag:
        now_midLine, now_ma = first_filter(0, 0)
        flag = False
    else:
        now_midLine, now_ma = first_filter(now_midLine, now_ma)
    time.sleep(3)