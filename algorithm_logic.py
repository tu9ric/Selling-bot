import requests
import pprint
import time
import threading
import keyboard
import sys

stop = True

def get_pairs():
    urlcoins = "https://api.bitget.com/api/v2/spot/public/symbols"
    responsecoins = requests.get(urlcoins)
    data = responsecoins.json()
    pairs = []

    for i in range(0, len(data["data"])):
        if(data["data"][i]["status"] == "online"):
            pair = [data["data"][i]["symbol"], data["data"][i]["baseCoin"], data["data"][i]["quoteCoin"]]
            pairs.append(pair)  
    return pairs

def get_chains(pairs):
    chains = []
    for i in range(0, len(pairs)):
        if(pairs[i][2] == "USDT"):
            for ii in range(0, len(pairs)):
                if(pairs[i][1] == pairs[ii][2]):
                    for iii in range(0, len(pairs)):
                        if(pairs[iii][1] == pairs[ii][1] and pairs[iii][2] == "USDT"):
                            chains.append([pairs[i][0], pairs[ii][0], pairs[iii][0]])
    return chains

def get_prices(chain):
    prices = {}
    for i in range(0, 3):
        urlorder = f'https://api.bitget.com/api/v2/spot/market/orderbook?symbol={chain[i]}&type=step0&limit=100'
        responseorder = requests.get(urlorder).json()
        prices[chain[i]] = ([responseorder["data"]['asks'][0], responseorder["data"]['bids'][0]])
    return prices

def get_income(prices, chain, usdt):
    in1 = usdt / float(prices[chain[0]][0][0]) - usdt / float(prices[chain[0]][0][0]) * 0.001
    in2 = in1 / float(prices[chain[1]][0][0]) - (in1 / float(prices[chain[1]][0][0])) * 0.001
    in3 = in2 * float(prices[chain[2]][1][0]) - (in2 * float(prices[chain[2]][1][0])) * 0.001
    in4 = usdt / float(prices[chain[2]][0][0]) - (usdt / float(prices[chain[2]][0][0])) * 0.001
    in5 = in4 * float(prices[chain[1]][1][0]) - (in4 * float(prices[chain[1]][1][0])) * 0.001
    in6 = in5 * float(prices[chain[0]][1][0]) - (in5 * float(prices[chain[0]][1][0])) * 0.001
    income = [in3 - usdt, in6 - usdt]
    return income


def continuous_function():
    usdt = 10
    data_pairs = get_pairs()
    data_chains = get_chains(data_pairs)
    i = 0
    while stop: 
        
        data_prices = get_prices(data_chains[i])
        data_income = get_income(data_prices, data_chains[i], usdt)
        '''
        global s
        s = str(i) + " " + str(data_chains[i]) + " " + str(data_income)
        '''
        print(i, " ", data_chains[i], " ", data_income)
        
        
        if(data_income[0] > 0 and data_income[1]  > 0):
            print(i, " ", data_chains[i], " ", data_income)
        
        #else:
            #print(i, " ", end='')
        if(data_income[0] < 0 and data_income[1]  < 0):
            i += 1
        if(i == len(data_chains)):
            i = 0 
    
def stop_function():
    global stop
    while stop:
        if keyboard.is_pressed('q'):
            stop = False
            
    print("Оба потока остановлены.")
   
    

def action():
    thread1 = threading.Thread(target=continuous_function)
    thread2 = threading.Thread(target=stop_function)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

action()
