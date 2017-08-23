# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 22:10:50 2017

@author: stinson
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 21:44:34 2017

@author: stinson
"""

import requests
from bs4 import BeautifulSoup
import time
import json
import codecs


def get_googleSERP(keyword,page):
    index = (page-1)*10
    if index == 0:
        url = 'https://www.google.com/search?q='+keyword;
    else:
        url = 'https://www.google.com/search?q='+keyword+"&start="+str(index);
    res = requests.get(url)
    return res

def bs_GoogleSerp_Ad(res,page):
    ##廣告
    soup = BeautifulSoup(res.text,"lxml")
    data_Ad = soup.find_all('li',class_ = 'ads-ad')
    ad=[]
    for d in data_Ad:
        web ={"page" : str(page),
              "title" : d.find('a').text,
              "cite" : str(d.find('cite', class_="_WGk").text),
              "description" : str(d.find('div',class_='ellip').text) 
        }
        
        ad.append(web)
    return ad
    
def bs_GoogleSERP_Organic(res,page):
    # google organic serch rank
    soup = BeautifulSoup(res.text,"lxml")
    data_organic = soup.find_all('div', class_='g')
    rank = (page-1)*10
    SERP = []
    for d in data_organic:
        rank +=1;
        if (d.find('cite') is None and (d.find('img')['alt'] is not None)):
            #print("==="+str(d.find('img')['alt'])+"===")
            web = {"rank" :  str(rank),
                   "title" : "==="+str(d.find('img')['alt'])+"===",
                   "cite": '',
                   "description":''}
        else:
            web = {"rank" :  str(rank),
                   "title" : str(d.find('a').text),
                   "cite":str(d.find('cite').text),
                   "description":str(d.find('span',class_="st").text) }
        
        SERP.append(web)
        print("#" + str(rank)+"  "+web['title'])
    return SERP
        


def googleSERP(keyword,WebSite):
    ad = []
    SERP = []
    for page in range(1,6):
        if (page != 1):
            print('waiting 30s...避免被google判定為機器人')
            time.sleep(20)  # 每次爬取前暫停 30 秒以免被google網站判定為大量惡意爬取
        print("Analyze Page "+str(page))
        res = get_googleSERP(keyword,page)
        ad.extend([bs_GoogleSerp_Ad(res,page)])
        SERP.extend([bs_GoogleSERP_Organic(res,page)])
        
        #檢查是否有目標網站
        isContinue = True
        for i in SERP[page-1]:
            if WebSite in i['cite']:
                print('find '+ WebSite+' at '+i['rank'])
                isContinue = False;
                break
        if isContinue == False:
            break

    isprint = True  # 是否列印結果    
    if( isprint == True):
        filename =  'C:/Users/stinson/Desktop/SERP_'+keyword+'_'+str(time.strftime("%Y%m%d"))+'.txt';
        filename =  'SERP_'+keyword+'_'+str(time.strftime("%Y%m%d"))+'.txt';
        with open(filename, 'wb') as f:
            for j in SERP:
                for i in j:
                    json.dump(i, codecs.getwriter('utf-8')(f), ensure_ascii=False)
    print('Complete!')
    return SERP
                

##############main

keywords = ['空飄氣球','廣告氣球','展場氣球','大氣球'] #要查找的關鍵字
WebSite ='www.moskafactory.com' #目標網址
rank = []
for keyword in keywords:
    SERP = googleSERP(keyword,WebSite)
    
    isContinue = True;
    _rank = 0
    for j in SERP:
        for i in j:
            if WebSite in i['cite']:
                print('find '+ WebSite+' at '+i['rank'])
                isContinue = False;
                _rank = i['rank']
                break
        if isContinue == False:
            break
    rank.extend([_rank])


