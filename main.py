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

def plot_transaction(filtered_data):

    index_delta = filtered_data['Zamkniecie'].iloc[-1] - filtered_data['Zamkniecie'].iloc[0]

    transaction_values = []
    transaction_dates = []
    transaction_start_date = None
    transaction_start_values = []
    transaction_end_date = None
    transaction_end_values = []
    transaction_count = 0


    # Calculate MACD and SIGNAL for the filtered data
    macd = MACD(filtered_data['Zamkniecie'])

    signal = SIGNAL(macd)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))

    ax1.plot(filtered_data['Data'], macd, color='blue', label='MACD')
    ax1.plot(filtered_data['Data'], signal, color='red', label='SIGNAL')

    for i in range(1, len(filtered_data)):
        if (macd[i] < signal[i]) and (macd[i - 1] > signal[i - 1]):
            # sell
            if transaction_start_date is not None:
                transaction_end_date = filtered_data['Data'][i]
                transaction_end_values.append(filtered_data['Zamkniecie'][i])
                transaction_values.append(transaction_end_values[-1] - transaction_start_values[-1])
                transaction_dates.append((transaction_start_date, transaction_end_date))
                transaction_start_date = None
                transaction_start_value = None
                transaction_count += 1
            ax1.annotate('',
                         xy=(filtered_data['Data'][i], macd[i]),
                         xytext=(0, 10),
                         textcoords='offset points',
                         arrowprops=dict(arrowstyle='wedge', color='red', mutation_scale=20))

        elif (macd[i] > signal[i]) and (macd[i - 1] < signal[i - 1]):
            # buy
            transaction_start_values.append(filtered_data['Zamkniecie'][i])
            transaction_start_date = filtered_data['Data'][i]


            ax1.annotate('',
                         xy=(filtered_data['Data'][i], macd[i]),
                         xytext=(0, -10),
                         textcoords='offset points',
                         arrowprops=dict(arrowstyle='wedge', color='green', mutation_scale=20))

    for i in range(len(transaction_dates)):
        ax2.annotate('',
                     xy=(transaction_dates[i][0], transaction_start_values[i]),
                     xytext=(transaction_dates[i][1], transaction_end_values[i]),
                     arrowprops=dict(arrowstyle='<->', color='blue', mutation_scale=20))
        print("Transaction: ", transaction_dates[i], "Value: ", transaction_values[i])

    print("Total value: ", sum(transaction_values))
    print("Index growth: ", index_delta)
    ax1.set_title('MACD and SIGNAL ' + filtered_data['Data'].iloc[0] + ' - ' + filtered_data['Data'].iloc[-1])
    ax1.legend()

    ax2.plot(filtered_data['Data'], filtered_data['Zamkniecie'], color='black', label='WIG20')
    ax2.set_title('WIG20 value ' + filtered_data['Data'].iloc[0] + ' - ' + filtered_data['Data'].iloc[-1])

    ax2.xaxis.set_major_locator(plt.MaxNLocator(10))
    ax1.xaxis.set_major_locator(plt.MaxNLocator(10))

    ax2.legend()
    plt.show()

def main():
    #print(raw_data.to_string())

    # 1000 units for simulation
    capital_units = 1000
    capital_value = 1000 * raw_data['Zamkniecie'][0]
    available_money = 0
    capital = []
    capital.append(capital_value)
    transaction_values = []



    macd = MACD(raw_data['Zamkniecie'])
    signal = SIGNAL(macd)


    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))

    ax1.plot(raw_data['Data'], macd, color='blue', label='MACD')
    ax1.plot(raw_data['Data'], signal, color='red', label='SIGNAL')


    for i in range(1, len(raw_data)):


        if (macd[i] < signal[i]) and (macd[i - 1] > signal[i - 1]):
            #sell
            if capital_units > 0:
                available_money = capital_units * raw_data['Zamkniecie'][i]
                capital_value = available_money
                capital_units = 0
                capital.append(round(capital_value, 2))
            ax1.annotate('',
                         xy=(raw_data['Data'][i], macd[i]),
                         xytext=(0, 10),
                         textcoords='offset points',
                         arrowprops=dict(arrowstyle='wedge', color='red', mutation_scale=20))

        elif (macd[i] > signal[i]) and (macd[i - 1] < signal[i - 1]):
            #buy
            if capital_units == 0:
                capital_units = capital_value / raw_data['Zamkniecie'][i]
                available_money = 0
                capital_value = capital_units * raw_data['Zamkniecie'][i]
                capital.append(round(capital_value, 2))
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

    # Filter data for the specified date range
    filtered_data = raw_data[(raw_data['Data'] >= '2022-09-01') & (raw_data['Data'] <= '2023-05-30')].reset_index(drop=True)

    plot_transaction(filtered_data)

    filtered_data = raw_data[(raw_data['Data'] >= '2023-03-20') & (raw_data['Data'] <= '2023-07-01')].reset_index(drop=True)

    plot_transaction(filtered_data)



    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))

    ax1.plot(capital, color='green', label='Capital')
    ax1.set_title('Capital')
    ax1.legend()

    ax2.plot(raw_data['Data'], raw_data['Zamkniecie'], color='black', label='WIG20')
    ax2.set_title('WIG20 value')

    ax2.xaxis.set_major_locator(plt.MaxNLocator(10))
    ax1.xaxis.set_major_locator(plt.MaxNLocator(10))

    ax2.legend()

    plt.show()

    print("Final capital: ", capital[-1])
    print("Total capital growth: ", capital[-1] - capital[0])
    print("Passive value: ", 1000 * raw_data['Zamkniecie'].iloc[-1])
    print("Passive growth: ", (raw_data['Zamkniecie'].iloc[-1] - raw_data['Zamkniecie'].iloc[0]) * 1000)


if __name__ == '__main__':
    main()