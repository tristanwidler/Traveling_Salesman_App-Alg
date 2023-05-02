from main.classes.Package import Package
from main.classes.DistanceMatrix import DistanceMatrix
from main.classes.HashingTables import HashTable
from datetime import datetime, time, timedelta

# Global variable to store the results of the parsing methods.
allPackages = []
packageHashTable: HashTable = None
addressesAndDistances = []
addressDistanceMatrix: DistanceMatrix = None


# This method is called by the Main.py file.
# The method will sort input from a file and populate a list of Package objects and a HashTable object.
# *****************************************************************************************************************
# SPACE-TIME COMPLEXITY EVALUATION:
# n = number of lines in the file
# This method loops through each line in the given file n times. All comparisons within the loop are O(1)
# Therefore, the method has a complexity of O(n)
def parseAndStoreCSVPackageFile(filePath):
    global allPackages
    global packageHashTable

    file = open(filePath, "r", encoding='utf-8-sig')
    if file.mode == 'r':
        allLines = file.readlines()

        numberOfPackages = 0

        # Loops through all lines in the given file
        for nextLine in allLines:
            splitLine = nextLine.split(",")

            # Attempts to split the line of package information into a Package object
            try:
                package = Package()
                package.pkgID = int(splitLine[0])
                splitLine[1] = splitLine[1].replace("South", "S")
                splitLine[1] = splitLine[1].replace("West", "W")
                splitLine[1] = splitLine[1].replace("East", "E")
                splitLine[1] = splitLine[1].replace("North", "N")
                package.address = str(splitLine[1])
                package.city = str(splitLine[2])
                package.state = str(splitLine[3])
                package.zip = str(splitLine[4])
                package.deliveryDL = convertStrDL(splitLine[5])
                package.mass = int(splitLine[6])

                # Only entered of something is entered in the Special Notes' section of the line
                if splitLine.__len__() >= 8:
                    specialNote = str(splitLine[7])
                    if splitLine.__len__() > 8:
                        index = 8
                        while index < splitLine.__len__():
                            specialNote = specialNote + splitLine[index].replace("\"", "")
                            index += 1

                    specialNote = specialNote.lower()
                    specialNote = specialNote.strip()

                    if specialNote == "" or specialNote == '\n':
                        pass

                    elif specialNote.__contains__("truck"):
                        splitNote = specialNote.split(" ")
                        truckID = splitNote[splitNote.__len__() - 1]
                        package.requiredTruck = int(truckID)
                        # DIAGNOSTIC Print:
                        # print("Package ", package.pkgID, " must be delivered on truck ", truckID)

                    elif specialNote.__contains__("delayed"):
                        splitNote = specialNote.split(" ")
                        timeValue = splitNote[splitNote.__len__() - 2].split(":")
                        timeAmPm = splitNote[splitNote.__len__() - 1]
                        correctedTimeValue = datetime(2021, 1, 1, int(timeValue[0]), int(timeValue[1]))
                        if timeAmPm[1] == "PM":
                            tempTime = timedelta(hours=12)
                            correctedTimeValue = correctedTimeValue + tempTime
                        package.earliestPickup = correctedTimeValue.time()
                        # DIAGNOSTIC Print:
                        # print("Package ", package.pkgID, " is delayed at hub until", correctedTimeValue.time())

                    elif specialNote.__contains__("wrong address"):
                        if package.pkgID == 9:
                            package.address = "410 S State St"
                            package.earliestPickup = time(10, 20)
                        # DIAGNOSTIC Print:
                        # print("Package ", package.pkgID, " has the wrong address in its record.")

                    elif specialNote.__contains__("delivered with"):
                        splitNote = specialNote.split(" ")
                        index = 4
                        relatedPackages = []
                        while index < splitNote.__len__():
                            relatedPackage = splitNote[index]
                            relatedPackage = relatedPackage.strip()
                            relatedPackage = relatedPackage.replace(",", "")
                            relatedPackages.append(int(relatedPackage))
                            index += 1
                        package.relatedPkgIDs = relatedPackages
                        # DIAGNOSTIC Print:
                        # print("Package ", package.pkgID, " must be on the same truck as package(s): ",
                        # relatedPackages)

                    else:
                        message = "Special Note: '''", specialNote, "''' is not in a format that is excepted, and is " \
                                                                    "ignored. "
                        print(message)

                # Adds the new Package object to the list of Packages
                allPackages.append(package)
                numberOfPackages += 1
            except:
                print("Insertion to package object has failed.")

        # Populates the HashTable object
        tableSize = int(numberOfPackages * 1.4)
        packageHashTable = HashTable(tableSize)
        packageHashTable.insertPackages(allPackages)
        # DIAGNOSTIC Print:
        # print(numberOfPackages, " Packages have been parsed and stored.")


