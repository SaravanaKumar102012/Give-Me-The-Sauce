#Module imports
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os

header = lambda : {"user-agent":UserAgent().random, "connection":"keep-alive"}
temp = "https://nhentai.net/g/"

def imgURLS(number):
    url = temp + number + "/"
    html = requests.get(url,headers=header()).text
    soup = BeautifulSoup(html,"html.parser").find_all("a")
    return list(filter(lambda x : number in x,list(map(lambda x: str(x.get("href")),soup))))[1:]

def imgSRC(url):
    html = requests.get(url,headers=header()).text
    soup = BeautifulSoup(html,"html.parser").find_all("img")
    final = list(map(lambda x: str(x.get("src")),soup))
    return final[1] if len(final) > 1 else final[0]

def rel2abs(urls):
    return list(map(lambda x: temp[:-3] + x,urls ))

def imgNames(lst):
    final = list()
    for el in lst:
        for i in range(len(el) - 2,-1,-1):
            if el[i] == '/':
                final.append(el[i+1:])
                break
    return final
    
def createFolder(folder):
    os.mkdir("Downloads/{}".format(folder))
    os.chdir("Downloads/{}".format(folder))

def downloadChap(number):
    number = str(number)
    urls = imgURLS(number)
    urls = rel2abs(urls)
    urls = list(map(lambda x: imgSRC(x),urls))
    names = imgNames(urls)
    return (number,urls,names)
