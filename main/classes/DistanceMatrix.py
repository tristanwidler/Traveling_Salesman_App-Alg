# This class provides near constant lookup times of distance values between any two addresses stored in the matrix to
# be used by other classes.
class DistanceMatrix:

    # This acts as a constructor for the DistanceMatrix object and populates the two-dimensional array structure.
    def __init__(self, matrixSize=0, addressAndDistanceList=[], distanceMatrix=[[], []], ):
        self.matrixSize = matrixSize
        self.addressDictionary = {"": -1}
        self.addressDistanceList = addressAndDistanceList

        if matrixSize > 0:
            self.distanceMatrix = self.buildMatrixOfSize(matrixSize)
            self.populateDistMatrix(addressAndDistanceList)
        else:
            self.distanceMatrix = distanceMatrix

    # This method is used to build the two-dimensional array distanceMatrix to the size required.
    def buildMatrixOfSize(self, matrixSize):
        tempVal = 0
        matrix = []
        while tempVal < matrixSize:
            matrix.append([])
            tempVal += 1
        return matrix

    # This method is used to populate the two-dimensional array distanceMatrix and the addressDictionary
    def populateDistMatrix(self, addressAndDistList):
        rowCounter = 0
        colCounter = 0
        isFirstSplit = True
        distanceValList = []

        for addressDistanceLine in addressAndDistList:
            splitValues = str(addressDistanceLine).split(",")
            for split in splitValues:
                if isFirstSplit:
                    # The first split of the first line is formatted differently than the rest of the values.
                    # Thus the first split must be entered and parsed differently
                    isFirstSplit = False

                    secondarySplit = split.split("(")
                    tempList = list(secondarySplit[0])
                    tempList.pop(0)
                    tempList.pop(0)
                    while tempList[0] == " ":
                        tempList.pop(0)
                    finalAddress = "".join(tempList)
                    finalAddress.strip()
                    finalAddress = finalAddress.replace("South", "S")
                    finalAddress = finalAddress.replace("West", "W")
                    finalAddress = finalAddress.replace("East", "E")
                    finalAddress = finalAddress.replace("North", "N")
                    self.addressDictionary[finalAddress] = len(self.addressDictionary) - 1
                else:
                    if split != "" and split != ' \'\'':
                        # Remove unnecessary values from the distance and convert to a float value.
                        split = split.strip()
                        split = split.replace(" \'", "")
                        split = split.replace("'", "")
                        try:
                            distanceValList.append(float(split))
                        except:
                            # DIAGNOSTIC Print:
                            # print("Unable to convert ", split, " to a 'float' datatype for the distance matrix.")
                            pass
                    else:
                        break

            for distVal in distanceValList:
                self.distanceMatrix[rowCounter].append(distVal)
                colCounter += 1
            rowCounter += 1
            colCounter = 0
            isFirstSplit = True
            distanceValList.clear()

        # DIAGNOSTIC Prints:
        # temp = 1
        # for address in self.distanceMatrix:
            # print("Address ", temp, ":", address)
            # temp += 1

    # This method is used to navigate the two-dimensional array stored by this class.
    # When searching through the matrix for a specific "coordinate", if the first coordinate is longer than the amount
    # of values in the first nested list, the coordinates will flip. Meaning the row index becomes the column index
    # and the column index becomes the row. This allows the matrix to be structured identical to the reference file.
    # *****************************************************************************************************************
    # SPACE-TIME COMPLEXITY EVALUATION:
    # n = number of addresses(columns or rows)
    # This method uses a dictionary object to navigate the two-dimensional distance array. As a dictionary is similar
    # in logic to a hash table, the method shares its complexity.
    # meaning, in a vast majority cases the complexity is O(1).
    # However, though extremely unlikely, the worst case complexity could be O(n)
    def lookupDistance(self, addressOne, addressTwo):
        distance = None
        firstIndex = None
        secondIndex = None

        try:
            firstIndex = self.addressDictionary.get(addressOne)
            try:
                secondIndex = self.addressDictionary.get(addressTwo)
                try:
                    if firstIndex < secondIndex:
                        temp = firstIndex
                        firstIndex = secondIndex
                        secondIndex = temp
                    distance = self.distanceMatrix[firstIndex][secondIndex]
                    return distance
                except:
                    print("Error while reading from the distance matrix.")
            except:
                print("Could not find address two in the distance dictionary.")
        except:
            print("Could not find address one in the distance dictionary.")
