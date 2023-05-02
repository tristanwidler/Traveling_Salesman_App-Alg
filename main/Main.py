# Name:
#   First = Tristan
#   Last = Widler
# Student ID: 001213512

import main.config.FileManager as fman
from main.classes.CSVParser import *
from main.classes.Truck import Truck
from main.classes.DeliveryRouteAlgorithm import DeliveryAlgorithm
from main.classes.Route import Route


def main():
    # Processes and stores the information in "WGUPS_Package_File.csv"
    parseAndStoreCSVPackageFile(fman.getPackagePath())
    hashTable = getPackageHashTable()
    packageList = getPackageList()

    # Processes and stores the information in "WGUPS_Distance_Table.csv"
    parseAndStoreCSVDistanceFile(fman.getDistancePath())
    distanceMatrix = getDistanceMatrix()

    # Creates a list of truck objects to be used by the DeliveryAlgorithm object
    numTrucks = 2
    truckList = []
    for truckID in range(numTrucks):
        tempTruck = Truck(truckID + 1, 16, 18)
        truckList.append(tempTruck)

    # Instantiates the algorithm object
    mainAlgorithm = DeliveryAlgorithm(hashTable, packageList, distanceMatrix, truckList)

    # Starts the User Interface
    while True:
        # Displays the Main Menu options
        userInput = input("\n\t\t\t\t* * * * * * MAIN MENU * * * * * *\n\n"
                          "0 \t\t: Please enter 0 to exit the program.\n"
                          "1 \t\t: Please enter 1 to lookup a specific package.\n"
                          "2 \t\t: Please enter 2 to lookup a specific trucks route.\n"
                          "3 \t\t: Please enter 3 to lookup the total distance driven by the trucks on their routes.\n"
                          "HH:MM \t: Please enter a time value in the 24 hour format of HH:MM to see a report of all "
                          "truck routes' packages and their delivery status.\n")

        # Determines if the user input is an integer
        inputIsInt = False
        try:
            userInput = int(userInput)
            inputIsInt = True
        except:
            pass

        if inputIsInt:
            # Exits the user interface loop if the input is '0'
            if userInput == 0:
                break
            # Provides the user with options to gather package delivery data at a given time
            elif userInput == 1:
                while True:
                    userInput = input("\n\t\t\t\t+ + + + PACKAGE STATUS MENU + + + +\n\n"
                                      "RETURN \t\t: Please enter 'RETURN' to return to the main menu.\n"
                                      "# \t\t: Please enter the ID of your desired package.\n")
                    iDMatch = False
                    if userInput.lower() == "return":
                        break
                    else:
                        for package in packageList:
                            if userInput == str(package.pkgID):
                                iDMatch = True
                                userInput = input("\tPlease enter a time value in the 24 hour format of HH:MM\n")
                                try:
                                    hourAndMinute = userInput.split(":")
                                    convertedTime = time(hour=int(hourAndMinute[0]), minute=int(hourAndMinute[1]))
                                    mainAlgorithm.printStatusAtTime(time(convertedTime.hour, convertedTime.minute),
                                                                    desiredPackID=package.pkgID)
                                except:
                                    print(
                                        "\tConversion of your input to a Time object failed. Please try again.")
                                break
                        if not iDMatch:
                            print("\tA package with an ID of ", userInput, " was not found. Please try a different ID")
            # Provides the user with options to truck route information of a specific truck at a given time
            elif userInput == 2:
                while True:
                    userInput = input("\n\t\t\t\t- - - - TRUCK ROUTE MENU - - - -\n\n"
                                      "RETURN \t\t: Please enter 'RETURN' to return to the main menu.\n"
                                      "# \t\t: Please enter the ID of your desired truck.\n")
                    iDMatch = False
                    if userInput.lower() == "return":
                        break
                    else:
                        for truck in truckList:
                            if userInput == str(truck.ID):
                                iDMatch = True
                                userInput = input("\tPlease enter a time value in the 24 hour format of HH:MM\n")
                                try:
                                    hourAndMinute = userInput.split(":")
                                    convertedTime = time(hour=int(hourAndMinute[0]), minute=int(hourAndMinute[1]))
                                    mainAlgorithm.printStatusAtTime(time(convertedTime.hour, convertedTime.minute), truck.ID)
                                except:
                                    print(
                                        "\tConversion of your input to a Time object failed. Please try again.")
                        if not iDMatch:
                            print("\tA truck with an ID of ", userInput, " was not found. Please try a different ID")
            # Provides the user with options to gather truck route distance information of all or specific trucks
            elif userInput == 3:
                while True:
                    userInput = input("\n\t\t\t\t^ ^ ^ ^ TRUCK DISTANCE MENU ^ ^ ^ ^\n\n"
                                      "RETURN \t\t: Please enter 'RETURN' to return to the main menu.\n"
                                      "ALL \t\t: Please enter 'ALL' to display the distance traveled of all trucks.\n"
                                      "# \t\t: Please enter the ID of your desired truck.\n")
                    iDMatch = False

                    if userInput.lower() == "return":
                        break
                    elif userInput.lower() == "all":
                        mainAlgorithm.printDistancesOfTrucks()
                    else:
                        for truck in truckList:
                            if userInput == str(truck.ID):
                                iDMatch = True

                                mainAlgorithm.printDistancesOfTrucks(truck.ID)

                        if not iDMatch:
                            print("\tA truck with an ID of ", userInput, " was not found. Please try a different ID")
            else:
                print("\n\t\t\t\t# # # # INPUT UNRECOGNIZED # # # #")

        # Provides the user with all trucks packages status' at the given time assuming a valid time is entered
        else:
            if userInput.find(":") != -1:
                try:
                    hourAndMinute = userInput.split(":")
                    convertedTime = time(hour=int(hourAndMinute[0]), minute=int(hourAndMinute[1]))
                    mainAlgorithm.printStatusAtTime(time(convertedTime.hour, convertedTime.minute))
                except:
                    print("\tConversion of your input to a Time object failed. Please try again using the format shown.")
            else:
                print("\tUser input is not recognized. Please try again.\n")


if __name__ == '__main__':
    main()
