from pypdf import PdfWriter
import pdfmerge
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import languages

__NOIMAGE__ = True
__VERSION__ = "2.0.0"


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
    "OK","OK",
    "Are you sure you want to overwrite the file?","Etes-vous sûr de vouloir écraser le fichier ?",
    "No input file selected","Aucun fichier d'entrée sélectionné",
    "Please select a single PDF file to split.", "Veuillez sélectionner un seul fichier PDF à séparer.",
    "Please enter a positive integer for split.", "Veuillez entrer un nombre entier positif pour le split.",
    "Number of pages must be at least 1.", "Le nombre de pages doit être supérieur ou égal à 1.",
    "File doesn't have enough pages", "Le fichier ne contient pas assez de pages.",
    "Error during split", "Erreur lors du split"
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

# List of listedFile class objects.
# Contains a list of all files available in the input folder
fileList = []
lastLineNum = -1

sourcePath = "E:\\DCIM\\113MEDIA"

# Each file from input folder is defined with its name, state (Selected or not), and position in fileBox
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

# Deselect all files in fileList
def clearFileSelection():
    for f in fileList:
        f.deselect()

# Force a refresh of the fileBox: displays all files from the input folder.
# All files are deselected after the refresh.
# Files are displayed in alphabetical order.

def goRefreshFileList():
    inPath = inputFolderEntry.get()
    fileBox.config(state="normal")
    fileBox.delete('1.0', "end")
    fileList.clear()

    if (os.path.isdir(inPath)):
        # List and sort PDF files alphabetically
        pdfs = [i for i in os.listdir(inPath) if i.lower().endswith('.pdf')]
        pdfs.sort(key=lambda x: x.lower())
        for i in pdfs:
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
    # Define as global to allow write of the variable, available from other functions
    global lastLineNum

    # Get the click context (Shift, Ctrl...)
    shiftClick = False
    ctrlClick = False
    # event.state: 1 = SHIFT, 2 = CAPSLOCK, 4 = CTRL, 8 = CLICK
    if (event.state & 0b0001):
        shiftClick = True
    if (event.state & 0b0100):
        ctrlClick = True

    # No CTRL-CLICK: select only clicked item. Clear others first
    if (False == ctrlClick):
        clearFileSelection()

    # Get the index of the mouse click
    index = event.widget.index("@%s,%s" % (event.x, event.y))
    # index is str(<line>.<column>) of the clicked text box - lineNum is the line number (starting from 0 to comply with fileList)
    lineNum = int(index[:index.find('.')]) - 1

    # Update fileList bSelected value for clicked items
    if ((True == shiftClick) & (lastLineNum >= 0)):
        for i in range (min(lineNum, lastLineNum), max(lineNum, lastLineNum)+1):
            fileList[i].bSelected = True
    elif (True == ctrlClick):
        fileList[lineNum].toggleSelect()
    else:
        fileList[lineNum].select()
    lastLineNum = lineNum

    # Refresh visible file selection
    for f in fileList:
        if (f.bSelected):
            fileBox.tag_add("select", f.start, f.end)
        else:
            fileBox.tag_remove("select", f.start, f.end)

# Execution function. Gets all selected files, merges them into the output filename and deletes selected files.
# Returns True if merge is done, False if not.

def pdfMergeCore(destPath, sourcePath):
    merger = PdfWriter()

    # Only write output file if at least one input file has been selected 
    # fileSelected = False

    if (os.path.isfile(destPath)):
        if (messagebox.askokcancel(title="OK", message=l.textDisplay["Are you sure you want to overwrite the file?"]) == False):
            return False

    for f in fileList:
        if (f.bSelected):
            print ("Merging " + os.path.join(sourcePath, f.name))
            merger.append(os.path.join(sourcePath, f.name))
            os.remove(os.path.join(sourcePath, f.name))  # Remove input files after merging

    merger.write(destPath)

    merger.close()

    return True

# Open the dialog box to select the input folder

def goGetInputFolder():
    # Display the dialog for browsing folders
    filename = filedialog.askdirectory()
    # Display the selected folder path
    inputFolderEntry.delete(0, tk.END)
    inputFolderEntry.insert(0, filename)
    # Force a display of all files in the new selected folder
    goRefreshFileList()

# Click GO button: launch merge files process

def goMergeSelected():
    filename = outputFileEntry.get()
    # If no output file has been selected, do nothing
    if (0 == len(filename)):
        infoLabel.updateText("Missing output file path and name")
        infoLabel.updateBg("red")
        return
    
    if (0 == len(fileList)) or (all(f.bSelected == False for f in fileList)):
        infoLabel.updateText("No input file selected")
        infoLabel.updateBg("red")
        return
    
    # Get full path of the output file
    filepath = inputFolderEntry.get()
    # Execute merge
    result = pdfMergeCore(filename, filepath)

    # Refresh fileBox with remaining files (selected one have been deleted)
    goRefreshFileList()

    # Display result if merge is executed
    if result:
        infoLabel.updateText("Done")
        infoLabel.updateBg("Green")

# Display the dialog for browsing files

def goGetOutputFile():
    # Open output file name dialog box
    filename = filedialog.asksaveasfilename(confirmoverwrite=True, defaultextension=".pdf")
    # Update entry
    outputFileEntry.delete(0, tk.END)
    outputFileEntry.insert(0, filename)

