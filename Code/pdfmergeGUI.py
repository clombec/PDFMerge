from pypdf import PdfWriter
import pdfmerge
import tkinter as tk
from tkinter import filedialog
import os

fileList = {}
lastLineNum = -1

#Test

def clearFileSelection():
    for i in fileList:
        fileList[i] = False


def refreshFileList():
    inPath = inputFolderEntry.get()
    fileBox.config(state="normal")
    fileBox.delete('1.0', "end")
    fileList.clear()

    if (os.path.isdir(inPath)):
        for i in os.listdir(inPath):
            if i.endswith('.pdf'):
                fileList[i] = False
                fileBox.insert("end", i, "tag")
                fileBox.insert("end", "\n")
    else:
        fileBox.insert("end", "Folder Doesn't exist")

    fileBox.config(state="disabled")

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
    print(lineNum)
    print(event.widget)
 
    # get the indices of all "adj" tags
    tag_indices = list(event.widget.tag_ranges('tag'))
    print(tag_indices)

    # iterate them pairwise (start and end index)
    for start, end in zip(tag_indices[0::2], tag_indices[1::2]):
        clickedFileName = event.widget.get(start, end)

        # check if the tag matches the mouse click index
        if event.widget.compare(start, '<=', index) and event.widget.compare(index, '<', end):
            if ((True == shiftClick) & (lastLineNum >= 0)):
                print(min(lineNum, lastLineNum), max(lineNum, lastLineNum)+1)
                keys = list(fileList)
                for i in range (min(lineNum, lastLineNum), max(lineNum, lastLineNum)+1):
                    fileList[keys[i]] = True
                    print(fileList)
            elif (True == ctrlClick):
                fileList[clickedFileName] = not fileList[clickedFileName]
            else:
                fileList[clickedFileName] = True
            lastLineNum = lineNum

    #refresh visible file selection
    for start, end in zip(tag_indices[0::2], tag_indices[1::2]):
        clickedFileName = event.widget.get(start, end)
        if (False == fileList[clickedFileName]):
            fileBox.tag_remove("select", start, end)
        else:
            print("add",start,end)
            fileBox.tag_add("select", start, end)


def pdfMergeCore(destPath, sourcePath):
    merger = PdfWriter()
    fileSelected = False

    for i in fileList:
        if (True == fileList[i]):
            print ("Merging " + sourcePath + "\\" + i)
            merger.append(sourcePath + "\\" + i)
            fileSelected = True
            os.remove(sourcePath + "\\" + i)
    
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