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

#prints a message with the number of the current download
updateMessageFILES = lambda x : print("Now downloading {}.".format(x))

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
            print("(If one is not specified it will be downloaded to <current directory>/Downloads/)")
            print("Please don't put the '/' at the end of the path")
            direct = input("->")
            print("Initializing ...")
            content = source.initialize(int(number))
            print("Downloading ...")
            download = source.download(content)
            if direct == "":
                download.download(None,printProgressBar)
            else:
                download.download(direct,printProgressBar)
        elif choice == '2':
            print("\nFile has to be written in the following format:")
            print("<number>\n<number>\n<number>\n...")
            print("Please insert path to file")
            filepath = input("->")
            print("\nPlease input the (absolute) destination directory")
            print("(If one is not specified it will be downloaded to <current directory>/Downloads/")
            print("Please don't put the '/' at the end of the path")
            direct = input("->")
            allNumbers = source.txtfile(filepath)
            if direct == "":
                allNumbers.initandDownload(None,printProgressBar,updateMessageFILES)
            else:
                allNumbers.initandDownload(direct,printProgressBar,updateMessageFILES)
        elif choice == '3':
            break
    sys.exit()