# Communicate between 3DS Max and python

import MaxPlus
import time
import sys
from os import listdir
from os.path import isfile, join, splitext, isdir

sys.path.append(r"C:\Python27\Lib\lib-tk")

# Note: 3DS Max runs into problems with importing Tkinter. The tcl8.5 and tk8.5 directories need to be moved into the
# program folder for 3DS Max
import Tkinter
import tkFileDialog
import tkMessageBox


# Load and configure importer plugins
def configure_importers():
    # CONFIGURE IMPORTER
    # TODO: Configure importers based on file type? Could account for possibility of variety of files
    # Convert to mesh
    MaxPlus.Core.EvalMAXScript("ATF_IGES_importer.ConvertToMesh = true")
    MaxPlus.Core.EvalMAXScript("ATF_JT_importer.ConvertToMesh = true")

    # Keep hierarchy
    MaxPlus.Core.EvalMAXScript("ATF_IGES_importer.HierarchyMode = #UsingGrouping")
    MaxPlus.Core.EvalMAXScript("ATF_JT_importer.HierarchyMode = #UsingGrouping")

    # Mesh resolution set to -10
    MaxPlus.Core.EvalMAXScript("ATF_IGES_importer.MeshResolution = -10")
    MaxPlus.Core.EvalMAXScript("ATF_JT_importer.MeshResolution = -10")

    # Axis set to z-up
    MaxPlus.Core.EvalMAXScript("ATF_IGES_importer.UpAxis = #z")
    MaxPlus.Core.EvalMAXScript("ATF_JT_importer.UpAxis = #z")


# Filter out the files we don't want to import, import the ones that we do want
def filter_files(path, subdirectories, text):
    for item in listdir(path):  # list all items in import directory
        subpath = join(path, item)  # get the absolute path of that item

        # Is the item in the directory a file or a subdirectory?
        if isdir(subpath):  # item is a directory
            subdirectories.append(subpath)

        elif isfile(subpath):  # item is a file
            extension = splitext(item)[1].lower()  # Split extension from file name, normalize to lowercase.

            # check to see if the file is the correct type (.igs)
            if extension == ".igs" or ".jt":
                text.write(item + "\n")
                start = time.time()
                fileManagerIn.Import(subpath, True)  # True suppresses the import window popup
                end = time.time()
                text.write(str(end - start) + "\n")

            # file is a project based file and should be removed
            else:
                pass


# Traverse any subdirectories in the import directory to find other files to convert
def traverse_subdirectories(subdirectories, text):
    # Were there subdirectories?
    if subdirectories:
        for directory in subdirectories:
            filter_files(directory, subdirectories, text)

    return


# Export the files to FBX format
def export_files(path_out, text):

    # NOTE: 3DS Max ran into problems when trying to evaluate using the full parameter path
    # (e.g., MaxPlus.Core.EvalMAXScript("FbxExporterSetParam #Export|IncludeGrp|LightGrp|Light False")
    # To bypass this, I have used the parameter names instead

    # Load and configure FBX exporter
    MaxPlus.Core.EvalMAXScript("pluginManager.loadClass FbxExporter")

    # Don't include lights
    MaxPlus.Core.EvalMAXScript("FbxExporterSetParam #Lights False")

    # Don't include cameras
    MaxPlus.Core.EvalMAXScript("FbxExporterSetParam #Cameras False")

    # Include smoothing groups
    MaxPlus.Core.EvalMAXScript("FbxExporterSetParam #SmoothingGroups True")

    # Include Turbosmooth (Note: parameter "SmoothMesh" is Turbosmooth)
    MaxPlus.Core.EvalMAXScript("FbxExporterSetParam #SmoothMeshExport True")

    # Include convert def dummies (Note: parameter "MaxBoneAsBone" is convert def dummies)
    MaxPlus.Core.EvalMAXScript("FbxExporterSetParam #GeomAsBone True")

    # Include preserve edge orientation
    MaxPlus.Core.EvalMAXScript("FbxExporterSetParam #PreserveEdgeOrientation True")

    # Create instantiated object
    selector = MaxPlus.SelectionManager

    geometry = MaxPlus.Core.GetRootNode().Children  # all the imported geometry

    for part in geometry:
        selector.ClearNodeSelection()
        selector.SelectNode(part)

        name = part.GetName()
        path = path_out + "/" + name

        text.write(name + "\n")
        start = time.time()
        fileManagerOut.ExportSelected(path, True)  # True suppresses the export popup window
        end = time.time()
        text.write(str(end - start) + "\n")
    return


def user_select(prompt):
    root = Tkinter.Tk()
    root.withdraw()  # hide root window

    while(True):
        folder = tkFileDialog.askdirectory(parent=root, initialdir="/", title=prompt)

        # user picked a valid folder
        if len(folder) > 0:
            print(folder)
        # user did not pick a valid folder and chose to cancel or X out of the window
        else:
            tkMessageBox.showinfo("Attention", "You have chosen to quit the program.")

        return folder


# Global variables
directories = []  # empty array of directories to traverse

# For timing purposes when debugging
importLog = open('import log.txt', 'w')
exportLog = open('export log.txt', 'w')

sys.path.append("C://Python27")

importPath = user_select('Select the folder of files to import.')

# user chose valid import directory
if(importPath):
    exportPath = user_select('Select the folder to send the exports.')

    # user chose valid export directory
    if(exportPath):
        # Must create instantiated objects
        fileManagerIn = MaxPlus.FileManager
        fileManagerOut = MaxPlus.FileManager
        pathManagerIn = MaxPlus.PathManager
        pathManagerOut = MaxPlus.PathManager

        pathManagerIn.SetImportDir(importPath)
        getImport = pathManagerIn.GetImportDir()

        pathManagerOut.SetExportDir(exportPath)  # Needs to run every time or script will use old export directory
        getExport = pathManagerOut.GetExportDir()

        # prevent imported items from appearing in display port to speed up conversion process
        viewManager = MaxPlus.ViewportManager
        viewManager.GetActiveViewport()
        viewManager.DisableSceneRedraw()

        configure_importers()

        filter_files(importPath, directories, importLog)

        traverse_subdirectories(directories, importLog)

        export_files(getExport, exportLog)

        # re-enable rendering of items in display port
        viewManager.EnableSceneRedraw()
