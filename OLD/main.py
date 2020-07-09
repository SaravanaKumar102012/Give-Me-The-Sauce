#Module imports
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os

header = lambda : {"user-agent":UserAgent().random, "connection":"keep-alive"}
temp = "https://nhentai.net/g/"

def imgURLS(number):
    #This function generates the relative urls for the pictures using the number of pages
    url = temp + number + "/"
    html = requests.get(url,headers=header()).text
    pageNum = int(BeautifulSoup(html,"html.parser").find_all("span",class_="name")[-1].string)
    return list("/g/{}/".format(number) + str(i) for i in range(1,pageNum+1))

def rel2abs(url):
    #rel2abs returns an absolute url after receiving as argument a relative url
    return temp[:-3] + url

def absoluteUrls(urls):
    #applies rel2abs to a list of relative urls
    return list(rel2abs(url) for url in urls)

def imgSRC(url):
    #imgSRC parses the image url for the source
    html = requests.get(url,headers=header()).text
    soup = BeautifulSoup(html,"html.parser").find_all("img")
    final = list(x.get("src") for x in soup)
    return final[-1]

def imgNames(lst):
    #generates the name of the images
    return list(str(i) + ".jpg" for i in range(1,len(lst) + 1))
    
def createFolder(folder):
    #creates the folder for the doujinshi
    os.mkdir("Downloads/{}".format(folder))
    os.chdir("Downloads/{}".format(folder))

def downloadChap(number):
    #uses the previously defined functions to get the urls and names for all the images
    number = str(number)
    urls = imgURLS(number)
    urls = absoluteUrls(urls)
    urls = list(map(lambda x: imgSRC(x),urls))
    names = imgNames(urls)
    createFolder(number)
    return (urls,names)