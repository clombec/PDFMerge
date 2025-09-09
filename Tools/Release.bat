cd ..
cd code 
pyinstaller -F pdfmergeGUI.py
rem this command may generate a windows virus error
rem see https://stackoverflow.com/questions/77346372/pyinstaller-says-i-made-a-virus

cd dist
xcopy pdfmergeGUI.exe Z:\Lombec\Maison\Scanner /Y

cd ../../Tools
