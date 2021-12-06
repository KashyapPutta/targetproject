#!/usr/bin/python3
import sys
import subprocess
import json

def monitorFileSystem(mountInput):
    fileSystemData = subprocess.check_output(
        "cd %s; cat /proc/mounts"
        "| grep -w %s"
        "| awk '{print $2}'"
        "| xargs ls"
        "| awk '{print substr($0, index($0,$1))}'"
        "| xargs -d '\n' du"
        "| awk -v OFS=\"#\" '{print $1, substr($0, index($0,$2))}'" % (mountInput, mountInput), shell=True).decode("utf-8")
    rawFileList = fileSystemData.split("\n")
    fileSystemDict = {}
    fileList = []
    for file in rawFileList:
        if file != '/':
            splitlist = file.split('#',1)
            if len(splitlist) >= 2:
                individualFile = {}
                fileAbsolutePath = "{mountInput}/{fileName}".format(mountInput=mountInput,
                                                                            fileName=splitlist[1])
                fileSize = splitlist[0]
                individualFile[fileAbsolutePath] = fileSize
                fileList.append(individualFile)
    fileSystemDict["files"] = fileList
    return fileSystemDict


def main():
    mountInput = sys.argv[1]
    # mountInput = "/Users/p2931556/PycharmProjects/targetproject/opt/twc/nationalnavigation/components/navigation/conf/symphoni"
    fileSystemDict = monitorFileSystem(mountInput)
    print(json.dumps(fileSystemDict, indent=1))


main()
