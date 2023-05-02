from datetime import datetime, time


# This class serves as a shell for all information relating to the packages.
class Package:

    # This acts as a constructor for the Truck class sets the local variables.
    def __init__(self,
                 pkgID=-1, address=None, city=None,
                 state=None, zipcode=None, deliveryDL=None,
                 mass=None, requiredTruck=None, relatedPkgIDs=[], earliestPickup: time = time(8, 0)):
        self.pkgID = int(pkgID)
        self.address = address
        self.city = city
        self.state = state
        self.zip = zipcode
        self.deliveryDL = deliveryDL
        self.mass = mass
        self.requiredTruck = requiredTruck
        self.relatedPkgIDs = relatedPkgIDs
        self.earliestPickup = earliestPickup
        self.stateDictionary = {0: "At HUB", 1: "On Truck", 2: "Delivered"}

    def getPackageID(self):
        return self.pkgID

    def setPackageState(self, state):
        self.state = state
