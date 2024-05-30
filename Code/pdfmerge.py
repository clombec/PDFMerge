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

