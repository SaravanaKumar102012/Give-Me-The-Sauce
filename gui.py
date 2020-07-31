import source
import PySimpleGUI as sg

#function used to return current filled percentage of the progress bar
iteration = lambda current,total:int((current / total) * 100)

#the theme used for the window
sg.theme("Reddit")

#the layout for the window
layout = [  [sg.Text('Input the Number:                     ',key="UpperText")],
            [sg.Input(), sg.FileBrowse(key="Browse")],
            [sg.Text('Destination Directory (If one is not specified it will be downloaded to <current directory>/Downloads/)')],
            [sg.Input(), sg.FolderBrowse()],
            [sg.Text("                                                       ",key="DownloadText")],
            [sg.ProgressBar(100,orientation='h',size=(45,15),key="progressbar")],
            [sg.OK(button_text="Go!"), sg.Cancel(),sg.Radio("Number","rad1",background_color='grey',default=True),sg.Radio("File","rad1",background_color='grey')]]

#initialization of the window object
window = sg.Window('nHentai.net GUI Downloader', layout)

#progress bar for a single download
progressbar = lambda current,total: window["progressbar"].UpdateBar(iteration(current,total))

#progressbar for downloading from a file
messageUpdateFILES = lambda number: window["DownloadText"].update("Now Downloading {}".format(number))

#main code
while True:
    event,values = window.read(timeout=10)
    if values[2] == True: #values[2] and [3] are the radio buttons for the options
        window['UpperText'].update("Input the number:")
        window['Browse'].update(disabled=True)
    elif values[3] == True:
        window['UpperText'].update("Input the path to the file:")
        window['Browse'].update(disabled=False)
    if event == "Cancel":
        break
    if event == "Go!":
        sg.popup_ok("Downloading Now !",auto_close=True,auto_close_duration=5) #popup auto closes after 5 seconds unless manually closed
        direct = values[1]                                                     #because the download won't start while the popup is open
        if direct == "":
            direct = None
        if values[2]:
            number = values[0]
            window["DownloadText"].update("Now Downloading {}".format(number))
            data = source.initialize(int(number))
            down = source.download(data)
            down.download(direct,progressbar)
        else:
            filepath = values[0]
            txtfile = source.txtfile(filepath)
            txtfile.initandDownload(direct,progressbar,messageUpdateFILES)
        print("Directory:{}".format(direct)) #little message printed when the download is finished
        print("Input:{}".format(values[0]))
        sg.popup_ok("Done!") #another popup at the end for when the download is done

window.close()