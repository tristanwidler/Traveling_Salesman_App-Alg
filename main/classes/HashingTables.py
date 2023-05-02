from main.classes.Package import Package
import math


# This class acts as a repository for the program and provides near constant time lookups of the Package objects.
class HashTable:

    # This acts as a constructor for the DeliveryAlgorithm object and plans the route for all packages and trucks given
    def __init__(self, tableSize=10):
        self.tableSize = tableSize
        self.table = []
        for i in range(tableSize):
            self.table.append([])

    # This method acts as a hash function and is used to evenly spead out the locations of the packages stored
    def genKey(self, packageID):
        iDCharacterList = list(str(packageID))
        # Serves as a base multiplicand
        keyMultiplicand = math.sqrt(math.pi) * math.tau - .33
        # loops through and selects characters from the given ID to create a unique multiplicand
        for character in iDCharacterList:
            asciiVal = (ord(character))
            # print("\tASCII val :", asciiVal)
            keyMultiplicand = keyMultiplicand * math.sqrt(asciiVal)

        # Relatively Unique multiplicand * a Fermat prime number
        # DIAGNOSTIC Prints:
        # print("\tMultiplicand: ", keyMultiplicand)
        # print("\tPi * multiplicand: ", math.pi * keyMultiplicand)
        return int(math.pi * keyMultiplicand)

    # This method inserts a package object into the hash table.
    # *****************************************************************************************************************
    # SPACE-TIME COMPLEXITY EVALUATION:
    # As the insertion point is decided mathematically using genKey(), the complexity is constant O(1)
    def insertPackage(self, package):
        # print(package.pkgID, " Insert:")
        key = self.genKey(package.pkgID)
        # print("\tKey: ", key)
        tableSize = self.table.__len__()
        index = key % tableSize
        # print("\tIndex: ", index)
        self.table[index].append(package)

    def insertPackages(self, packageList):
        for package in packageList:
            self.insertPackage(package)

    # This method searches for and , if found, returns a package object from the hash table.
    # *****************************************************************************************************************
    # SPACE-TIME COMPLEXITY EVALUATION:
    # n = number of packages in HashTable
    # Assuming an effective hash function (genKey()) the packages should be relatively evenly spead through the
    # hash table.
    # Thus resulting in a complexity of O(1) or near O(1) a vast majority of the time.
    # However, should the right conditions manifest, all packages could potentially end up in the same index of the hash
    # table. This very unlikely condition would result in a complexity of O(n)
    def searchPackage(self, packageID):
        packageID = int(packageID)
        tableIndex = self.genKey(packageID) % self.table.__len__()
        listFromIndex = self.table[tableIndex]

        if listFromIndex.__len__() > 0:
            for package in listFromIndex:
                if package.pkgID == packageID:
                    return package
            return False
        else:
            return False

    # Prints all buckets in the table and their contents and the current efficiency of the hash function genKey().
    # Used for diagnostic purposes
    def printTableContents(self):
        numListCollisions = 0
        numCleanLists = 0
        print("Table Size: ", self.tableSize)
        for listOfPackages in self.table:
            if listOfPackages.__len__() == 1:
                print("[", listOfPackages[0].pkgID, "]")
                numCleanLists += 1
            if listOfPackages.__len__() > 1:
                packageIDs = []
                for package in listOfPackages:
                    packageIDs.append(package.pkgID)
                print(packageIDs)
                numListCollisions += 1
            if listOfPackages.__len__() == 0:
                print(listOfPackages)

        print("Hash Function Efficiency: ", 1 - (numListCollisions / (numCleanLists + numListCollisions)))

    # This method searches for and , if found, removes a package object from the hash table.
    # *****************************************************************************************************************
    # SPACE-TIME COMPLEXITY EVALUATION:
    # n = number of packages in HashTable
    # This method relies on the searchPackage() method to find the package to be deleted in the hash table. As the
    # actual removal of the package is a constance time operation, the methods shares searchPackage() complexity.
    # Therefore, in a vast majority of cases, complexity is O(1) but can technically be O(n)
    def removePackage(self, packageID):
        index = self.genKey(packageID) % self.table.__len__()
        try:
            if self.searchPackage(packageID):
                self.table[index].remove(self.searchPackage(packageID))
                print("Package ID: ", packageID, " was removed from the hash table.")
                return True
            else:
                print("Package ID: ", packageID, " was not found in the hash table.")
                return False
        except:
            print("An error has occurred while attempting to delete Package ID: ", packageID)
            return False
