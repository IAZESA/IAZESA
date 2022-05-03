import yfinance as yf
import pandas as pd


# FUNCTIONS ---------------------------------------------------------------------------------------------------------------


# trailing stop for max profit
def ipo_maxprofit(p_xlsx, p_ticker, p_trail):

    print(p_ticker)
    print('----------')

    price_stock = p_ticker[0] + '.JK'
    price_ipo = p_ticker[1]
    price_trail_percent = p_trail
    price_peak = price_ipo
    price_close = price_ipo
    price_trailing_stop = 0
    price_sell = 0

    ticker = yf.Ticker(price_stock)
    df = ticker.history(period='2y', interval='1d')

    df.insert(len(df.columns), 'Change %', 0)

    df.insert(len(df.columns), 'IPO', price_ipo)
    df.insert(len(df.columns), 'Floating PL %', 0)

    df.insert(len(df.columns), 'Peak', 0)
    df.insert(len(df.columns), 'Trail %', price_trail_percent)
    df.insert(len(df.columns), 'Trailing Stop', 0)

    df.insert(len(df.columns), 'Sell', 0)
    df.insert(len(df.columns), 'Realized PL %', 0)

    df.insert(len(df.columns), 'Flag', '-')

    df['Floating PL %'] = round(df['Close'] / price_ipo * 100, 1) - 100

    for i in df.index:
        df.at[i, "Change %"] = round(df.at[i, 'Close'] / price_close * 100, 1) - 100

        price_close = df.at[i, 'Close']
        price_peak = max(price_peak, df.at[i, 'High'])
        price_trailing_stop = int(price_peak * (1 + price_trail_percent))
        
        df.at[i, 'Peak'] = price_peak
        df.at[i, 'Trailing Stop'] = price_trailing_stop

        if price_sell == 0 and (price_close < price_trailing_stop):
            price_sell = price_close

            df.at[i, 'Sell'] = price_sell
            df.at[i, 'Realized PL %'] = round(price_sell / price_ipo * 100, 1) - 100
            df.at[i, 'Flag'] = "TS"


    print(df)
    print('----------')
    print('')
    
    df.to_excel(p_xlsx, sheet_name=p_ticker[0])
    p_xlsx.save()


# MAIN ---------------------------------------------------------------------------------------------------------------


# stock with trailing stop
stocks = [
            ['UNIQ',  118], ['ARCI',  750], ['MASB', 3360], ['BMHS',  340], ['UVCR',  100],
            ['HAIS',  300], ['GPSO',  180], ['OILS',  270], ['MCOL', 1420], ['RSGK', 1720],

            ['SBMA',  180], ['GTSI',  100], ['CMNT',  680], ['RUNS',  254], ['IDEA',  140],
            ['KUAS',  195], ['BOBA',  280], ['MTEL',  800], ['BINO',  138], ['DEPO',  482],

            ['WGSH',  140], ['WMPP',  160], ['TAYS',  360], ['CMRY', 3080], ['RMKE',  206],
            ['OBMD',  180], ['AVIA',  930], ['IPPE',  100], ['NASI',  155], ['BSML',  117],

            ['DRMA',  500], ['ADMR',  100], ['SEMA',  180], ['ASLC',  256], ['NETV',  196],
            ['BAUT',  100], ['ENAK',  850], ['NTBK',  100], ['ADCP',  130], ['SMKM',  264],

            ['STAA',  600], ['NANO',  100], ['BIKE',  170], ['WIRG',  168], ['SICO',  230],
            ['GOTO',  338], ['TLDN',  580], ['MTMH', 1280], ['IBOS',  100], ['WINR',  100]
]

print(stocks)
print('----------')
print('')


# check max profit & save to Excel
xlsx = pd.ExcelWriter('stock_ipo.xlsx', mode='w')

for stock in stocks:
    ipo_maxprofit(xlsx, stock, -0.15)

xlsx.close()
