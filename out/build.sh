# Run me to compile to a binary using PyInstaller.
# The output file should be in the 'dist' directory.
# This script should work for both Windows and Linux.

# NOTES:
# - Weakly encrypt/obfuscate the code to hopefully prevent antivirus falses. (GreatStudier is still GPL3)
# - To do a clean build, remove everything in this directory except for this file.

pyinstaller --onefile --key GREATSTUDIER ../main.py