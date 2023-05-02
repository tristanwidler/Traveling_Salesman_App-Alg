import os

packageFilePath = "files\\WGUPS_Package_File.csv"
distanceFilePath = "files\\WGUPS_Distance_Table.csv"

projectRoot = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", ".."))


def getPackagePath():
    return os.path.join(projectRoot, packageFilePath)


def getDistancePath():
    return os.path.join(projectRoot, distanceFilePath)
