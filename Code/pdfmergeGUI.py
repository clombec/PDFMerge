from pypdf import PdfWriter
import pdfmerge
import tkinter as tk
from tkinter import filedialog
import os

#fileList: List of listedFile class objects.
#Contains a list of all files available in the input folder
fileList = []
lastLineNum = -1

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
            if i.endswith('.pdf'):
                fileBox.insert("end", i, "tag")
                fileBox.insert("end", "\n")
    else:
        fileBox.insert("end", "Folder Doesn't exist")

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
        print("nope")
        return
    
    #Get full path of the output file
    filepath = inputFolderEntry.get()
    #Execute merge
    pdfMergeCore(filename, filepath)
    #Refresh fileBox with remaining files (selected one have been deleted)
    goRefreshFileList()

# Display the dialog for browsing files
def goGetOutputFile():
    #open output file name dialog box
    filename = filedialog.asksaveasfilename(confirmoverwrite=True, defaultextension=".pdf")
    #update entry
    outputFileEntry.delete(0, tk.END)
    outputFileEntry.insert(0, filename)


sourcePath = "D:\\DCIM\\113MEDIA"

window = tk.Tk()
window.geometry("400x600")

inputFolderEntry = tk.Entry(width=50)
inputFolderEntry.insert(0, sourcePath)

outputFileEntry = tk.Entry(width=50)

fileBox = tk.Text(
    window,
    height = 12,
    width = 32
    )
#Create tag for file Box
fileBox.tag_config("tag", foreground="#788f82")
fileBox.tag_bind("tag", "<Button-1>", fileClicked)
fileBox.tag_config("select", background="#f0efd5")
#disable all binds for fileBox: now a Click in the file box will only execute the event bind to "tag". It avoids text selection
fileBox.bindtags((str(fileBox), str(window), "all"))


inputFolderBt = tk.Button(
    text="...",
    width=5,
    height=2,
    bg="#f0efd5",
    fg="#788f82",
    font='None 12 bold',
    command = goGetInputFolder
)

outputFileBt = tk.Button(
    text="...",
    width=5,
    height=2,
    bg="#f0efd5",
    fg="#788f82",
    font='None 12 bold',
    command = goGetOutputFile
)

refreshButton = tk.Button(
    text="Rafraichir",
    width=15,
    height=3,
    bg="#f0efd5",
    fg="#788f82",
    font='None 12 bold',
    command = goRefreshFileList
)

goButton = tk.Button(
    text="GO",
    width=25,
    height=5,
    bg="#f0efd5",
    fg="#788f82",
    command=goMergeSelected
)

#Start with updated fileBox using the default input folder
goRefreshFileList()

#Build the window
inputFolderEntry.pack()
inputFolderBt.pack()
refreshButton.pack()
fileBox.pack()
outputFileEntry.pack()
outputFileBt.pack()
goButton.pack()

#run
window.mainloop()