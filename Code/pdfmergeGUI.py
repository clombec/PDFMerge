from pypdf import PdfWriter
import pdfmerge
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import os
import languages

__NOIMAGE__ = True

"""
#
# Language data
#
"""
textAllLang = [
    "Input folder doesn't exist", "Le dossier d'entrée n'existe pas",
    "Input Folder", "Dossier d'entrée",
    "Output File", "Fichier de sortie",
    "Missing output file path and name", "Fichier de sortie manquant",
    "Done","Fusion",
    "OK","OK"
]
l = languages.lang(languages.FRENCH,textAllLang,2)

class labelText:
    def __init__(self,master,text,l):
        self.text = text
        self.label = tk.Label(
            master=master,
            text="",
            font="None 10 bold"
        )
        self.label.pack(pady=5)
        self.langDict=l

    def refreshLabel(self):
        try:
            self.label["text"]=self.langDict.textDisplay[self.text]
        except KeyError:
            #In case the message is not in language Dictionnary, display the given message directly
            self.label["text"]=self.text

    def updateText(self,newTxt):
        self.text=newTxt
        self.refreshLabel()

    def updateBg(self,color):
        self.label["bg"] = color


def refreshLabels():
    l.initDictionary()
    for lb in allLabels:
        lb.refreshLabel()

def langChangeEnglish():
    print("English")
    l.selected=languages.ENGLISH
    refreshLabels()
        
def langChangeFrench():
    l.selected=languages.FRENCH
    refreshLabels()
    print("French")

"""
#
# Code
#
"""

#fileList: List of listedFile class objects.
#Contains a list of all files available in the input folder
fileList = []
lastLineNum = -1

sourcePath = "D:\\DCIM\\113MEDIA"

#list of files from input folder. Each file is defined with its name, state (Selected or not), and position in fileBox
class listedFile:
    def __init__(self, name, start, end):
        self.name = name
        self.bSelected = False
        self.start = start
        self.end = end

    def select(self):
        self.bSelected = True

    def deselect(self):
        self.bSelected = False

    def toggleSelect(self):
        self.bSelected = not self.bSelected

#Empty fileList
def clearFileSelection():
    for f in fileList:
        f.deselect()

#Force a refresh of the fileBox = display of all files from the input folder.
#All files are not-selected after the refresh
def goRefreshFileList():
    inPath = inputFolderEntry.get()
    fileBox.config(state="normal")
    fileBox.delete('1.0', "end")
    fileList.clear()

    if (os.path.isdir(inPath)):
        for i in os.listdir(inPath):
            if ((i.endswith('.pdf')) or (i.endswith('.PDF'))):
                fileBox.insert("end", i, "tag")
                fileBox.insert("end", "\n")
        infoLabel.updateText("")
        infoLabel.updateBg("SystemButtonFace")
    else:
        infoLabel.updateText("Input folder doesn't exist")
        infoLabel.updateBg("red")

    fileBox.config(state="disabled")
    tagIndex = list(fileBox.tag_ranges('tag'))
    for start, end in zip(tagIndex[0::2], tagIndex[1::2]):
        fileList.append(listedFile(fileBox.get(start,end),start,end))
       
def fileClicked(event):
    #define as global to allow write of the variable, available from other functions
    global lastLineNum

    #Get the click Contexte (Shift, Ctrl...)
    shiftClick = False
    ctrlClick = False
    #event.state: 1 = SHIFT, 2 = CAPSLOCK, 4 = CTRL, 8 = CLICK
    if (event.state & 0b0001):
        shiftClick = True
    if (event.state & 0b0100):
        ctrlClick = True

    #No CTRL-CLICK: select only clicked item. Clear others first
    if (False == ctrlClick):
        clearFileSelection()

    # get the index of the mouse click
    index = event.widget.index("@%s,%s" % (event.x, event.y))
    #index is str(<line>.<column>) of the clicked text box - lineNum is the line number (starting from 0 to comply with fileList)
    lineNum = int(index[:index.find('.')]) - 1

    #update fileList bSelected value for clicked items
    if ((True == shiftClick) & (lastLineNum >= 0)):
        for i in range (min(lineNum, lastLineNum), max(lineNum, lastLineNum)+1):
            fileList[i].bSelected = True
    elif (True == ctrlClick):
        fileList[lineNum].toggleSelect()
    else:
        fileList[lineNum].select()
    lastLineNum = lineNum

    #refresh visible file selection
    for f in fileList:
        if (f.bSelected):
            fileBox.tag_add("select", f.start, f.end)
        else:
            fileBox.tag_remove("select", f.start, f.end)

#Execution function. Get all selected files, merge them into output filename and delete selected files
def pdfMergeCore(destPath, sourcePath):
    merger = PdfWriter()

    #Only write output file if at least one input file has been selected 
    fileSelected = False

    for f in fileList:
        if (f.bSelected):
            print ("Merging " + sourcePath + "\\" + f.name)
            merger.append(sourcePath + "\\" + f.name)
            fileSelected = True
            os.remove(sourcePath + "\\" + f.name)

    #Only write output file if at least one input file has been selected 
    if (True == fileSelected):
        merger.write(destPath)

    merger.close()

#Open the dialog box to select the input folder
def goGetInputFolder():
    # Display the dialog for browsing folders
    filename = filedialog.askdirectory()
    #Display the selected folder path
    inputFolderEntry.delete(0, tk.END)
    inputFolderEntry.insert(0, filename)
    #Force a display of all files in the new selected folder
    goRefreshFileList()

