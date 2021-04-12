import math

def choose():
    func = input("請選擇功能(1-投報率試算,2-房貸試算,3-槓桿平衡試算):")
    if func == '1':
        invest()
    elif func == '2':
        debt()
    else:
        leverage()

def invest():
    principle = input("本金(萬):")
    rate = input("年利率(%):")
    monthly = input("每月投入(萬):")
    year = input("投入年數(年):")
    print("本金:{}萬 / 年利率:{}% / 每月投入:{}萬 / 連續:{}年".format(
        principle,
        rate,
        monthly,
        year
    ))
    principle = float(principle) * 10000
    rate = float(rate) / 100
    monthly = float(monthly) * 10000
    year = int(year)

    result_i = 0
    result = 0
    base = principle + (monthly * 12 * year)

    def t1(x, y):
        x = (x * (1 + rate)) + (monthly * 12)
        if y == 0:
            return x
        else:
            return t1(x, y - 1)
    result_i = t1(principle, year)
    result = base + sum([(principle + (monthly * 12 * y)) * rate for y in range(year)])

    base = principle + (monthly * 12 * year)

    returnOn = round(((result - base) / base) * 100, 2)
    yReturnOn = round((pow(result / base, 1 / year) - 1) * 100, 2)

    returnOn_i = round(((result_i - base) / base) * 100, 2)
    yReturnOn_i = round((pow(result_i / base, 1 / year) - 1) * 100, 2)

    print("=======================利息不投入=========================")
    print("投入本金:{}".format(base))
    print("{}年後總額:{}".format(year, round(result, 2)))
    print("累積報酬率:{}%".format(returnOn))
    print("年化報酬率:{}%".format(yReturnOn))
    print("=======================利息再投入=========================")
    print("投入本金:{}".format(base))
    print("{}年後總額:{}".format(year, round(result_i, 2)))
    print("累積報酬率:{}%".format(returnOn_i))
    print("年化報酬率:{}%".format(yReturnOn_i))

def debt():
    principle = input("貸款金額(萬):")
    rate = input("利率(%):")
    year = input("還款年數(年):")
    early = input("預計還款年數(年):")
    print("貸款金額:{}萬 / 利率:{}% / 還款年數:{}年 / 預計還款年數:{}年".format(
        principle,
        rate,
        year,
        early
    ))
    principle = float(principle) * 10000
    mrate = (float(rate) / 12) / 100
    year = int(year)
    monthly = principle / (year * 12)
    early = int(early)
  
    interest_early = 0
    interest_all = 0
    base = principle
    remain = principle
    for m in range(year * 12):
        interest = base * mrate
        interest_all = interest_all + interest
        base = base - monthly
        if m < early * 12:
            interest_early = interest_all
            remain = base
    real_rate = round((pow((principle + interest_all) / principle, 1 / year) - 1) * 100, 2)
    if year == early:
        real_rate_early = real_rate
        real_rate_remain = 0
    else:
        real_rate_early = round((pow((principle - remain + interest_early) / (principle - remain), 1 / early) - 1) * 100, 2)
        real_rate_remain = round((pow((remain + interest_all - interest_early) / remain, 1 / (year - early)) - 1) * 100, 2)

    print("=======================本金平均攤還=========================")
    print("總還款金額:{}".format(round(principle + interest_all)))
    print("總利息金額:{}".format(round(interest_all)))
    print("平均月還款:{}".format(round((principle + interest_all) / (year * 12))))
    print("實際年利率:{}".format(real_rate))
    print("{}年後已付利息:{}".format(early, round(interest_early)))
    print("{}年後剩餘本金:{}".format(early, round(remain)))
    print("{}年後已付平均月還款:{}".format(early, round((principle - remain + interest_early) / (early * 12))))
    print("{}年後已付年化利率:{}".format(early, real_rate_early))
    print("{}年後剩餘年化利率:{}".format(early, real_rate_remain))

def leverage():
    principle = input("貸款金額(萬):")
    rate = input("貸款利率(%):")
    year = input("還款年數(年):")
    invest_base = input("投資本金(萬):")
    invest_rate = input("投資年利率(%):")
    print("貸款金額:{}萬 / 貸款利率:{}% / 還款年數:{}年 / 投資本金:{}萬 / 投資連利率:{}%".format(
        principle,
        rate,
        year,
        invest_base,
        invest_rate
    ))
    principle = float(principle) * 10000
    mrate = (float(rate) / 12) / 100
    year = int(year)
    monthly = principle / (year * 12)
    invest_base = float(invest_base) * 10000
    invest_rate = float(invest_rate) / 100  

    interest_all = 0
    base = principle
    invest_all = 0
    bucket = 0
    run_m = 0
    total_pay = 0
    for m in range(year * 12):
        interest = base * mrate
        if bucket > 0:
            if bucket >= interest:
                bucket = bucket - interest
                interest = 0
            else:
                interest = interest - bucket
                bucket = 0
        interest_all = interest_all + interest
        base = base - monthly
        if m > 0 and m % 12 == 0:
            invest_all = invest_all + (invest_base * invest_rate)
            bucket = bucket + (invest_base * invest_rate)
        if base <= invest_base + bucket:
            run_m = m + 1
            total_pay = run_m * monthly + interest_all
            break

    print("====================槓桿投資本金平均攤還======================")
    print("總還款金額:{}".format(round(principle + interest_all)))
    print("總利息金額:{}".format(round(interest_all)))
    print("投資產生利息:{}".format(round(invest_all)))
    print("實際支付總額:{}".format(round(total_pay)))
    print("平均月還款:{}".format(round(total_pay / run_m)))
    print("實際還款時間:{}年{}個月".format(math.floor(run_m / 12), run_m % 12))

if __name__ == '__main__':
    choose()
