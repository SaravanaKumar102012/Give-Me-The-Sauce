import PySimpleGUI as sg   
import sys
import requests
import os
from main import header,downloadChap

def getImgs(urls,names):
    #downloads the images
    l = len(urls)
    for i in range(l):
        binary = requests.get(urls[i],headers=header(),timeout=1).content
        with open(names[i],"wb+") as f:
            f.write(binary)
        sg.OneLineProgressMeter('Downloading...', i+1, l,orientation='h')
    os.chdir("..")

layout = [[sg.Text('Insert number here:',background_color=None)],      
                 [sg.InputText()],      
                 [sg.Submit(), sg.Cancel()]]

sg.theme("DarkBrown4")

def run():
    window = sg.Window('nhentai.net scraper', layout)    

    event, values = window.read()    
    window.close()

    if event == "Cancel":
        return

    number = values[0]
    sg.popup('Downloading {} to {}/Downloads/{}/\n(Press OK to continue)'.format(number,os.getcwd(),number))
    args = downloadChap(number)
    getImgs(*args)

if __name__ == "__main__":
    run()
    sys.exit(0)