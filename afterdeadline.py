#! /usr/bin/python3
import subprocess
import json
import sys

def monitorFileSystem(mountInput):
    fileSystemData = subprocess.check_output(
        "MOUNTPOINT=%s && cd $MOUNTPOINT"
        "| find . -type f"
        "| awk '{print substr($0, 3)}'"
        "| xargs -d '\n' du"
        "| awk -v OFS=\"#\" '{print $1, substr($0, index($0,$2))}'" % (mountInput), stderr=subprocess.STDOUT, shell=True).decode("utf-8")
    list1 = fileSystemData.split("\n")
    fileSystemDict = {}
    fileList = []
    for file in list1:
        if file != '':
            splitlist = file.split('#',1)
            if len(splitlist) >= 2:
                individualFile = {}
                fileAbsolutePath = "{mountInput}/{fileName}".format(mountInput=mountInput,
                                                                            fileName=splitlist[1])
                fileSize = splitlist[0]
                individualFile[fileAbsolutePath] = fileSize
                fileList.append(individualFile)
            else:
                print("Invalid file contents. Less than 2 elements in splitList")
    fileSystemDict["files"] = fileList
    return fileSystemDict

def main():
    try:
        mountInput = sys.argv[1]
        fileSystemDict = monitorFileSystem(mountInput)
        print(json.dumps(fileSystemDict, indent=1))
    except subprocess.CalledProcessError as exception:
        print("Exception occured: {}".format(exception.output))

main()
