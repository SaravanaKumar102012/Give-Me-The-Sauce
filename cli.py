import source
import sys

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


class ALTdownload(source.download):
    def download(self,direct:str) -> None:
        """
        method that downloads all the pages either to a specified directory or to Downloads/<Doujin_name>
        """
        if direct is None:
            direct = "Downloads"
        try:
            source.os.mkdir("{}/{}".format(direct,self.djin.title))
        except: #if directory exists mkdir raises an error
            pass
        previousdir = source.os.getcwd() # save the current directory to come back to it
        source.os.chdir("{}/{}".format(direct,self.djin.title))
        with open("{}.txt".format(self.djin.number),"w+") as f:
                f.write(self.djin.number) #creates a text file with the doujin number inside the folder
        for Page in self.pages:
            Page.download()
            printProgressBar(Page.pageNumber,self.djin.pageNum)
            with open("{}.jpg".format(Page.pageNumber),"wb+") as f:
                f.write(Page.content)
            Page.content = None #so it doesnt occupy space
        source.os.chdir(previousdir)

if __name__ == "__main__":
    print("nHentai.net CLI Downloader")
    while(True):
        print("Options:")
        print("(1) -> Insert a number and download")
        print("(2) -> Read from a file")
        print("(3) -> Exit")
        choice = input("[1/2/3]->")
        if choice == '1':
            number = input("\nPlease input the number\n->")
            print("Please input the (absolute) destination directory")
            print("(If one is not specified it will be downloaded to <current directory>/Downloads/")
            print("Please don't put the '/' at the end of the path")
            direct = input("->")
            print("Initializing ...")
            content = source.initialize(int(number))
            print("Downloading ...")
            download = ALTdownload(content)
            if direct == "":
                download.download(None)
            else:
                download.download(direct)
        elif choice == '2':
            print("\nFile has to be written in the following format:")
            print("<number>\n<number>\n<number>\n...")
            print("Please insert path to file")
            filepath = input("->")
            print("\nPlease input the (absolute) destination directory")
            print("(If one is not specified it will be downloaded to <current directory>/Downloads/")
            print("Please don't put the '/' at the end of the path")
            direct = input("->")
            #make a function that creates the objects and downloads
        elif choice == '3':
            break
    sys.exit()