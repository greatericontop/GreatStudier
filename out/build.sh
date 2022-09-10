# Run me to compile to a binary using PyInstaller.
# The output file should be in the 'dist' directory.

# NOTES:
# - Weakly encrypt/obfuscate the code to hopefully prevent antivirus falses. (GreatStudier is still GPL3)
# - Both `rapidfuzz` and its dependency `jarowinkler` need to be all-submodule-imported.

if [ "$1" == "clean" ]; then
  pyinstaller --onefile --key GREATSTUDIER --clean ../main.py
else
  pyinstaller --onefile --key GREATSTUDIER ../main.py
fi