# 3DS-Max-Converter
This script interfaces with 3DS Max using the MaxPlus language in order to automate the conversion of 3D model files between different file formats.

## Preparation
To use this script, 3DS Max must be installed. As noted in the code, 3DS Max has some problems importing Tkinter. To fix this, install the version of Python corresponding to your copy of 3DS Max. For 3DS Max 2020, this is Python 2.7.15. Once installed, navigate to C:/YourPython27InstallationDirectory/tcl and copy the tk8.5 and tcl8.5 directories to the C:/Program Files/Autodesk/Your 3ds Max version/python/Lib directory. You may need to create the Lib directory yourself.

## How to run the code
To run the script, do the following:
1. Open the MAXScript Listener window in 3DS Max.
![Step 1](https://user-images.githubusercontent.com/14677252/69062584-2752f700-09e9-11ea-934b-ae691d4cfc3f.png)
2. Switch from the MaxPlus language to Python.
![Step 2](https://user-images.githubusercontent.com/14677252/69062617-3174f580-09e9-11ea-901c-c90b66f7db74.png)
3. Load the .py script file and run it from the MAXScript Listener window.
![Step 3a](https://user-images.githubusercontent.com/14677252/69062627-3639a980-09e9-11ea-94d6-75ff8b590898.png)
![Step 3b](https://user-images.githubusercontent.com/14677252/69062635-3a65c700-09e9-11ea-89a7-8252c2cff3aa.png)
4. Follow any prompts that pop up.
![Step 4](https://user-images.githubusercontent.com/14677252/69062648-3e91e480-09e9-11ea-860d-fd872df1bf38.png)

## Troubleshooting
If you receive an error saying that there is a version conflict for either the Tcl or the Tk package, go into the tcl8.5 and tk8.5 directories you copied over in the [Preparation section](#preparation) above.

### In the tcl8.5 directory:
1. Open the init.tcl file.
2. Find the line of code that looks like this:
```python
package require -exact Tcl #.#.#
```
3. The error message you received tells you what version of Tcl you already have and what version of Tcl you need. Replace the version number from the line in step 2 with the version number that the error message says you need.

### In the tk8.5 directory:
1. Open the tk.tcl file.
2. Find the line of code that looks like this:
```python
package require -exact Tk  #.#.#
```
3. The error message you received tells you what version of Tk you already have and what version of Tk you need. Replace the version number from the line in step 2 with the version number that the error message says you need.
