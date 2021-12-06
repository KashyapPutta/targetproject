#!/usr/bin/python3
import sys
import subprocess
import json

def monitorFileSystem(mountInput):
    fileSystemData = subprocess.check_output(
        "MOUNTPOINT=%s && cd $MOUNTPOINT && cat /proc/mounts"
        "| grep $MOUNTPOINT"
        "| awk '{print $2}'"
        "| xargs ls"
        "| awk '{print substr($0, index($0,$1))}'"
        "| xargs -d '\n' du"
        "| awk -v OFS=\"#\" '{print $1, substr($0, index($0,$2))}'" % (mountInput), stderr=subprocess.STDOUT, shell=True).decode("utf-8")
    rawFileList = fileSystemData.split("\n")
    fileSystemDict = {}
    fileList = []
    for file in rawFileList:
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
                print("Invalid file data found and skipped filename: %s" % File)
    fileSystemDict["files"] = fileList
    return fileSystemDict

def main():
    try:
        mountInput = sys.argv[1]
        fileSystemDict = monitorFileSystem(mountInput)
        print(json.dumps(fileSystemDict, indent=1).replace("\\",""))
    except subprocess.CalledProcessError as e:
        print("Exception occured: {}".format(e.output))

main()
