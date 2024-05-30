from pypdf import PdfWriter
import os

def fourdigits(i):
    if i < 10:
        return "000" + str(i)
    elif i < 100:
        return "00" + str(i)
    elif i < 1000:
        return "0" + str(i)
    else:
        return str(i)
        

def pdfMergeCore(nbFiles, fileName, destPath, sourcePath):
    print(str(nbFiles) + fileName + destPath + sourcePath)
    merger = PdfWriter()

    i = 1
    while i <= nbFiles:
        print ("Merging " + sourcePath + '\\IMAG' + fourdigits(i) + '.pdf')
        merger.append(sourcePath + '\\IMAG' + fourdigits(i) + '.pdf')
        i = i+1

    merger.write(destPath + fileName + ".pdf")
    merger.close()

    for i in os.listdir(sourcePath):
        #print (i)
        if i.endswith('.PDF'):
            os.remove(sourcePath + "\\" + i)

"""
# Ce chemin doit être adapté au dossier qui contient les pdf scannés, en cas de changement, ne pas oublier les doubles \\
path = "D:\\DCIM\\113MEDIA"

# Ce chemin est le dossier par défaut dans lequel sera enregistré le fichier pdf généré. Il peut être modifié, mais ne pas oublier les doubles \\, ainsi que le \\ final
destFolder = "C:\\Users\\Admin\\Dropbox\\Personnel\\ScanTemp\\"

total = input("Combien de pages ?")  # Python 3
totalNb = int(total)
print(totalNb)
#print(fourdigits(totalNb))

file = input("Nom du fichier de sortie ?")  # Python 3

pdfMergeCore(totalNb, file, destFolder, path)
"""