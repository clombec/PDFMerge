import pdfmerge
import tkinter as tk
from tkinter import filedialog


def goGetOutputFolder():
    # Display the dialog for browsing files.
    filename = filedialog.askdirectory()
    # Print the selected file path.
    print(filename)
    outputFolderEntry.delete(0, tk.END)
    outputFolderEntry.insert(0, filename)

def goGetScannerFolder():
    # Display the dialog for browsing files.
    filename = filedialog.askdirectory()
    # Print the selected file path.
    print(filename)
    scannerFolderEntry.delete(0, tk.END)
    scannerFolderEntry.insert(0, filename)


def handle_click():
    totalNb = int(pageNbEntry.get())
    file = fileNameEntry.get()
    destFolder = outputFolderEntry.get() + "//"
    path = scannerFolderEntry.get()
    pdfmerge.pdfMergeCore(totalNb, file, destFolder, path)
    print("click")

window = tk.Tk()
pageNbText = tk.Label(text="Nombre de pages ?")
pageNbEntry = tk.Entry(width=5)
fileNameText = tk.Label(text="Nom du fichier de sortie ? (sans le \".pdf)\"")
fileNameEntry = tk.Entry(width=50)
scannerFolderText = tk.Label(text="Dossier du scanner")
outputFolderText = tk.Label(text="Dossier de sortie")
scannerFolderEntry = tk.Entry(width=50)
scannerFolderEntry.insert(0, "D:\\DCIM\\113MEDIA")
outputFolderEntry = tk.Entry(width=50)
outputFolderEntry.insert(0, "C:\\Users\\Admin\\Dropbox\\Personnel\\ScanTemp")


goButton = tk.Button(
    text="GO",
    width=25,
    height=5,
    bg="#f0efd5",
    fg="#788f82",
    command=handle_click
)

goGetOutputFolderButton = tk.Button(
    text="Changer le dossier sortie",
    width=25,
    height=2,
    bg="#f0efd5",
    fg="#788f82",
    command=goGetOutputFolder
)
goGetScannerFolderButton = tk.Button(
    text="Changer le dossier du scanner",
    width=25,
    height=2,
    bg="#f0efd5",
    fg="#788f82",
    command=goGetScannerFolder
)

pageNbText.pack()
pageNbEntry.pack()
fileNameText.pack()
fileNameEntry.pack()
scannerFolderText.pack()
scannerFolderEntry.pack()
goGetScannerFolderButton.pack()
outputFolderText.pack()
outputFolderEntry.pack()
goGetOutputFolderButton.pack()
goButton.pack()
#print("go")

#goButton.bind("<Button-1>", handle_click)


window.mainloop()
