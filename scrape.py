# -*- coding: utf-8 -*-
"""

Read CME group rate hike expectation and probabilities

Created on Fri Oct 14 17:41:46 2016

@author: lizhuo
"""
import sys
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

def main(): 
    if len(sys.argv)>=2:
        path=sys.argv[1]
    else:
        print('Please Spcify output file!')
        sys.exit()
    
    # Need to use agent to mask access otherwise acess will be denied
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    
    # URL to Chicago Mechandise Exchange
    url='http://cme-fedwatch-prod.aws.barchart.com/static/index.html'

    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.User-Agent'] = user_agent
    driver = webdriver.PhantomJS()
    driver.get(url)
    time.sleep(3)
    
    
    soup = BeautifulSoup(driver.page_source,"lxml")
    
    all_tables=soup.find_all('table')
    mydivs=soup.find_all('a')
    
    
    column_nm=[all_tables[1].findAll('tr')[0].findAll('th')[i].contents for i in range(0,3)]
    column_nm=[str(item).replace("'",'').replace('[','').replace(']','') for item in column_nm]
    column_nm.append('date')
    
    index=list()
    data=list()
    
    for i in range(len(all_tables)):
        for j in range(len(all_tables[i].findAll('tr'))-1):
                row=[item.contents[0] for item in all_tables[i].findAll('tr')[j+1].findAll('td')]
                row.append(mydivs[i+1].contents[0])
                data.append(row)
    
    output=pd.DataFrame(data,columns=column_nm)
    output.iloc[:,1:3]=test.iloc[:,1:3].astype('float')
    index=list(zip(pd.DatetimeIndex(output.loc[:,'date']),output.loc[:,'Target Rate (bps)']))
    index = pd.MultiIndex.from_tuples(index, names=['time', 'rate'])
    output=pd.DataFrame(data,columns=column_nm,index=index)
    output.drop(['date','Target Rate (bps)'],axis=1,inplace=True)
    
    # save daily target rates prediction to csv file
    output.to_csv(path)

if __name__=="__main__":
   sys.exit(main())