#Click GO button: launch merge files process
def goMergeSelected():
    filename = outputFileEntry.get()
    #If no output file has been selected, do nothing
    if (0 == len(filename)):
        infoLabel.updateText("Missing output file path and name")
        infoLabel.updateBg("red")
        return
    
    #Get full path of the output file
    filepath = inputFolderEntry.get()
    #Execute merge
    pdfMergeCore(filename, filepath)
    #Refresh fileBox with remaining files (selected one have been deleted)
    goRefreshFileList()

    infoLabel.updateText("Done")
    infoLabel.updateBg("Green")

# Display the dialog for browsing files
def goGetOutputFile():
    #open output file name dialog box
    filename = filedialog.asksaveasfilename(confirmoverwrite=True, defaultextension=".pdf")
    #update entry
    outputFileEntry.delete(0, tk.END)
    outputFileEntry.insert(0, filename)


"""
########################################################################
##
## Geometry definition
##
########################################################################
"""

window = tk.Tk()
allLabels = []

#
#
# Languages buttons
#
#
languageFrame = tk.Frame(
    relief=tk.FLAT,
    borderwidth=2,
    width = 500,
    height = 500
)

if __NOIMAGE__:
    photo1 = ""
else:
    photo1 = PhotoImage(file="D:\\Projects\\PDFMerge\\Images\\unionjack.png")


tk.Button(
    master = languageFrame,
    text="",
    width=1,
    height=1,
    bg="#f0efd5",
    fg="#788f82",
    font='None 8 bold',
    command = langChangeEnglish,
    image=photo1
).pack(side=tk.LEFT)

if __NOIMAGE__:
    photo2 = ""
else:
    photo2 = PhotoImage(file="D:\\Projects\\PDFMerge\\Images\\frenchflag.png")

tk.Button(
    master = languageFrame,
    text="",
    width=1,
    height=1,
    bg="#f0efd5",
    fg="#788f82",
    font='None 8 bold',
    command = langChangeFrench,
    image=photo2
).pack(side=tk.LEFT)

#
#
# Input Folder label, Entry test and browse Button, within inputFrame
#
#
inputFrame = tk.Frame(
    relief=tk.GROOVE,
    borderwidth = 2
    )

#Input Label
inuputLabel = labelText(inputFrame,"Input Folder",l)
allLabels.append(inuputLabel)

#Input Folder Entry text
inputFolderEntry = tk.Entry(master = inputFrame, width=50, font='None 10')
inputFolderEntry.pack(side=tk.LEFT, pady=5,padx=5)
inputFolderEntry.insert(0, sourcePath)

#Browse for input folder Button
inputFolderBt = tk.Button(
    master = inputFrame,
    text="...",
    width=5,
    height=1,
    bg="#f0efd5",
    fg="#788f82",
    font='None 8 bold',
    command = goGetInputFolder
)
inputFolderBt.pack(side=tk.LEFT, pady=5,padx=5)

#
#
# file Box frame, containing file box list, and refresh button
#
#
fileFrame = tk.Frame(
    relief=tk.GROOVE,
    borderwidth=2,
    width = 500,
    height = 500
    )

#File list display box
fileBox = tk.Text(
    master = fileFrame,
    height = 15,
    width = 44
    )
fileBox.pack(side=tk.LEFT,padx=5,pady=5)

#Create tag for file Box. Tag is used to differentiate file name entries when clicked. Tag is bind to click
fileBox.tag_config("tag", foreground="#788f82")
fileBox.tag_bind("tag", "<Button-1>", fileClicked)
fileBox.tag_config("select", background="#f0efd5")
#disable all other binds for fileBox: now a Click in the file box will only execute the event bind to "tag". It avoids text selection
fileBox.bindtags((str(fileBox), str(window), "all"))

if __NOIMAGE__:
    photo = ""
else:
    photo = PhotoImage(file="D:\\Projects\\PDFMerge\\Images\\path1.png")

#Refresh Button
tk.Button(
    master = fileFrame,
    text="Rafraichir",
    width=1,
    height=1,
    bg="#f0efd5",
    fg="#788f82",
    font='None 12 bold',
    command = goRefreshFileList,
#    image=photo
).pack(side=tk.LEFT)

#
#
#Output file frame, with label, text entry and button
#
#
outputFrame = tk.Frame(
    relief=tk.GROOVE,
    borderwidth=2)

#Output Label
outputLabel = labelText(outputFrame,"Output File",l)
allLabels.append(outputLabel)

outputFileEntry = tk.Entry(
    master = outputFrame,
    width=50,
    font='None 10'
    )
outputFileEntry.pack(side=tk.LEFT,pady=5,padx=5)

outputFileBt = tk.Button(
    master = outputFrame,
    text="...",
    width=5,
    height=1,
    bg="#f0efd5",
    fg="#788f82",
    font='None 8 bold',
    command = goGetOutputFile
)
outputFileBt.pack(side=tk.LEFT,pady=5,padx=5)

#
#
#Go button frame, with Go button only
#
#
goFrame = tk.Frame(
    relief=tk.FLAT,
    borderwidth = 2
    )

#Go Button
tk.Button(
    master = goFrame,
    text="GO",
    width=25,
    height=5,
    bg="#f0efd5",
    fg="#788f82",
    command=goMergeSelected
).pack(padx=5,pady=5)


#
#
# Info file frame, with label only
#
#
infoFrame = tk.Frame(
    relief=tk.FLAT,
    borderwidth=2,
    width=50
    )

infoLabel = labelText(infoFrame,"",l)
allLabels.append(infoLabel)

#Start with updated fileBox using the default input folder
goRefreshFileList()

#Display all etxt using slected language
refreshLabels()

#Build the window
languageFrame.pack(pady=5,side=tk.BOTTOM)
inputFrame.pack(pady=5)
fileFrame.pack(expand=True,pady=5)
outputFrame.pack(pady=5)
goFrame.pack(pady=5)
infoFrame.pack(pady=5)

#run
window.mainloop()