'''
start: 2019-08-28 00:00:00
end: 2019-09-26 00:00:00
period: 1H
exchanges: [{"eid":"OKEX","currency":"BTC_USDT","stocks":0}]
'''
#上面注释是回测设置

from fmz import * # 导入所有FMZ函数
task = VCtx(__doc__) # 初始化
'''
# 获取账户信息和时间
print(exchange.GetAccount())
print(_D())

# 获取行情
ticker = exchange.GetTicker()
print('最新成交价：', ticker['Last'])
print('当前时间  ：', _D())
ticker = exchange.GetTicker()
print('最新成交价：', ticker['Last'])
print('当前时间  ：', _D())
Sleep(1000*60*15)  # 15分钟
ticker = exchange.GetTicker()
print('最新成交价：', ticker['Last'])
print('当前时间  ：', _D())

# 获取K线图
records = exchange.GetRecords()
print('历史K线长度：', len(records))
print('最新K线：    ', records[len(records)-1])
print('最新K线时间: ', _D(records[len(records)-1]['Time']/1000))
'''
# ticker = exchange.GetTicker()
# print(ticker)
'''
# 订单未成交
id = exchange.Buy(ticker['Last']-10,0.1)
print(exchange.GetAccount())
print(exchange.GetOrder(id))
exchange.CancelOrder(id)
print(exchange.GetAccount())
'''
'''
# 订单成交
id = exchange.Buy(ticker['Last'] + 10, 0.1)
print(exchange.GetAccount())
print(exchange.GetOrder(id))
print(exchange.GetAccount())
'''

# 走进我的交易室 -- 计算价格通道
# 走进我的交易室 -- 计算
# 走进我的交易室 -- 计算
# 走进我的交易室 -- 计算

# 交易系统一 FROM 走进我的交易室
'''
三重过滤网交易系统：
  第一层滤网： 长期战略决策 -- 长期图表：30  MACD确定做空或者做多
  第二层滤网： 中介图表： 6min， 
              1、勾画一条22日EMA  描绘出一条相应价格通道（涵盖95%的行情价格）
              2、长期决策做多： EMA线以下根据RSI寻找相应入场点位
                 长期决策做空： EMA线以上根据RSI寻找相应入场点位
              3、设置止损单，关注收盘价。如果收盘价超出止损价位，就止损。
  第三层滤网： 确定进场和离场的实际操作方法 -- 在6min图的移动平均线附近
              价位进场。如果30min相关产品价格的走势向上，当6min价格柱形
              回调到指数均线附件时 + RSI呈现超卖状态 --》做多。降势之中
              反向操作即可。
在相关通道上轨设置止盈。
'''
# 交易系统二 FROM 走进我的交易室
'''
脉冲交易系统：
  1、做多需要所有指标都上指（30min行情趋势EMA上扬、6min行情趋势EMA和
     MACD两项指标同时给出买入信号。6min的MACD若掉头则立即平仓）
  2、做空则相反
'''
# 交易系统三 FROM 走进我的交易室
'''
三重过滤网系统 + 脉冲系统 
两个交易系统的反关联
'''

# 大趋势单边行情还是震荡行情判断 -- 市场晴雨表

'''
# 数字货币期货
# 获取仓位信息
exchange.GetPosition()
# 设置杠杆大小(10倍)
exchange.SetMarginLevel(10)
# 设置合约类型（永续合约）
exchange.SetContractType("swap")

# 交易下单
# 开多(10000价格， 2张)
exchange.SetDirection("buy")
exchange.Buy(10000, 2)
# 平多
exchange.SetDirection("closebuy")
exchange.Sell(10000, 2)

# 开空、平空
exchange.SetDirection("sell")
exchange.Sell(10000, 2)

exchange.SetDirection("closesell")
exchange.Buy(10000,2)

#
'''
records = exchange.GetRecords(PERIOD_M30)
print(records[9])