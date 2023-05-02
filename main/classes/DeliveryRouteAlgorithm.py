from main.classes.HashingTables import HashTable
from main.classes.DistanceMatrix import DistanceMatrix
from main.classes.Truck import Truck
from main.classes.Package import Package
from operator import itemgetter, attrgetter
from datetime import time
from datetime import timedelta
from main.classes.Route import Route

# Global variables used by various methods within the DeliveryAlgorithm class
unvisitedPkgIDs = []
basePackageList = []
packagesOnATruck = []
currentlyAvailPkgIds = []
visitedPkgIDs = []
currentPkgIDs = ""
previousPkgIDs = []
tempRelatedIDs = []
relatedIDAr = [[]]
previousAddress = ""
previousID = 0
sameDestinationIDArr = [[]]
numPackagesInRoute = 0
currentDeliveryNumber = 0
deadLinePackages = []
isFirstPass = True


# This class determines the path of all trucks passed in as well as provides methods to view the results of the route
# planning process.
class DeliveryAlgorithm:

    # This acts as a constructor for the DeliveryAlgorithm class and plans the route for all packages and trucks given.
    def __init__(self, pkgHashTable=HashTable(), listOfPackages=[], distMatrix=DistanceMatrix(), listOfTrucks=[]):
        global unvisitedPkgIDs
        global currentlyAvailPkgIds
        global tempRelatedIDs
        global basePackageList
        global packagesOnATruck
        global relatedIDAr
        global previousAddress
        global previousID
        global sameDestinationIDArr
        global numPackagesInRoute
        global currentDeliveryNumber
        global deadLinePackages
        global isFirstPass

        self.pkgHashTable = pkgHashTable
        self.listOfPackages = listOfPackages
        self.distMatrix = distMatrix
        self.listOfTrucks = listOfTrucks
        self.hubAddress = "4001 S 700 E Salt Lake City UT"
        for package in self.listOfPackages:
            unvisitedPkgIDs.append(package.pkgID)
            basePackageList.append(package.pkgID)
        self.findDeliveryRoute()

    # This method is called when the DeliveryAlgorithm object is initialized.
    # The method will use the base package list to fill the Truck objects and determine the optimal route for each truck
    # *****************************************************************************************************************
    # SPACE-TIME COMPLEXITY EVALUATION:
    # n = number of packages in the base package list
    # k = number of trucks
    # The method loops through all trucks in the listOfTrucks once(k).
    # In each loop through the truck object, fillTruck() is called and planTruckRoute() is called.
    # fillTruck() has a complexity of O(n^2)
    # planTruckRoute() has a complexity of O(n^2)
    # Therefore the methods' complexity is (k * n^4)
    def findDeliveryRoute(self):
        global isFirstPass
        self.populateRelatedID()
        self.popIDsOfSameDestination()
        self.popDeadlinePackages()

        passNum = 1

        while packagesOnATruck.__len__() < basePackageList.__len__():
            # DIAGNOSTIC Print:
            # print("\n\n\t\t\tPass Number: ", passNum, "\n\n")
            for truck in self.listOfTrucks:
                self.fillTruck(truck)
                self.planTruckRoute(truck)
            totalDistTraveled = 0
            # DIAGNOSTIC Prints:
            # for truck in self.listOfTrucks:
            # totalRouteDist = truck.truckRoute.calcTotalDistanceOfRoute()
            # truck.truckRoute.printPathAndDist(self.pkgHashTable)
            # print("Total Route distance of truck ", truck.ID, " is ", totalRouteDist)
            # totalDistTraveled += totalRouteDist
            # print("Total Dist Traveled: ", totalDistTraveled)
            # passNum += 1
            isFirstPass = False

    # This method is called by the findDeliveryRoute(self) method.
    # The method will use the package list of the Truck object to determine a route to follow.
    # *****************************************************************************************************************
    # SPACE-TIME COMPLEXITY EVALUATION:
    # n = number of packages in the truck
    # The worst case scenarios assume the truck that is passed in holds all packages from the package file.
    # The method will loop through the length of all packages originally in the truck (n). Each iteration of the loop
    # then call the findIdealNextAddress() method which has O(n).
    # This results in a complexity of O(n^2)
    def planTruckRoute(self, truck: Truck):
        global numPackagesInRoute
        global currentDeliveryNumber

        if truck.packageIDs.__len__() >= 1:
            firstPass = True
            halfwayPoint = truck.packageIDs.__len__() / 2
            currentDeliveryNumber = 0
            numPackagesInRoute = truck.packageIDs.__len__()
            # change packageID to packageNum
            for packageID in range(numPackagesInRoute + 2):
                if firstPass:
                    firstPass = False
                    self.findIdealNextAddress(1, truck)
                    currentDeliveryNumber += 1
                elif currentDeliveryNumber <= halfwayPoint and truck.packageIDs.__len__() >= 1:
                    self.findIdealNextAddress(2, truck, previousAddress)
                    currentDeliveryNumber += 1
                elif halfwayPoint < currentDeliveryNumber <= numPackagesInRoute:
                    self.findIdealNextAddress(3, truck, previousAddress)
                    currentDeliveryNumber += 1
                elif currentDeliveryNumber > numPackagesInRoute:
                    self.findIdealNextAddress(4, truck, previousAddress)
                else:
                    print("There has been an Error in DeliveryRouteAlgorithm.planTruckRoute()")
        else:
            print("Route planning abandoned as there are no new packages in truck ", truck.ID)

    # This method is called by the planTruckRoute(self, truck: Truck) method.
    # The method will use the package list of the Truck object to determine the best next package to deliver. The result
    # of this process of elimination is added to the Route object of the Truck and is removed of the trucks package list
    #
    # Modes:
    #   1 = First package being delivered. This means the starting location is the HUB and the ideal location has
    #       the shortest distance to the HUB
    #   2 = A package is being delivered before half of all the packages in the truck have been delivered. This means
    #       the ideal next address is both farther away from the hub than the current address and is nearby
    #       the current address.
    #   3 = A package is being delivered after half of all the packages in the truck have been delivered. This means
    #       the ideal next address is both closer to the hub than the current address and is nearby
    #       the current address.
    #   4 = All packages have been delivered. The Hub will be entered as the last entry in the truck route.
    # *****************************************************************************************************************
    # SPACE-TIME COMPLEXITY EVALUATION:
    # n = number of packages in the truck
    # The worst case scenarios assume the truck that is passed in holds all packages from the package file.
    # Mode 1:
    #   This mode loops through all packages in the truck once.
    #   This makes for a complexity of O(n).
    # Mode 2 & 3:
    #   Both of these modes share nearly identical code with minor differences.
    #   These modes loop through all packages in the truck once,
    #   Ths makes for a complexity of O(n)
    # Mode 4:
    #   This mode is a constant time operation.
    #   This makes for a complexity of O(1)
    #
    # Therefore these methods worst case scenario is O(n)
    def findIdealNextAddress(self, mode: int, truck: Truck, currentAddress=""):

        global previousAddress
        global previousID

        if mode == 1:
            firstPackageID = True
            shortestDist = None
            shortestAddress = None
            shortestPackID = None
            for packageID in truck.packageIDs:
                tempAddress = self.pkgHashTable.searchPackage(packageID).address
                tempDist = self.distMatrix.lookupDistance(self.hubAddress, tempAddress)
                if firstPackageID:
                    firstPackageID = False
                    shortestDist = tempDist
                    shortestAddress = tempAddress
                    shortestPackID = packageID
                else:
                    if tempDist < shortestDist:
                        shortestDist = tempDist
                        shortestAddress = tempAddress
                        shortestPackID = packageID
                        # DIAGNOSTIC Print:
                        # print("Package:", shortestPackID, " with address ", shortestAddress,
                        # " Had the shortest distance of: ", shortestDist)
            truck.packageIDs.remove(shortestPackID)
            truck.truckRoute.addPackageToRoute(shortestPackID, shortestDist)
            previousAddress = shortestAddress
            previousID = shortestPackID
        if mode == 2:
            currentScore = 0
            scorePenalty = 0
            if currentDeliveryNumber < numPackagesInRoute * .25:
                scorePenalty = 0
            else:
                maximumPenalty = 20
                modifier = (numPackagesInRoute / 2) - (currentDeliveryNumber - numPackagesInRoute / 4)
                penaltyPercentage = (1 - modifier / (numPackagesInRoute / 2)) * 2
                scorePenalty = penaltyPercentage * maximumPenalty
            bestScore = None
            bestDistFromCurrent = None
            bestDistFromHub = None
            firstPackageID = True
            shortestAddress = None
            shortestPackID = None
            currentDistFromHub = self.distMatrix.lookupDistance(self.hubAddress, currentAddress)
            # DIAGNOSTIC Print:
            # print("Truck ", truck.ID, " Package List:\n\t", truck.packageIDs)
            for packageID in truck.packageIDs:
                tempAddress = self.pkgHashTable.searchPackage(packageID).address
                tempDistFromCurrent = self.distMatrix.lookupDistance(currentAddress, tempAddress)
                tempDistFromHub = self.distMatrix.lookupDistance(self.hubAddress, tempAddress)
                deadlineNotMet = False
                deadlineBeforeEOD = False

                pkgDeadline = self.pkgHashTable.searchPackage(packageID).deliveryDL
                if pkgDeadline is not None:
                    deadLineDelta = timedelta(days=0, hours=pkgDeadline.hour, minutes=pkgDeadline.minute,
                                              seconds=pkgDeadline.second)
                    eTA = truck.truckRoute.calcTimeAtDistPlusStartTime(truck.truckRoute.calcTotalDistanceOfRoute()
                                                                       + tempDistFromCurrent, truck.speed,
                                                                       truck.startingTime)
                    eTADelta = timedelta(days=0, hours=eTA.hour, minutes=eTA.minute, seconds=eTA.second)

                    if deadLineDelta < timedelta(days=0, hours=16, minutes=59, seconds=59):
                        deadlineBeforeEOD = True
                    if eTADelta > deadLineDelta:
                        # DIAGNOSTIC Print:
                        # print("The deadline was not met")
                        deadlineNotMet = True

                if tempDistFromCurrent == 0.0:
                    # Select this Package
                    bestScore = currentScore
                    shortestAddress = tempAddress
                    shortestPackID = packageID
                    bestDistFromCurrent = tempDistFromCurrent
                    bestDistFromHub = tempDistFromHub
                    break
                elif firstPackageID:
                    firstPackageID = False
                    currentScore = tempDistFromCurrent * 10
                    if deadlineBeforeEOD:
                        currentScore -= 100000
                    if tempDistFromHub < currentDistFromHub:
                        currentScore += scorePenalty
                    bestScore = currentScore
                    shortestAddress = tempAddress
                    shortestPackID = packageID
                    bestDistFromCurrent = tempDistFromCurrent
                    bestDistFromHub = tempDistFromHub
                elif deadlineBeforeEOD:
                    if deadlineNotMet:
                        truck.packageIDs.remove(packageID)
                        packagesOnATruck.remove(packageID)
                    else:
                        currentScore = (tempDistFromCurrent * 10) - 100000
                        if tempDistFromHub < currentDistFromHub:
                            currentScore += scorePenalty
                        if currentScore < bestScore:
                            bestScore = currentScore
                            shortestAddress = tempAddress
                            shortestPackID = packageID
                            bestDistFromCurrent = tempDistFromCurrent
                            bestDistFromHub = tempDistFromHub
                else:
                    currentScore = tempDistFromCurrent * 10
                    if tempDistFromHub < currentDistFromHub:
                        currentScore += scorePenalty
                    if currentScore < bestScore:
                        bestScore = currentScore
                        shortestAddress = tempAddress
                        shortestPackID = packageID
                        bestDistFromCurrent = tempDistFromCurrent
                        bestDistFromHub = tempDistFromHub
            # DIAGNOSTIC Print:
            # print("Package:", shortestPackID, " with address ", shortestAddress, " had the best score of: ",
            # bestScore, "\n\tDistance from hub: ", bestDistFromHub,
            # "\n\tDistance from current address: ",
            # currentAddress, " is: ", bestDistFromCurrent)
            truck.packageIDs.remove(shortestPackID)
            truck.truckRoute.addPackageToRoute(shortestPackID, bestDistFromCurrent)
            previousAddress = shortestAddress
            previousID = shortestPackID
        if mode == 3:
            if truck.packageIDs.__len__() == 0:
                distToHub = self.distMatrix.lookupDistance(self.hubAddress, currentAddress)
                truck.distToHubFromFinalPackage = distToHub
                # DIAGNOSTIC Print:
                # print("Final Distance From Current to Hub: ", distToHub)
            else:
                currentScore = 0
                scorePenalty = 0
                if currentDeliveryNumber < numPackagesInRoute * .75:
                    scorePenalty = 0
                else:
                    maximumPenalty = 0
                    modifier = numPackagesInRoute - (currentDeliveryNumber - numPackagesInRoute * .75)
                    penaltyPercentage = (1 - modifier / numPackagesInRoute) * 4
                    scorePenalty = penaltyPercentage * maximumPenalty
                bestScore = None
                bestDistFromCurrent = None
                bestDistFromHub = None
                firstPackageID = True
                shortestAddress = None
                shortestPackID = None
                currentDistFromHub = self.distMatrix.lookupDistance(self.hubAddress, currentAddress)
                # DIAGNOSTIC Print:
                # print("Truck ", truck.ID, " Package List:\n\t", truck.packageIDs)
                for packageID in truck.packageIDs:
                    tempAddress = self.pkgHashTable.searchPackage(packageID).address
                    tempDistFromCurrent = self.distMatrix.lookupDistance(currentAddress, tempAddress)
                    tempDistFromHub = self.distMatrix.lookupDistance(self.hubAddress, tempAddress)

                    deadlineNotMet = False
                    deadlineBeforeEOD = False

                    pkgDeadline = self.pkgHashTable.searchPackage(packageID).deliveryDL
                    if pkgDeadline is not None:
                        deadLineDelta = timedelta(days=0, hours=pkgDeadline.hour, minutes=pkgDeadline.minute,
                                                  seconds=pkgDeadline.second)
                        eTA = truck.truckRoute.calcTimeAtDistPlusStartTime(truck.truckRoute.calcTotalDistanceOfRoute()
                                                                           + tempDistFromCurrent, truck.speed,
                                                                           truck.startingTime)
                        eTADelta = timedelta(days=0, hours=eTA.hour, minutes=eTA.minute, seconds=eTA.second)

                        if deadLineDelta < timedelta(days=0, hours=16, minutes=59, seconds=59):
                            deadlineBeforeEOD = True
                        if eTADelta > deadLineDelta:
                            # DIAGNOSTIC Print:
                            # print("The deadline was not met")
                            deadlineNotMet = True

                    if tempDistFromCurrent == 0.0:
                        # Select this Package
                        bestScore = currentScore
                        shortestAddress = tempAddress
                        shortestPackID = packageID
                        bestDistFromCurrent = tempDistFromCurrent
                        bestDistFromHub = tempDistFromHub
                        break
                    elif firstPackageID:
                        firstPackageID = False
                        currentScore = tempDistFromCurrent * 10
                        if tempDistFromHub > currentDistFromHub:
                            currentScore += scorePenalty
                        bestScore = currentScore
                        shortestAddress = tempAddress
                        shortestPackID = packageID
                        bestDistFromCurrent = tempDistFromCurrent
                        bestDistFromHub = tempDistFromHub
                    elif deadlineBeforeEOD:
                        if deadlineNotMet:
                            truck.packageIDs.remove(packageID)
                            packagesOnATruck.remove(packageID)
                        else:
                            currentScore = (tempDistFromCurrent * 10) - 100000
                            if tempDistFromHub < currentDistFromHub:
                                currentScore += scorePenalty
                            if currentScore < bestScore:
                                bestScore = currentScore
                                shortestAddress = tempAddress
                                shortestPackID = packageID
                                bestDistFromCurrent = tempDistFromCurrent
                                bestDistFromHub = tempDistFromHub
                    else:
                        currentScore = tempDistFromCurrent * 10
                        if tempDistFromHub > currentDistFromHub:
                            currentScore += scorePenalty
                        if currentScore < bestScore:
                            bestScore = currentScore
                            shortestAddress = tempAddress
                            shortestPackID = packageID
                            bestDistFromCurrent = tempDistFromCurrent
                            bestDistFromHub = tempDistFromHub
                # DIAGNOSTIC Print:
                # print("Package:", shortestPackID, " with address ", shortestAddress, " had the best score of: ",
                # bestScore, "\n\tDistance from hub: ", bestDistFromHub,
                # "\n\tDistance from current address: ",
                # currentAddress, " is: ", bestDistFromCurrent)
                truck.packageIDs.remove(shortestPackID)
                truck.truckRoute.addPackageToRoute(shortestPackID, bestDistFromCurrent)
                previousAddress = shortestAddress
                previousID = shortestPackID
        if mode == 4:
            if currentAddress.__len__() < 1:
                truck.truckRoute.addPackageToRoute(-1, self.distMatrix.lookupDistance(self.hubAddress, self.hubAddress))
            else:
                truck.truckRoute.addPackageToRoute(-1, self.distMatrix.lookupDistance(currentAddress, self.hubAddress))

    # This method is called by the findDeliveryRoute(self) method.
    # This method finds all packages with deadlines that are before the End Of Day time and adds them to the global
    # list variable "deadLinePackages".
    def popDeadlinePackages(self):
        for packageID in basePackageList:
            tempDL = self.pkgHashTable.searchPackage(packageID).deliveryDL
            if tempDL is not None:
                deadLineDelta = timedelta(days=0, hours=tempDL.hour, minutes=tempDL.minute)
                endOfDayDelta = timedelta(days=0, hours=17, minutes=0)

                if deadLineDelta < endOfDayDelta:
                    deadLinePackages.append(packageID)

    # This method is called by the findDeliveryRoute(self) method.
    # This method finds all packages that are currently available for pickup and based on the packages related packages,
    # the packages required truck, and packages with the same destination, the truck will be filled space permitting
    # *****************************************************************************************************************
    # SPACE-TIME COMPLEXITY EVALUATION:
    # n = number of packages
    # The worst case scenario for this algorithm is when nearly all packages are available, the truck has the capacity
    # to hold all the packages, and the all the packages are related to exactly one other package. Then, because of how
    # the data would be stored in the relatedIDAr, the relatedID check loops would for n/2 times and then a constant
    # number of times for the inner loop. Effectively executing n times. And the main loop which iterates through all
    # available packages would execute n times as well.
    # Therefore, fillTruck is essentially O(n^2)
    def fillTruck(self, truck: Truck):

        truck.refreshTimeAlongRoute()

        self.findAvailablePackages(truck.timeAlongRoute)

        # Loops through all packages at Hub which can be picked up based on the time variable in the truck object.
        for packID in currentlyAvailPkgIds:

            if isFirstPass and truck.packageIDs.__len__() > .6 * truck.capacity:
                break
            else:
                # ************************************************************************
                # Checks for related packages and adds to the Truck if all packages to be added are available and
                # if the Truck has enough space to fit all the packages
                for listOfRelatedIDs in relatedIDAr:
                    if packID in listOfRelatedIDs:
                        allRelatedPackagesAvail = True
                        for relatedID in listOfRelatedIDs:
                            if relatedID not in currentlyAvailPkgIds:
                                allRelatedPackagesAvail = False
                        if allRelatedPackagesAvail:
                            sizeOfRelatedPacks = listOfRelatedIDs.__len__()
                            if sizeOfRelatedPacks <= truck.spaceInTruck():
                                if packID not in truck.packageIDs:
                                    truck.packageIDs.append(packID)
                                    packagesOnATruck.append(packID)
                                for relatedID in listOfRelatedIDs:
                                    if relatedID not in truck.packageIDs:
                                        truck.packageIDs.append(relatedID)
                                        packagesOnATruck.append(relatedID)

                # Checks for required trucks and adds the package to the truck if there is space
                package = self.pkgHashTable.searchPackage(packID)
                if package.requiredTruck is not None:
                    # Checks if the truck parameter ID matches the packages' req truck
                    if package.requiredTruck == truck.ID:
                        if not truck.addPackage(packID):
                            # The truck has reached capacity
                            break

                # If the current package has the same destination as other packages, all packages with the same
                # destination will attempt to be added to the truck
                for sameDestinationList in sameDestinationIDArr:
                    if packID in sameDestinationList:
                        if type(packID) == str:
                            continue
                        else:
                            if truck.spaceInTruck() >= 1:
                                if packID not in truck.packageIDs and packID in currentlyAvailPkgIds:
                                    truck.packageIDs.append(packID)
                                    packagesOnATruck.append(packID)
                                for sameDestinationPackID in sameDestinationList:
                                    if sameDestinationPackID in currentlyAvailPkgIds:
                                        if truck.spaceInTruck() >= 1:
                                            if sameDestinationPackID not in truck.packageIDs:
                                                truck.packageIDs.append(sameDestinationPackID)
                                                packagesOnATruck.append(sameDestinationPackID)

                # If the package is available, does not require a specific truck, and has no related packages, it may be
                # added to the Truck space permitting
                if packID not in truck.packageIDs:
                    if truck.spaceInTruck() >= 1:
                        truck.addPackage(packID)
                        packagesOnATruck.append(packID)
                    else:
                        # DIAGNOSTIC Print:
                        # print("Package ", packID, " cannot be added to truck ", truck.ID, " as the truck is full.")
                        break

    # This method is called by the findDeliveryRoute(self) method.
    # This method finds all packages that have the same delivery address and adds them to the sameDestinationIDArr
    # global variable.
    def popIDsOfSameDestination(self):
        for rootiD in basePackageList:
            tempList = []
            rootIDAddress = self.pkgHashTable.searchPackage(rootiD).address
            tempList.append(rootIDAddress)
            tempList.append(rootiD)
            destinationListExists = False
            index = 0
            for sameDestinationList in sameDestinationIDArr:
                if rootiD in sameDestinationList:
                    tempList = sameDestinationList
                    destinationListExists = True

            if not destinationListExists:
                for tempiD in basePackageList:
                    tempIDAddress = self.pkgHashTable.searchPackage(tempiD).address
                    if rootIDAddress == tempIDAddress and tempiD not in tempList:
                        tempList.append(tempiD)
                if tempList.__len__() > 2:
                    sameDestinationIDArr.append(tempList)

    # This method is called by the findDeliveryRoute(self) method.
    # This method finds all packages that have related packages and adds them to the 2D relatedIDAr
    # global variable. If the current package has related packages already in relatedIDAr, then it is added to the same
    # list. Otherwise, a new list is created and added to relatedIDAr.
    def populateRelatedID(self):
        for iD in basePackageList:
            tempRelatedIDs.clear()
            self.findAllRelatedIDs(self.pkgHashTable.searchPackage(iD))
            if tempRelatedIDs.__len__() >= 1:
                if tempRelatedIDs[0] == iD and tempRelatedIDs.__len__() == 1:
                    continue
                listExistsWithID = False
                index = 0
                for listOfAllRelatedIDs in relatedIDAr:
                    if iD in listOfAllRelatedIDs:
                        listExistsWithID = True
                    for relatedID in tempRelatedIDs:
                        if relatedID in listOfAllRelatedIDs:
                            listExistsWithID = True
                    if listExistsWithID:
                        if iD not in listOfAllRelatedIDs:
                            relatedIDAr[index].append(iD)
                        for relatedID in tempRelatedIDs:
                            if relatedID not in listOfAllRelatedIDs:
                                relatedIDAr[index].append(relatedID)
                    index += 1
                if not listExistsWithID:
                    relatedIDAr.append([])
                    if iD not in relatedIDAr[relatedIDAr.__len__() - 1]:
                        relatedIDAr[relatedIDAr.__len__() - 1].append(iD)
                    for relatedID in tempRelatedIDs:
                        if relatedID not in relatedIDAr[relatedIDAr.__len__() - 1]:
                            relatedIDAr[relatedIDAr.__len__() - 1].append(relatedID)

    # Recursive method which finds and appends all related packageIDs to the relatedIDList global variable.
    def findAllRelatedIDs(self, basePackage: Package):
        if basePackage.relatedPkgIDs.__len__() >= 1:
            for relatedID in basePackage.relatedPkgIDs:
                relatedPackage = self.pkgHashTable.searchPackage(relatedID)
                if relatedPackage.relatedPkgIDs.__len__() >= 1:
                    self.findAllRelatedIDs(self.pkgHashTable.searchPackage(relatedID))
                else:
                    tempRelatedIDs.append(relatedID)
        else:
            tempRelatedIDs.append(basePackage.pkgID)

    # This method returns the time it would take to travel the distance given at the speed given.
    def calcTimeFromDistanceTraveled(self, distance: int, speed: int):
        hours = distance / speed
        minutes = int((hours % 1) * 60)
        hours = int(hours - (hours % 1))
        return time(hour=hours, minute=minutes)

    # Iterative method which compares the time() parameter to the earliestPickup variable of each package
    # which has not been visited.
    def findAvailablePackages(self, currTime: time):
        currentlyAvailPkgIds.clear()
        for iD in basePackageList:
            package = self.pkgHashTable.searchPackage(iD)
            hour = int(package.earliestPickup.hour)
            minute = int(package.earliestPickup.minute)
            earliestPickupDelta = timedelta(hours=hour, minutes=minute)
            currTimeDelta = timedelta(hours=currTime.hour, minutes=currTime.minute)

            if earliestPickupDelta <= currTimeDelta and iD not in packagesOnATruck:
                currentlyAvailPkgIds.append(iD)

    # This method prints the package status's at any given time.
    def printStatusAtTime(self, desiredReportTime, desiredTruckID=None, desiredPackID=None):
        truckFound = False

        if desiredTruckID is not None:
            print("\n\t\t\t\t< < < < TRUCK ROUTE REPORT > > > >")
            for truck in self.listOfTrucks:
                if truck.ID == desiredTruckID:
                    truck.printRouteStatusAtTime(desiredReportTime, self.pkgHashTable)
                    truckFound = True
            if not truckFound:
                print("A truck with an ID of ", desiredTruckID, " was not found.")
        elif desiredPackID is not None:
            print("\n\t\t\t\t< < < < PACKAGE STATUS > > > >")
            for truck in self.listOfTrucks:
                truck.printPackageStatusAtTime(desiredReportTime, self.pkgHashTable, desiredPackID)
        else:
            print("\n\t\t\t\t< < < < TRUCK ROUTE REPORT > > > >")
            for truck in self.listOfTrucks:
                truck.printRouteStatusAtTime(desiredReportTime, self.pkgHashTable)

    # This method prints the total distance traveled by each truck at the end of their delivery route.
    def printDistancesOfTrucks(self, desiredTruckID=None):
        truckFound = False

        if desiredTruckID is not None:
            print("\n\t\t\t\t< < < < TRUCK ROUTE REPORT > > > >")
            for truck in self.listOfTrucks:
                if truck.ID == desiredTruckID:
                    truckRouteDistance = truck.truckRoute.calcTotalDistanceOfRoute()
                    print("\tTruck ", truck.ID, " drove a combined: ", truckRouteDistance, " miles along it's route.")
                    truckFound = True
            if not truckFound:
                print("A truck with an ID of ", desiredTruckID, " was not found.")
        else:
            print("\n\t\t\t\t< < < < TRUCK ROUTE REPORT > > > >")
            totalDistTraveled = 0
            for truck in self.listOfTrucks:
                truckRouteDist = truck.truckRoute.calcTotalDistanceOfRoute()
                totalDistTraveled += truckRouteDist
            print("\tAll trucks drove a combined: ", totalDistTraveled, " miles along their routes.")
