from pypdf import PdfWriter
import pdfmerge
import tkinter as tk
from tkinter import filedialog
import os

fileList = []
lastLineNum = -1
tagIndex = []

fileData = []

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

def clearFileSelection():
    for f in fileList:
        f.deselect()


def refreshFileList():
    global tagIndex
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

def callback(event):
    global lastLineNum
    global fileList
    print("callback")
    print(lastLineNum)
    #Get the click Contexte (Shift, Ctrl...)
    shiftClick = False
    ctrlClick = False
    #event.state: 1 = SHIFT, 2 = CAPSLOCK, 4 = CTRL, 8 = CLICK
    if (event.state & 0b0001):
        shiftClick = True
    if (event.state & 0b0100):
        ctrlClick = True

    #No CTRL-CLICK: select only clicked item. Clear others
    if (False == ctrlClick):
        clearFileSelection()

    # get the index of the mouse click
    index = event.widget.index("@%s,%s" % (event.x, event.y))
    #index is str(<line>.<column>) of the clicked text box - lineNum is the line number (starting from 0)
    lineNum = int(index[:index.find('.')]) - 1

    if ((True == shiftClick) & (lastLineNum >= 0)):
        for i in range (min(lineNum, lastLineNum), max(lineNum, lastLineNum)+1):
            fileList[i].bSelected = True
            print(fileList[i])
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

def pdfMergeCore(destPath, sourcePath):
    merger = PdfWriter()
    fileSelected = False

    for f in fileList:
        if (f.bSelected):
            print ("Merging " + sourcePath + "\\" + f.name)
            merger.append(sourcePath + "\\" + f.name)
            fileSelected = True
            os.remove(sourcePath + "\\" + f.name)
    
    if (True == fileSelected):
        merger.write(destPath)

    merger.close()

def goGetInputFolder():
    # Display the dialog for browsing files.
    filename = filedialog.askdirectory()
    # Print the selected file path.
    print(filename)
    inputFolderEntry.delete(0, tk.END)
    inputFolderEntry.insert(0, filename)


def handle_click():
    filename = outputFileEntry.get()
    path = inputFolderEntry.get()
    pdfMergeCore(filename, path)
    refreshFileList()
    #clearFileSelection()
    print("click")

def goGetOutputFile():
    # Display the dialog for browsing files.
    filename = filedialog.asksaveasfilename(confirmoverwrite=True, defaultextension=".pdf")
    # Print the selected file path.
    print(filename)
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
fileBox.tag_config("tag", foreground="#788f82")
fileBox.tag_bind("tag", "<Button-1>", callback)
fileBox.tag_config("select", background="#f0efd5")

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
    command = refreshFileList
)

goButton = tk.Button(
    text="GO",
    width=25,
    height=5,
    bg="#f0efd5",
    fg="#788f82",
    command=handle_click
)

refreshFileList()

inputFolderEntry.pack()
inputFolderBt.pack()
refreshButton.pack()
fileBox.pack()
outputFileEntry.pack()
outputFileBt.pack()
goButton.pack()

window.mainloop()