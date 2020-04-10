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

params = type('obj', (object,), {"MACD_range": "12", "RSI_range": "12", "EMA_range": "22",
                                 "BOLL_range": "20", "middle_range": PERIOD_M15, "long_range": PERIOD_M75})
# 多头代号1，空头代号0

def manage_account():
    # 仓位管理功能，计算开仓数量、资金划转
    pass

def account_station():
    # 如果持有仓位，持续观察价格变化是否达到止盈止损
    pass

def trade_chance(direction):
    # 根据RSI获取中介时间节点的入场机会

    # 设置期货杠杆大小、合约类型（永续）
    exchange.SetMarginLevel(10)
    exchange.SetContractType("swap")
    while True:
        r = exchange.GetRecords(PERIOD_M15)
        rsi = TA.RSI(r, 12)
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

def triple_net(recoders):
    # 判断长期趋势 -- macd和ema
    macd = TA.MACD(recoders, 12)
    if recoders and len(recoders) > 22:
        ema = TA.EMA(recoders, 22)
        if ema: # EMA多趋势判断标准
            Log("[EMA趋势]： 向上")
            if macd: # MACD多趋势判断标准
                Log("[MACD趋势]： 向上, 与EMA趋势判断相同！")
                Log("[== 开始寻找多头入场机会 ==]")
                trade_chance(1)
            else:
                Log("【-- MACD趋势判断与EMA相悖，等待机会 --】")

        if ema: # EMA空趋势判断标准
            Log("[EMA趋势]： 向下")
            if macd: # MACD空趋势判断标准
                Log("[MACD趋势]： 向下，与EMA趋势判断相同！")
                Log("[== 开始寻找空头入场机会 ==]")
                trade_chance(0)
            else:
                Log("【-- MACD趋势判断与EMA相悖，等待中 --】")
        else:
            Log("[-- EMA多空难以判断，等待中 --]")
    else:
        Log("[-- 数据量不足以计算EMA数值，等待中 --]")


while True:
    # 获取持仓信息
    position = exchange.GetPosition()
    if position
    recoders = exchange.GetRecords(PERIOD_M15)
    triple_net(recoders)
    Sleep(10)