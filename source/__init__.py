import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os

class doujin:

    #the template used to generate the urls from the numbers
    template = "https://nhentai.net/g/"
    #the header used for the http requests
    header = lambda : {"user-agent":UserAgent().random, "connection":"keep-alive"}

    #initializes the object properties
    def __init__(self,number:int) -> None:
        """
        initializes the doujin type object by converting the number to a string (if not already) 
        and assigning it to the number property,also initializes all the object's remaining properties as None
        """
        if not isinstance(number,str):
            number = str(number)      #the number is stored as a string instead of an integer so
        self.number = number          #I dont have to convert it every time i concatenate strings
        self.URL = None               # property will contain a string (the url for the doujin)
        self.pageNum = None           # property will contain an integer (the total number of pages)
        self.html = None              # property will contain a beautifulSoup type object
        self.pageURLS = None          # property will contain an array of strings (urls for each page)
        self.title = None             # property will contain a string (the doujin title)
    
    def url(self) -> None:
        """
        #generates the url from the number and the template
        """
        self.URL = doujin.template + self.number + "/"
    
    def reqhtml(self) -> None:
        """
        makes a request to nhentai and stores the html received in self.html
        if the request fails a RuntimeError will be raised
        """
        req = requests.get(self.URL,headers=doujin.header()) #request to the server
        if req.status_code == 200:
            self.html = BeautifulSoup(req.text,"html") #beautifulsoup initialization
        else:
            raise RuntimeError("Request was not successful") #the request failed
    
    def getTitle(self) -> None:
        """
        uses the html requested in the reqhtml method to get the doujin title
        """
        self.title = [self.html.find("span",class_="before"),self.html.find("span",class_="pretty"),self.html.find("span",class_="after")]
        self.title = "".join(list(tag.get_text() for tag in self.title)).replace(" ","_")
    
    def getTotalNum(self) -> None:
        """
        uses the html requested in the reqhtml method to get the total number of doujin pages
        """
        self.pageNum = int(self.html.find_all("span",class_="name")[-1].string) #find the page number and convert it to int
    
    def genURLS(self) -> None:
        """
        uses the total page number to generate all page urls using the template
        """
        if self.pageNum is None:
            raise RuntimeError("self.pageNum is None, can't generate urls")
        self.pageURLS = list()
        for i in range(1,self.pageNum + 1): #generates the urls for the page that hosts the pictures
            self.pageURLS.append(self.URL + str(i) + '/')


class page(doujin):

    def __init__(self,url,num) -> None:
        """
        initializes the page type object by assigning the page's url to the url property and
        the page's number to the num property, all the remaining properties are initialized as None
        """
        self.URL = url
        self.source = None
        self.html = None
        self.content = None
        self.pageNumber = num
    
    def getSource(self) -> None:
        """
        uses the html requested in the reqhtml method to get the link for the image source,
        raises an error if it is unable to find any tags
        """
        self.source = self.html.find_all("img")
        if len(self.source) == 0:
            raise RuntimeError("Unable to find img tags")
        else:
            self.source = self.source[-1].get("src")
    
    def download(self) -> None:
        """
        requests the binary content from the image source and stores it in the
        content property
        """
        if self.source is None:
            raise RuntimeError("self.source is None")
        self.content = requests.get(self.source,headers=doujin.header())
        if self.content.status_code == 200:
            self.content = self.content.content
        else:
            raise RuntimeError("Request was not successful") #the request failed

    
class initialize:

    def __init__(self,number:int) -> None:
        """
        the constructor for the main class, receives a number and initializes the doujin object
        and a page object for each page
        """
        self.raw = doujin(number)
        self.raw.url()
        self.raw.reqhtml()
        self.raw.getTitle()
        self.raw.getTotalNum()
        self.raw.genURLS()
        self.initializePages() #self.pages is not declared here because i think it would be redundant
    
    def initializePages(self) -> None:
        """
        initializes all the page objects which are then stored in an array in the pages property
        """
        self.pages = list(page(self.raw.pageURLS[i],i + 1) for i in range(self.raw.pageNum))
        for Page in self.pages:
            Page.reqhtml()
            Page.getSource()

class download:

    def __init__(self,initedObj:initialize):
        """
        initializes a download object using the initialize class
        """
        self.djin = initedObj.raw
        self.pages = initedObj.pages
    
    def download(self,direct):
        """
        method that downloads all the pages either to a specified directory or to Downloads/<Doujin_name>
        """
        if direct is None:
            direct = "Downloads"
        try:
            os.mkdir("{}/{}".format(direct,self.djin.title))
        except: #if directory exists mkdir raises an error
            pass
        os.chdir("{}/{}".format(direct,self.djin.title))
        for Page in self.pages:
            Page.download()
            with open("{}.jpg".format(Page.pageNumber),"wb+") as f:
                f.write(Page.content)
            Page.content = None #so it doesnt occupy space