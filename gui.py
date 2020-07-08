import PySimpleGUI as sg   
import sys
import requests
import os
from main import createFolder,header,downloadChap

def getImgs(urls,names):
    l = len(urls)
    for i in range(l):
        binary = requests.get(urls[i],headers=header(),timeout=1).content
        with open(names[i],"wb+") as f:
            f.write(binary)
        sg.OneLineProgressMeter('Downloading...', i+1, l,orientation='h')
    os.chdir("..")

def download(number,urls,names):
    createFolder(number)
    getImgs(urls,names)

layout = [[sg.Text('Insert number here:')],      
                 [sg.InputText()],      
                 [sg.Submit(), sg.Cancel()]]      

window = sg.Window('nhentai.net scraper', layout)    

event, values = window.read()    
window.close()

if event == "Cancel":
    sys.exit()

number = values[0]
sg.popup('Downloading {} to Downloads/{}\n(Press OK to continue)'.format(number,number))
args = downloadChap(number)
download(*args)
sys.exit()