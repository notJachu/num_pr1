# TODO:
# - MACD function
# - EMA(period, data) function
# - SIGNAL function
# - check intersection of MACD and SIGNAL
# - plot the graph
# numpy, pyplot

# csv from WIG20 (pandas)

# plot 1 : index value
# plot 2 : MACT + SIGNAL + BUY/SELL AS ARROWS

import pandas as pd
import matplotlib.pyplot as plt

raw_data = pd.read_csv('wig20_sh.csv')
# EMAn(i) = alpha * data(i) + (1 - alpha) * EMAn(i-1)
# EMAn(0) = data(0)
def EMA(period, start, data):
    if start == 0:
        return data[start]
    alpha = 2 / (period + 1)
    ema = alpha * data[start] + (1 - alpha) * EMA(period, start - 1, data)
    return ema

def main():
    print(raw_data.to_string())
    raw_data.plot(x='Data', y='Zamkniecie')
    plt.show()


if __name__ == '__main__':
    main()