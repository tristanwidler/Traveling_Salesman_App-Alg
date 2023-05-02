# Traveling Salesman CLI App and Algorithm
Purpose: This program was created to solve a spin on the Traveling Salesman Problem where the prmopt is is more along side a package delivery algorithm.
It provides a CLI for user interaction and uses a mixture of the greedy and simulated annealing algorithms. 
The path planning also has a scoring system with customizable weights which could be used to improve the generated path.

The project was created as part of a course when I attended Western Governors University. 
The premise is that the program must find a path between the given locations which allows all packages to be delivered before the end of business hours.

#### Constraints

- Packages
  - Packages may have deadlines
  - Packages may need to be delivered along side other related packages
  - Packages may have an earliest pickup time
- Trucks
  - Delivery Trucks are limited in quantity
  - Delivery Trucks have limited storage space
  
#### Algorithms Used

- Simulated Annealing
- Greedy

## Application Information

### Contact

- Author: Tristan Widler
- Contact Information:
  - Email: tristan.widler@gmail.com

### Versions

- Application Version: 1.0
  - Creation Date: 04/07/2022
- IDE & Version: PyCharm 2021.3.1
- Language: Python 3.10

### Project Contributions/Credits

- Source Code
  - Tristan Widler
- files\WGUPS_Distance_Table.csv
  - Western Governors University
- files\WGUPS_Package_File.csv
  - Western Governors University
  
### Algorithms

#### Overview

The algorithm used in this program uses aspects of both the greedy algorithm and the simulated annealing algorithm. 
The project's algorithm starts by picking the next closest address which has a package that needs to be delivered using a scoring system. 
Once approximately one-quarter of the packages on the delivery truck has been delivered, a score penalty is applied and gradually increased to drive the truck away from the hub. 
After the truck delivers half of the packages it contains, the same system is applied in reverse. 
Meaning the truck delivers to the closest address until three-quarters of the packages have been made. 
The remaining packages receive score penalties to try and persuade the truck back towards the hub.

#### Time Complexity
All locations referenced below have comments above their definitions with further explanation.

Major run-time complexity evaluation locations:
- HashingTables.py:
  - insertPackage: O (1)
  - searchPackage: O (n)
  - removePackage: O (n)
- DistanceMatrix.py:
  - lookupDistance: O(n)
- CSVParser.py:
  - parseAndStoreCSVDistanceFile: O (n)
  - parseAndStoreCSVPackageFile: O (n)
- DeliveryRouteAlgorithm.py:
  - findIdealNextAddress: O (n)
  - fillTruck: O (𝑛2)
  - planTruckRoute O (𝑛2)
  - findDeliveryRoute O (𝑘∗𝑛4)

- HashingTables.py: O(1)
- DistanceMatrix.py: O(1)
- CSVParser.py: O(n)
- DeliveryRouteAlgorithm.py: O(𝑘∗𝑛^4)

Therefore, the programs time complexity is 𝑘∗𝑛^4+𝑛+1+1), or O(𝒌∗𝒏^𝟒) where k is the number of trucks and n is the number of packages.

If my analysis is flawed please feel free to contact me at the email given above.

#### Space Complexity
- HashingTables.py:
  - As n (number of packages) increases, the space required by the Hash Table is O(n)
- DistanceMatrix.py:
  - As n (number of packages) increases, the space required by the Distance Matrix increases by O(𝑛^2) as the matrix is a 2D array.

Therefore the programs space complexity is 𝑛^2+𝑛, or O(𝒏^𝟐).

## The CLI

This applications CLI is relatively simple to use. The application calculates the theoretical package and truck status at any given time. 

For example:
- At 09:00
  - Package ID 1 is out for delivery on Truck ID 3
- At 12:23
  - Package ID 1 was delivered at 09:35
  
The interface has descriptive prompts and should check for invalid input. 
