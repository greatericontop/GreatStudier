# Run me to compile to a binary using PyInstaller.
# The output file should be in the 'dist' directory.

# Weakly encrypt/obfuscate the code to hopefully prevent antivirus falses. (GreatStudier is still GPL3)

if [ $1 == "clean" ]; then
  pyinstaller --onefile --clean --key GREATSTUDIER ../main.py
else
  pyinstaller --onefile --key GREATSTUDIER ../main.py
fi
