# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from bs4 import BeautifulSoup
import re


def BTC_Coin(url):
    r = requests.get(url)
    text = r.json()
    print("Bit coin price is(BTC/USD): ", text['high'])
    r.close()


def Coin(url):
    r = requests.get(url)
    text = r.text
    r.close()
    text = text.encode('utf-8').decode('ascii', 'ignore')
    text = str(text)
    return text


def AMPLE_Coin(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    rest = soup.find_all('tbody', attrs={"data-target": "gecko-table.paginatedShowMoreTbody"})
    txt: str = re.sub(r'\s+', ' ', rest[0].text).strip()
    # print(txt)
    reg1 = r".+ Uniswap \(v2\) AMPL/ETH.+?\$(\d+\.\d+).+"
    reg2 = r".+ KuCoin AMPL/USDT.+?\$(\d+\.\d+).+ "
    reg3 = r".+ Balancer AMPL/USDC.+?\$(\d+\.\d+).+"
    reg4 = r".+ Mooniswap AMPL/ETH.+?\$(\d+\.\d+).+"
    reg5 = r".+ Sushiswap AMPL/ETH.+?\$(\d+\.\d+).+"
    dct = dict()
    dct["Uniswap_AMPL_ETH"] = re.findall(reg1, txt)[0]
    dct["KuCoin_AMPL_USDT"] = re.findall(reg2, txt)[0]
    dct["Balancer_AMPL_USDC"] = re.findall(reg3, txt)[0]
    dct["Mooniswap_AMPL_ETH"] = re.findall(reg4, txt)[0]
    dct["Sushiswap_AMPL_ETH"] = re.findall(reg5, txt)[0]
    return dct


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    btc_url = 'https://api.livecoin.net/exchange/ticker?currencyPair=BTC/USD'
    BTC_Coin(btc_url)
    ampl_url = 'https://www.coingecko.com/en/coins/ampleforth#'
    # txt = Coin(btc_url)
    dct = AMPLE_Coin(ampl_url)
    print('AMPLE Coin Price:')
    # print(dct)
    for d in dct:
        print(d, ':', dct[d])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/