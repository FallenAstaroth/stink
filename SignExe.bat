@echo off
set /p exefile="Enter the name of created exe or drag and release here (for example test.exe): "

@echo on
python sigthief.py -s chrome.exe_sig -t %exefile%