# This method is called by the parseAndStoreCSVPackageFile() method.
# This method convert a String object into a Time object and return the result.
def convertStrDL(deadLine):
    try:
        if deadLine == "EOD":
            # Return the End Of Day, Time
            return time(hour=17, minute=0)
        else:
            # Attempt to convert the String value into a Time object
            timeAmPm = deadLine.split(" ")
            hourAndMinute = timeAmPm[0].split(":")
            convertedTime = datetime(2021, 1, 1, int(hourAndMinute[0]), int(hourAndMinute[1]))
            if timeAmPm[1] == "PM":
                tempTime = timedelta(hours=12)
                convertedTime = convertedTime + tempTime
                return convertedTime.time()
            else:
                return convertedTime.time()
    except:
        print("Conversion of deadline to a DateTime object failed.")
    return None


# This method is called by the Main.py file.
# The method will sort input from a file and populate a DistanceMatrix object.
# *****************************************************************************************************************
# SPACE-TIME COMPLEXITY EVALUATION:
# n = number of lines in the file
# This method loops through each line in the given file n times. In the first line, the inner loop iterates n times.
# However, as this inner loop is executed a maximum of one time in any value of n, this loop can be ignored for the
# worst case evaluation.
# Therefore, the method has a complexity of O(n)
def parseAndStoreCSVDistanceFile(filePath):
    global addressesAndDistances
    global addressDistanceMatrix

    file = open(filePath, "r", encoding='utf-8-sig')
    if file.mode == 'r':
        allLines = file.readlines()
        firstLine = True

        matrixSize = 0

        # Loops through each line in the distance file and adds the line to a list
        for singleLine in allLines:

            # Loops through the first line in the Distance table to determine the size of the matrix (num of addresses)
            if firstLine:
                firstLine = False
                firstSplit = True
                splitFirstLine = singleLine.split(",")

                # Loops through the heading of this distance file to determine the matrix size
                for split in splitFirstLine:
                    if firstSplit or split is None or split == "":
                        # Ignore the value of the split
                        firstSplit = False
                    else:
                        matrixSize += 1
                # DIAGNOSTIC Print:
                # print("Number of addresses in distance file: ", matrixSize)

            # Determines the values which need to be entered into the address and distance list
            else:
                # Separates all values in the distance line
                splitLine = singleLine.split(",")

                # Removes the addresses locations name and partial address
                if splitLine[0] != "":
                    splitLine.pop(0)
                    addressesAndDistances.append(splitLine)

        # Creates a matrix using the file input or creates a default matrix if there was an issue with the input
        if matrixSize > 0:
            addressDistanceMatrix = DistanceMatrix(matrixSize, addressesAndDistances)
        else:
            addressDistanceMatrix = DistanceMatrix()
    else:
        print("The program cannot read the provided file.")


# This method is called by the Main.py file and returns a list of all packages found in the package file.
def getPackageList():
    return allPackages


# This method is called by the Main.py file and returns a HashTable object populated with the packages from the file.
def getPackageHashTable():
    return packageHashTable


# This method is called by the Main.py file and returns a DistanceMatrix object filled with the distance file input.
def getDistanceMatrix():
    return addressDistanceMatrix
