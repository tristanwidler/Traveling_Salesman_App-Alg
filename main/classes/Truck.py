from main.classes.Route import Route
from datetime import time
from main.classes.HashingTables import HashTable


# This class serves as a shell for all information relating to the delivery trucks.
class Truck:

    # This acts as a constructor for the Truck class sets the local variables.
    def __init__(self, iD=-1, capacity=-1, speed=None, status="N/A"):
        self.ID = iD
        self.capacity = capacity
        self.speed = speed
        self.packageIDs = []
        self.status = status
        self.truckRoute = Route()
        self.startingTime = time(8, 0)
        self.timeAlongRoute = time(8, 0)
        self.distToHubFromFinalPackage = 0

    # This method attempts to add a package to the truck and results the result of the insertion attempt.
    def addPackage(self, packageID):
        if self.packageIDs.__len__() >= self.capacity:
            print("Package ", packageID, " cannot be added to truck ", self.ID, " as the truck is full.")
            return False
        elif packageID in self.packageIDs:
            print("Package ", packageID, " cannot be added to truck ", self.ID, " as it is already loaded.")
        else:
            self.packageIDs.append(packageID)
            return True

    # This method determines and prints the status of the desired package at the given time.
    def printPackageStatusAtTime(self, desiredTime, hashMap: HashTable, packID):
        numSkips = 0

        hours = desiredTime.hour - self.startingTime.hour
        minutes = desiredTime.minute - self.startingTime.minute
        seconds = desiredTime.second - self.startingTime.second
        minutes = minutes + (seconds / 60)
        hours = hours + (minutes / 60)

        if hours < 0:
            truckAtHubAfterTime = True
        else:
            truckAtHubAfterTime = False

        distTraveledAtTime = hours * self.speed

        for packageID in self.truckRoute.routeIDList:
            if str(packID) == str(packageID):
                print("\n\tPackage ", packageID, "'s route status at: ", desiredTime)

                distTraveledByTruckAtID = self.truckRoute.distFromStartToPackage(packageID, numSkips)
                timeDelivered = self.truckRoute.calcTimeAtDistPlusStartTime(distTraveledByTruckAtID, self.speed,
                                                                            self.startingTime)
                if not truckAtHubAfterTime:
                    if distTraveledByTruckAtID < distTraveledAtTime:
                        if packageID == -1:
                            print("\t\tTruck: ", self.ID, ", returned to HUB at: ", timeDelivered)
                            numSkips += 1
                        else:
                            print("\t\tPackage ID: ", packageID, ", Delivered at: ", timeDelivered, "\t\t Deadline: ",
                                  hashMap.searchPackage(packageID).deliveryDL)
                    else:
                        if packageID == -1:
                            print("\t\tTruck: ", self.ID, ", will return to HUB at: ", timeDelivered)
                            truckAtHubAfterTime = True
                        else:
                            print("\t\tPackage ID: ", packageID, ", is en Route", "\t\t Deadline: ",
                                  hashMap.searchPackage(packageID).deliveryDL)
                else:
                    if packageID == -1:
                        pass
                    else:
                        print("\t\tPackage ID: ", packageID, ", is at HUB")

    # This method determines and prints the status of all packages in the trucks Route at the given time.
    def printRouteStatusAtTime(self, desiredTime, hashMap: HashTable):
        # self.truckRoute.setStatusAtTime(desiredTime)
        numSkips = 0

        hours = desiredTime.hour - self.startingTime.hour
        minutes = desiredTime.minute - self.startingTime.minute
        seconds = desiredTime.second - self.startingTime.second
        minutes = minutes + (seconds / 60)
        hours = hours + (minutes / 60)

        if hours < 0:
            truckAtHubAfterTime = True
        else:
            truckAtHubAfterTime = False

        distTraveledAtTime = hours * self.speed
        print("\nTruck ", self.ID, "'s route status at: ", desiredTime)
        for packageID in self.truckRoute.routeIDList:
            distTraveledByTruckAtID = self.truckRoute.distFromStartToPackage(packageID, numSkips)
            timeDelivered = self.truckRoute.calcTimeAtDistPlusStartTime(distTraveledByTruckAtID, self.speed, self.startingTime)
            if not truckAtHubAfterTime:
                if distTraveledByTruckAtID < distTraveledAtTime:
                    if packageID == -1:
                        print("\tTruck: ", self.ID, ", returned to HUB at: ", timeDelivered)
                        numSkips += 1
                    else:
                        print("\tPackage ID: ", packageID, ", Delivered at: ", timeDelivered, "\t\t Deadline: ", hashMap.searchPackage(packageID).deliveryDL)
                else:
                    if packageID == -1:
                        print("\tTruck: ", self.ID, ", will return to HUB at: ", timeDelivered)
                        truckAtHubAfterTime = True
                    else:
                        print("\tPackage ID: ", packageID, ", is en Route", "\t\t Deadline: ", hashMap.searchPackage(packageID).deliveryDL)
            else:
                if packageID == -1:
                    pass
                else:
                    print("\tPackage ID: ", packageID, ", is at HUB")

    # This method determines and prints the total distance of the trucks Route.
    def printRouteDistancesAtTime(self, desiredTime, hashMap: HashTable):
        self.truckRoute.calcTotalDistanceOfRoute()

    # This method calculates and sets the timeAlongRoute at the last package in the Route.
    def refreshTimeAlongRoute(self):
        timeOfFullRoute = self.truckRoute.timeAtEndOfRoute(self.speed)

        newSec = (self.startingTime.second + timeOfFullRoute.second) % 60

        newMin = (self.startingTime.minute + timeOfFullRoute.minute) % 60
        newMin = newMin + ((self.startingTime.second + timeOfFullRoute.second) // 60)

        newHour = self.startingTime.hour + timeOfFullRoute.hour
        newHour = newHour + ((self.startingTime.minute + timeOfFullRoute.minute) // 60)

        self.timeAlongRoute = time(hour=newHour, minute=newMin, second=newSec)

    # This method return how much room the truck has left in its package list.
    def spaceInTruck(self):
        return self.capacity - self.packageIDs.__len__()

    # This method serves as a setter for the truckRoute variable
    def setTruckRoute(self, truckRoute):
        self.truckRoute = truckRoute

    # This method serves as a getter for the truckRoute variable
    def getTrucksRoute(self):
        return self.truckRoute

    # This method prints all packages currently in the truck.
    # The method is used for diagnostic purposes.
    def printPackageList(self):
        print("Truck", self.ID, "contains:")
        for packID in self.packageIDs:
            print("\tPackage ID: ", packID)