def splitfile():
    # Check that only one file is selected
    selected_files = [f for f in fileList if f.bSelected]
    if len(selected_files) != 1:
        infoLabel.updateText("Please select a single PDF file to split.")
        infoLabel.updateBg("red")
        return

    # Read the numeric value entered
    split_value_str = splitValueEntry.get().strip()
    if not split_value_str.isdigit():
        infoLabel.updateText("Please enter a positive integer for split.")
        infoLabel.updateBg("red")
        return
    split_value = int(split_value_str)
    if split_value < 1:
        infoLabel.updateText("Number of pages must be at least 1.")
        infoLabel.updateBg("red")
        return

    input_folder = inputFolderEntry.get()
    file_to_split = selected_files[0].name.strip()
    input_path = os.path.join(input_folder, file_to_split)

    try:
        from pypdf import PdfReader, PdfWriter
        reader = PdfReader(input_path)
        num_pages = len(reader.pages)
        if num_pages < split_value + 1:
            infoLabel.updateText(f"File doesn't have enough pages")
            infoLabel.updateBg("red")
            return
        # File with the first split_value pages
        first_writer = PdfWriter()
        for i in range(split_value):
            first_writer.add_page(reader.pages[i])
        first_out = os.path.splitext(input_path)[0] + f"_p1-{split_value}.pdf"
        with open(first_out, "wb") as f:
            first_writer.write(f)
        # File with the remaining pages
        rest_writer = PdfWriter()
        for i in range(split_value, num_pages):
            rest_writer.add_page(reader.pages[i])
        rest_out = os.path.splitext(input_path)[0] + f"_p{split_value+1}-end.pdf"
        with open(rest_out, "wb") as f:
            rest_writer.write(f)
        # Delete the original file
        os.remove(input_path)
        # Refresh the file list
        goRefreshFileList()
        infoLabel.updateText("Done")
        infoLabel.updateBg("green")
    except Exception as e:
        infoLabel.updateText(f"Error during split")
        infoLabel.updateBg("red")

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
    bw = 1
    bh = 1
else:
    photo1 = PhotoImage(file="D:\\Projects\\PDFMerge\\Images\\unionjack.png")
    bw = 25
    bh = 20


tk.Button(
    master = languageFrame,
    text="",
    width=bw,
    height=bh,
    bg="#f0efd5",
    fg="#788f82",
    font='None 8 bold',
    command = langChangeEnglish,
    image=photo1
).pack(side=tk.LEFT)

if __NOIMAGE__:
    photo2 = ""
    bw = 1
    bh = 1
else:
    photo2 = PhotoImage(file="D:\\Projects\\PDFMerge\\Images\\frenchflag.png")
    bw = 25
    bh = 20

tk.Button(
    master = languageFrame,
    text="",
    width=bw,
    height=bh,
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
inputLabel = labelText(inputFrame,"Input Folder",l)
allLabels.append(inputLabel)

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
# Add vertical scrollbar for fileBox
fileBoxScrollbar = tk.Scrollbar(fileFrame, orient="vertical", command=fileBox.yview)
fileBox.config(yscrollcommand=fileBoxScrollbar.set)
fileBox.pack(side=tk.LEFT,padx=5,pady=5)
fileBoxScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Support du scroll souris/trackpad dans fileBox
import platform

def _on_mousewheel(event):
    # Amplification pour macOS
    if platform.system() == 'Darwin':
        factor = 4  # Peut être ajusté selon le confort
        fileBox.yview_scroll(int(-1 * event.delta / 10 * factor), "units")
    else:
        fileBox.yview_scroll(int(-1 * (event.delta / 120)), "units")

fileBox.bind("<MouseWheel>", _on_mousewheel)
fileBox.bind("<Enter>", lambda e: fileBox.focus_set())
# Linux
fileBox.bind("<Button-4>", lambda e: fileBox.yview_scroll(-1, "units"))
fileBox.bind("<Button-5>", lambda e: fileBox.yview_scroll(1, "units"))

#Create tag for file Box. Tag is used to differentiate file name entries when clicked. Tag is bind to click
fileBox.tag_config("tag", foreground="#788f82")
fileBox.tag_bind("tag", "<Button-1>", fileClicked)
fileBox.tag_config("select", background="#f0efd5")
#disable all other binds for fileBox: now a Click in the file box will only execute the event bind to "tag". It avoids text selection
fileBox.bindtags((str(fileBox), str(window), "all"))

if __NOIMAGE__:
    photo = ""
    bw = 3
    bh = 1
else:
    photo = PhotoImage(file="D:\\Projects\\PDFMerge\\Images\\path1.png")
    bw = 50
    bh = 50

#Refresh Button
tk.Button(
    master = fileFrame,
    text="< >",
    width=bw,
    height=bh,
    bg="#f0efd5",
    fg="#788f82",
    font='None 12 bold',
    command = goRefreshFileList,
    image=photo
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
).pack(side=tk.LEFT, padx=5, pady=5)

# Sous-frame pour champ numérique, centré au-dessus du bouton Split
goSplitFrame = tk.Frame(goFrame)
goSplitFrame.pack(side=tk.LEFT, padx=5)

splitValueEntry = tk.Entry(
    master=goSplitFrame,
    width=5,
    font='None 10',
    justify='center'
)
splitValueEntry.pack(pady=(0,2))

# Split Button (hauteur réduite sous le champ)
tk.Button(
    master=goSplitFrame,
    text="Split",
    width=10,
    height=2,
    bg="#f0efd5",
    fg="#788f82",
    command=splitfile
).pack()

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

#
#
# Version frame, with version label only
#
#
version = __VERSION__
versionFrame = tk.Frame(
    relief=tk.FLAT,
    borderwidth=2,
    width=50
    )

version_label = tk.Label(versionFrame, text=f"Version {version}", anchor="w")
version_label.pack()

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
versionFrame.pack(pady=5)

#run
window.mainloop()