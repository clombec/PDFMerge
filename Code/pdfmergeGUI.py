from pypdf import PdfWriter
import pdfmerge
import tkinter as tk
from tkinter import filedialog
import os

lastClickIndex = -1
fileList = {}

def clearFileSelection():
    for i in fileList:
        fileList[i] = False

def invertSelection(fileName):
    print(fileName)
    print(fileList[fileName])
    if (False == fileList[fileName]):
        print("oui")
        fileList[fileName] = True
    else:
        print("non")
        fileList[fileName] = False

    print(fileList)


def refreshFileList():
    inPath = inputFolderEntry.get()
    fileBox.config(state="normal")
    fileBox.delete('1.0', "end")

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
    print("callback")
    #Get the click Contexte (Shift, Ctrl...)
    shiftClick = False
    ctrlClick = False
    #event.state: 1 = SHIFT, 2 = CAPSLOCK, 4 = CTRL, 8 = CLICK
    if (event.state & 0b0001):
        shiftClick = True
    if (event.state & 0b0100):
        ctrlClick = True

    #Shift click to be managed one day

    #No CTRL-CLICK: select only clicked item. Clear others
    if (False == ctrlClick):
        clearFileSelection()

    # get the index of the mouse click
    index = event.widget.index("@%s,%s" % (event.x, event.y))

    # get the indices of all "adj" tags
    tag_indices = list(event.widget.tag_ranges('tag'))

    # iterate them pairwise (start and end index)
    for start, end in zip(tag_indices[0::2], tag_indices[1::2]):
        clickedFileName = event.widget.get(start, end)
        # check if the tag matches the mouse click index
        if event.widget.compare(start, '<=', index) and event.widget.compare(index, '<', end):
            if (True == ctrlClick):
                print("invert")
                invertSelection(clickedFileName)
            else:
                fileList[clickedFileName] = True

        if (0 == fileList[clickedFileName]):
            print("remove",start,end)
            fileBox.tag_remove("select", start, end)
        else:
            print("add",start,end)
            fileBox.tag_add("select", start, end)

def pdfMergeCore(destPath, sourcePath):
    print(destPath + sourcePath)
    merger = PdfWriter()

    for i in fileList:
        if (True == fileList[i]):
            print ("Merging " + sourcePath + "\\" + i)
            merger.append(sourcePath + "\\" + i)

    merger.write(destPath)
    merger.close()

    for i in fileList:
        if (True == fileList[i]):
            os.remove(sourcePath + "\\" + i)


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
    clearFileSelection()
    print("click")

def goGetOutputFile():
    # Display the dialog for browsing files.
    filename = filedialog.asksaveasfilename(confirmoverwrite=True, defaultextension=".pdf")
    # Print the selected file path.
    print(filename)
    outputFileEntry.delete(0, tk.END)
    outputFileEntry.insert(0, filename)


sourcePath = "D:\\Projects\\PDFMerge\\TestFolder"


window = tk.Tk()
window.geometry("400x600")

inputFolderEntry = tk.Entry(width=50)
inputFolderEntry.insert(0, "D:\\DCIM\\113MEDIA")
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