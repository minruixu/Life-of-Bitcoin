import re
from lxml import etree
import requests
from bs4 import BeautifulSoup
def writedata(url,time,n):
    max = -1
    maxaddress = ''
    fo = open('trackbtc/%s.csv'%n,'a+')
    fo.write(time)
    fo.write('\n')
    page = requests.get(url).text
    page = str(BeautifulSoup(page,'lxml'))
    selector = etree.HTML(page)
    for i in range(2,200):
        address = ''
        if i == 2:
            address = ''.join(selector.xpath('//*[@align="center"]/table[3]/tr[2]/td[5]/a/@href'))
            balance = ''.join(selector.xpath('//*[@align="center"]/table[3]/tr[2]/td[6]/text()[1]'))
        else:
            address = ''.join(selector.xpath('//*[@align="center"]/table[3]/tr[%s]/td[2]/a/@href'%i))
            balance = ''.join(selector.xpath('//*[@align="center"]/table[3]/tr[%s]/td[3]/text()[1]'%i))
        if len(address) == 0:
            fo.close
            return maxaddress
        balance = ''.join(re.findall('[0-9.]+',balance))
        fbalance = float(balance)
        address = address[17:]
        if fbalance > max:
            max = fbalance
            maxaddress = address
        fo.write(address + ',' + balance + '\n')

def getnext(url,n):
    page = requests.get(url).text
    page = str(BeautifulSoup(page, 'lxml'))
    selector = etree.HTML(page)
    time = selector.xpath('//*[@class="text-error utc"]/text()')
    btc = ''.join(selector.xpath('//*[@itemprop="price"]/text()'))
    block = ''.join(selector.xpath('//*[@id="table_maina"]/tbody/tr[1]/td[1]/a/@href'))
    block = block[3:]
    btc = ''.join(re.findall('[0-9.]+', btc))
    if float(btc) == 0:
        dataurl = 'https://bitinfocharts.com/bitcoin/' + block
        newaddress = writedata(dataurl,time,n)
        newurl = 'https://bitinfocharts.com/bitcoin/address/' + newaddress
        getnext(newurl,n+1)
    else:
        print("The ttravel is end\n")
        return 0


address = '1Bxc45nVNLchwp2hbtJXbc3f5dAEPpPrZn'
url = 'https://bitinfocharts.com/bitcoin/address/'+address
getnext(url,1)