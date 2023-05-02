from datetime import time
from main.classes.Package import Package


class Route:

    def __init__(self, departureTime=time()):
        self.routeIDList = []
        self.routeDistList = []
        self.departureTime = departureTime
        self.returnTime = time()
        self.finalPackageToHubDist = None

    def addPackageToRoute(self, packID, distance):
        self.routeIDList.append(packID)
        self.routeDistList.append(distance)

    def calcTotalDistanceOfRoute(self):
        dist = 0
        for distance in self.routeDistList:
            dist += distance
        return dist

    def printPathAndDist(self, packHashMap):
        index = 0
        for iD in self.routeIDList:
            if iD != -1:
                print("\tID:\t", iD, ", ", self.routeDistList[index], "\tAddress\t",
                      packHashMap.searchPackage(iD).address)
                index += 1
            else:
                print("\tHUB ID:\t", iD, ", ", self.routeDistList[index], "\tAddress\t4001 S 700 E Salt Lake City UT")
                index += 1

    def timeAtEndOfRoute(self, speed):
        distance = self.calcTotalDistanceOfRoute()
        hours = distance / speed
        minutes = (hours % 1) * 60
        seconds = (minutes % 1) * 60
        hours = int(hours - (hours % 1))
        minutes = int(minutes - (minutes % 1))
        seconds = int(seconds - (seconds % 1))
        return time(hour=hours, minute=minutes, second=seconds)

    def calcTimeAtDistance(self, distance, speed):
        hours = distance / speed
        minutes = (hours % 1) * 60
        seconds = (minutes % 1) * 60
        hours = int(hours - (hours % 1))
        minutes = int(minutes - (minutes % 1))
        seconds = int(seconds - (seconds % 1))
        return time(hour=hours, minute=minutes, second=seconds)

    def calcTimeAtDistPlusStartTime(self, distance, speed, startingTime: time):
        hours = distance / speed
        minutes = (hours % 1) * 60
        seconds = (minutes % 1) * 60

        seconds = ((int(seconds - (seconds % 1)) + startingTime.second) % 60)

        minutes = ((int(minutes - (minutes % 1)) + startingTime.minute) % 60)
        minutes = minutes + ((int(seconds - (seconds % 1)) + startingTime.second) // 60)

        hours = int(hours - (hours % 1)) + startingTime.hour
        hours = hours + ((int(minutes - (minutes % 1)) + startingTime.minute) // 60)

        return time(hour=hours, minute=minutes, second=seconds)


    def setDepartureTime(self, departureTime: time):
        self.departureTime = departureTime

    def calcDistAtTime(self, desiredTime: time, speed):
        hours = desiredTime.hour
        minutes = desiredTime.minute
        seconds = desiredTime.second
        minutes = minutes + (seconds / 60)
        hours = hours + (minutes / 60)

        return hours * speed

    # FIX
    # returns only the first -1 ID time
    def distFromStartToPackage(self, packageID, numSkips):
        totalDist = 0
        index = 0
        for iD in self.routeIDList:
            totalDist += self.routeDistList[index]
            if iD == packageID:
                if iD == -1:
                    if numSkips >= 1:
                        numSkips -= 1
                        continue
                    else:
                        break
                else:
                    break
            index += 1
        return totalDist


