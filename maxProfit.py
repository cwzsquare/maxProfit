from testSamples import *

# 来源于官方题解
# 思想：我们偷个懒，反正手里最多就持有一支股票，谁说手续费要卖出的时候再交呢？（暗示买的时候直接交了）
def greedy_maxProfit(prices, fee):
    prices = list(prices)
    profit = 0
    buy = prices[0] + fee  # 初始化买入时用的钱
    for price in prices[1:]:
        if price + fee < buy:
            buy = price + fee  # 不如第i天再买入
        elif price > buy:
            profit += price - buy  # 此时卖出，但不一定是最优，万一后边又涨了呢，没事，到时候再反悔，反正手续费已经交过了
            buy = price  # 更新buy就好，相当于这个时候再买入一遍
        else:
            pass  # 这天什么都不做，空过
    return profit


# 我的贪心思维题解
# 问如何贪到最多，就每一天、每一次交易都贪最多
# 假设前一次交易为A - B - fee，后一次为 C - D - fee，什么时候才需要进行这两次交易而非一次直接C - B - fee呢
# 答案是 A - B - fee + C - D - fee > C - B - fee，即 A > fee + D 才行
# 说人话就是，涨了能赚钱就抛，但有：
# ①卧槽，到了第二天，跌破了我的基准线，还好我昨天抛了。这时继续观望，顺便更新一下今天的基准线为今天的低价
# ②卧槽，到了第二天，涨的居然比我基准线对应的最高点还高，我要反悔；前一天抛了的不算，今天抛，既然已经抛了那就重新按标准改基准线
# ③其他情况就空过，反正今天不能贪最多，不亏或者不少赚就是成功
def greedy2_maxProfit(prices, fee):
    prices = list(prices)
    profit = 0
    myline = float("inf") # 基准线：最高点 - fee，初值为无穷大数 - fee，还是无穷大
    for price in prices:
        if price < myline:
            myline = price
        elif price > myline + fee: # 对应  A > fee + D
            profit += price - myline -fee
            myline = price - fee
        else:
            pass
    return profit


# 思想：
# 定义dp[i][0]为手里没有股票时当前第i天maxProfit（定义为state0）
# dp[i][1]为手里有股票时当前第i天maxProfit（定义为state1）

# 转移方程
# dp[i][0]=max{dp[i−1][0],dp[i−1][1]+prices[i]−fee}
# dp[i][1]=max{dp[i−1][1],dp[i−1][0]−prices[i]}
# dp[0][0]=0，dp[0][1]=−prices[0]

# 最后返回dp[n-1][0]与0两者之间的较大值
def dp_maxProfit(prices, fee):
    prices = list(prices)
    state0 = 0
    state1 = -prices[0]
    for price in prices[1:]:
        state0_last = state0  # 由于执行有先后，暂存一下
        state0 = max(state0, state1 + price - fee)
        state1 = max(state1, state0_last - price)
    return state0 # 不会有人觉得最后手里还有股票，还没卖出去能赚最多吧，直接返回手里没股票的最后一天的maxProfit


prices = prices6
fee = fee6
print(greedy_maxProfit(prices, fee))
print(greedy2_maxProfit(prices, fee))
print(dp_maxProfit(prices, fee))
