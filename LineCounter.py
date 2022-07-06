
# Line counter
import os
import json
import platform
from optparse import OptionParser

############################################################################################################
#######################################Parse command line arguments and validate them#######################
############################################################################################################

# CLI options parser (i.e., -r ./YOUR_FILE -f "py|html")
parser = OptionParser()
parser.add_option("-r","--root",dest="rootFolder",help="Location of root directory containing code.")
parser.add_option("-f","--filefilter",dest="fileFilter",help="Pattern for included file paths (i.e., \"py|html\").")
parser.add_option("-o","--outputpath",dest="outputPath",help="Specify name of results file and its path.")
(options,args) = parser.parse_args()

# Check if arguments are not provided
if not (options.rootFolder):
    print("Please provide the root folder of your project.")
    exit()

if not (options.fileFilter):
    print("Please provide a file inclusion filter. (i.e., py|html|css)")
    exit()

if not (options.outputPath):
    print("Please provide a location for the results.")
    exit()

# Check if root folder doesn't exist
if not os.path.exists(options.rootFolder):
    print("Root folder does not exist. Please ensure you have typed the correct folder path.")
    exit()

######################################################################################################
####################################Determine file path seperator#####################################
######################################################################################################
filePathSeperator = "\\" if platform.system() == "Windows" else "/"

######################################################################################################
###########################Check if directory has been specified in output file path##################
######################################################################################################
pathParts = options.outputPath.split(filePathSeperator)

# /folder/results.json
rootDirectory = pathParts[:-1]
print(rootDirectory)
root = filePathSeperator.join(rootDirectory)
fileName = pathParts[-1]

# If file is within a folder
# results.json
# linecount.json
if len(root) > 0:
    if not os.path.exists(root):
        print("Output directory does not exist. Please create the directory first.")
        exit()

############################################################################################################
#######################################Retrieve project file paths##########################################
############################################################################################################

# Retrieve file names recursively
filePaths = []
for root, dirs, files in os.walk(options.rootFolder,topdown=False):
    for name in files:
        filePaths.append(os.path.join(root,name))


includedFileExtensions = options.fileFilter.split("|")
lineCounts = {
    "lineCountBreakdownPerFile": {

    },
    "lineCountBreakdownPerType": {

    },
    "totalLines": 0
}

for filePath in filePaths:
    extension = filePath.split(".")[-1]
    if extension in includedFileExtensions:
        with open(filePath) as file:
            fileData = file.read()
            lines = fileData.split("\n")
            numLines = len(lines)

            # Set linecount for file
            lineCounts["lineCountBreakdownPerFile"][filePath] = numLines

            # Check if extension does not exist in lineCountBreakDownPerType
            if not (extension in lineCounts["lineCountBreakdownPerType"]):
                lineCounts["lineCountBreakdownPerType"][extension] = 0

            # Update linecounts for file extension
            lineCounts["lineCountBreakdownPerType"][extension] += numLines

            # Update total number of lines
            lineCounts["totalLines"] += numLines

with open(options.outputPath,"w") as file:
    file.write(json.dumps(lineCounts,indent=4))
