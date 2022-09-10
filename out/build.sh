\# Run me to compile to a binary using PyInstaller.
# The output file should be in the 'dist' directory.

# NOTES:
# - Weakly encrypt/obfuscate the code to hopefully prevent antivirus falses. (GreatStudier is still GPL3)
# - Both `rapidfuzz` and its dependency `jarowinkler` need to be all-submodule-imported.

pyinstaller --onefile --clean --key GREATSTUDIER ../main.py
