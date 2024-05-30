cd ../code 
pyinstaller -F pdfmergeGUI.py

cd dist
xcopy pdfmergeGUI.exe Z:\Lombec\Maison\Scanner /Y

cd ../../Tools
