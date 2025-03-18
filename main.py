# TODO:
# - buy/sell transactions
# - simulation starting with 1000 units of the share
#   that buys and sells with the MACD and SIGNAL strategy
# - plot the simulation
# - write a report

import pandas as pd
import matplotlib.pyplot as plt

raw_data = pd.read_csv('wig20_sh.csv')
# EMAn(i) = alpha * data(i) + (1 - alpha) * EMAn(i-1)
# EMAn(0) = data(0)
def EMA(period, start, data, prev_ema = 0):
    if start == 0:
        return data[start]
    alpha = 2 / (period + 1)
    ema = alpha * data[start] + (1 - alpha) * prev_ema
    return ema

def MACD(data):
    macd = []
    ema_12 = EMA(12, 0, data, data[0])
    ema_26 = EMA(26, 0, data, data[0])
    macd.append(ema_12 - ema_26)
    for i in range(1, len(data)):
        ema_12 = EMA(12, i, data, ema_12)
        ema_26 = EMA(26, i, data, ema_26)
        macd.append(ema_12 - ema_26)

    return macd

def SIGNAL(data):
    signal = []
    ema_9 = EMA(9, 0, data, data[0])
    signal.append(ema_9)
    for i in range(1, len(data)):
        ema_9 = EMA(9, i, data, ema_9)
        signal.append(ema_9)

    return signal


def main():
    #print(raw_data.to_string())
    macd = MACD(raw_data['Zamkniecie'])
    signal = SIGNAL(macd)


    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))

    ax1.plot(raw_data['Data'], macd, color='blue', label='MACD')
    ax1.plot(raw_data['Data'], signal, color='red', label='SIGNAL')


    for i in range(1, len(raw_data)):


        if (macd[i] < signal[i]) and (macd[i - 1] > signal[i - 1]):
            #sell
            ax1.annotate('',
                         xy=(raw_data['Data'][i], macd[i]),
                         xytext=(0, 10),
                         textcoords='offset points',
                         arrowprops=dict(arrowstyle='wedge', color='red', mutation_scale=20))

        elif (macd[i] > signal[i]) and (macd[i - 1] < signal[i - 1]):
            #buy
            ax1.annotate('',
                         xy=(raw_data['Data'][i], macd[i]),
                         xytext=(0, -10),
                         textcoords='offset points',
                         arrowprops=dict(arrowstyle='wedge', color='green', mutation_scale=20))

    ax1.set_title('MACD and SIGNAL')
    ax1.legend()

    ax2.plot(raw_data['Data'], raw_data['Zamkniecie'], color='black', label='WIG20')
    ax2.set_title('WIG20 value')

    ax2.xaxis.set_major_locator(plt.MaxNLocator(10))
    ax1.xaxis.set_major_locator(plt.MaxNLocator(10))

    ax2.legend()
    plt.show()

if __name__ == '__main__':
    main()