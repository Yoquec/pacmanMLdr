---
title: "Pac-man first delivery report"
author: "Alvaro Viejo & Alejandro Mayo"
date: "2/7/2022"
---

Alvaro Viejo & Alejandro Mayo
# Pac-man first delivery report
This is the report for the first assignment on the **Machine Learning I** course. 

This report will contain all the notes on the resolution and answers to the proposed exercises.


### Exercise 1: What information is shown in the interface? And in the terminal? Which position does Pac-Man occupy initially?
In the game's user interface we can see Pac-cman along with 4 different ghosts. Down to the right we have 4 number indicating the Manhattan distances between Pac-man and each of the ghosts. Down to the left we can see 4 squares in which dead ghosts are placed after being eaten by Pac-man, and right down bellow we can see a counter with the current score.

If we do not specify any flags, `python busters.py` defaults to using the keyboard agent, letting the user take control of the movements. It will also default to use a simple test-bench map with a single wall.

In the terminal we can see info about the game's runtime, like the map's width and height, pacman's position, the permitted directions in which to move in, pacman's current direction, the number ghosts alive, etc.
We can also see a small sketch of the current map.

If we run the game, Pacman's initial position as indicated in the info belonging to the first tick is 12,10.

![[firstTick.png]]

The overall image the user gets when running the program is:

![[terminalAndGui.png|600]]


### Exercise 2: In your opinion, which data could be useful to decide what Pac-Man should do on each tick?
The most useful decision-taking information would be the **current tick**, **Pac-man's position** and the **ghosts' positions**.

Another factor of interest would be to get a mere knowledge of the **map**, to get a hold of the walls Pac-man would need to sort through to get to the ghosts. Along with the map, knowing **screen dimensions** could be useful to get a hold of the size of the map without any additional computing.

In view of developing an algorithm to control the Pac-man, the **legal movements/actions** and **distances to each ghost** in each specific tick would also be useful data when deciding which are our best bets in terms of movement.

Finally we can add in a variable to check which **ghosts are still alive**, just to avoid unnecessary computations; and some variable making reference to **pac-dots**

It is important to point out that the living ghosts variable  is a boolean list where the first object is always `false` as it references our character.


### Exercise 3: Take a look to the layout folder. How are the mazes defined? Create a new maze, save it and execute the game on it. Include a screenshot of the maze in the document.
There are 18 files with different mazes. They are text files with the `.lay` extension.
The mazes are built by 6 characters: `'%', ' ', '.', 'o', 'P', 'G'`.
* `%` indicate the **walls** of the map.
* ` ` (spaces) indicate parts of the map which are "**walkable**".
* `.` (dots) indicate **pac-dots**.
* `o` indicate the **power ups** that allow Pac-man to eat the ghosts.
* `P` indicates the **posistion** of the **Pac-man**
* `G` indicate the **position** of the **ghosts**

![[mazeExample.png]]

We built a maze called `ourLayout` and put it inside our layouts folder. It consist on a map saying "hello" and "bye" with a square in the middle containing the ghosts and a narrow space to fit in between.

![[ourLayoutImage.png]]


### Exercise 4: Execute the agent `BasicAgentAA` with the following command: `python busters.py -p BasicAgentAA`. Describe which information is shown in the screen about the game state. Which information do you consider the most useful?
When we execute  `python busters.py -p BasicAgentAA` command we can see data printed out by the `printInfo()` function in the terminal.
We get information as Pac-man's direction, the number of ghosts, the remaining living ghost and their positions, directions and distances. 
It also prints out the distance to the nearest pac-dot and how many pac dots there are.
Additionally, we get a diagram of the map and the current score.
On the interface we just see the game as in *Exercise 1*.

The most useful information in our opinion is, as mentioned in *Exercise 2*, **ghost's position, state and distances from Pac-man**, in order to choose a ghost to target. The score or dots doesn't seems so important in order to win the game, but could be useful when training **reinforcement learning models**.

![[tickInfo.png]]

### Exercise 5: Program a method called `printLineData()` inside the `BasicAgentAA` agent from the `bustersAgents.py` file. This method should return a string with the information from the Pac-Man state ...
There are 4 important parts to this exercise.

***The first one*** is to **check if the file exists**. If it doesn't, create it and add the csv headers.
If it does exist, we still have to check if the file isn't empty; if it is we also have to write headers.

We were able to achieve this using python's builtin `os` library

```py
CSV_FILE_NAME = "textdump.csv"

if CSV_FILE_NAME in os.listdir():
	with open(CSV_FILE_NAME, "r") as file_check:
		if len(file_check.readlines()) == 0:
			to_write = True
		else:
			to_write = False
# If file doesn't exist, then create it
else:
	os.mknod(CSV_FILE_NAME)
	to_write = True
```


The ***second part*** is creating the necessary headers for the csv.
Following the answers in *exercises 2 and 4*, we created a list of headers in a file called `headers.py`

```py
"""
Authors: Alvaro Viejo and Alejandro Mayo

File to get the header files
"""
header_vals =[
        "ticks",
        "screen_dim_x",
        "screen_dim_y",
        "pacman_pos_x",
        "pacman_pos_y",
        "legal_North",
        "legal_South",
        "legal_East",
        "legal_West",
        "legal_Stop",
        "pacman_dir",
        "ghost_num",
        "ghost1_alive",
        "ghost2_alive",
        "ghost3_alive",
        "ghost4_alive",
        "ghost1_x",
        "ghost1_y",
        "ghost2_x",
        "ghost2_y",
        "ghost3_x",
        "ghost3_y",
        "ghost4_x",
        "ghost4_y",
        "ghost1_dir",
        "ghost2_dir",
        "ghost3_dir",
        "ghost4_dir",
        "ghost1_dist",
        "ghost2_dist",
        "ghost3_dist",
        "ghost4_dist",
        "pacdots_remaining",
        "nearestpacdot_dist",
        "score"
        ]

HEADERS = ','.join(header_vals) + "\n"

```

As we can see, this file contains all the headers in a list, which are then joined by commas and added a newline.

The ***third part*** consists on opening a file handler in append mode before the main loop of the game.

```py
# Open the file
file_hand = open(CSV_FILE_NAME, "a")

# Write header
if to_write:
	file_hand.write(HEADERS)
```

This same file handler is closed after the game loop finishes.
(line 783)
```py
#NOTE: close the file with game state
file_hand.close()
```

the ***fourth and final step*** is to call our function when a new observation is created. This function should be called only by the BasicAgentAA, so we need to check that it is only being called by this agent. This check is performed by `if agentIndex == self.startingIndex:.`

```py
if agentIndex == self.startingIndex:
	to_write = agent.printLineData(observation)
	file_hand.write(to_write)
```
In our function we have done the same as for the headers but inserting the game state characteristics at each tick, as we can see below we have included most of the important information.
```py
        # Assamble all the variables
        gameInfo = [                                #HEADER_NAME
                str(self.countActions),             #ticks
                str(gameState.data.layout.width),   #screen_dim_x
                str(gameState.data.layout.height),  #screen_dim_y
                str(pacman_pos[0]),                 #pacman_pos_x
                str(pacman_pos[1]),                 #pacman_pos_y
                str(legal[0]),                      #legal_North
                str(legal[1]),                      #legal_South
                str(legal[2]),                      #legal_East
                str(legal[3]),                      #legal_West
                str(legal[4]),                      #legal_Stop
                str(gameState.data.agentStates[0].getDirection()), #pacman_dir
                str(gameState.getNumAgents() - 1),  #ghost_num
                str(ghost_living[0]),               #ghost1_alive
                str(ghost_living[1]),               #ghost2_alive
                str(ghost_living[2]),               #ghost3_alive
                str(ghost_living[3]),               #ghost4_alive
                str(ghost_positions[0][0]),         #ghost1_x
                str(ghost_positions[0][1]),         #ghost1_y
                str(ghost_positions[1][0]),         #ghost2_x
                str(ghost_positions[1][1]),         #ghost2_y
                str(ghost_positions[2][0]),         #ghost3_x
                str(ghost_positions[2][1]),         #ghost3_y
                str(ghost_positions[3][0]),         #ghost4_x
                str(ghost_positions[3][1]),         #ghost4_y
                str(ghost_dirs[0]),                 #ghost1_dir
                str(ghost_dirs[1]),                 #ghost2_dir
                str(ghost_dirs[2]),                 #ghost3_dir
                str(ghost_dirs[3]),                 #ghost4_dir
                str(ghost_dist[0]),                 #ghost1_dist
                str(ghost_dist[1]),                 #ghost2_dist
                str(ghost_dist[2]),                 #ghost3_dist
                str(ghost_dist[3]),                 #ghost4_dist
                str(gameState.getNumFood()),
                str(gameState.getDistanceNearestFood()),
                str(gameState.getScore())
                ]
        
        # Prepare the string with all the data
        returnstr = ",".join(gameInfo) + "\n"
        return returnstr# }}}

```
With this we create a file where the first line will always be the header and then we will insert the game status at each tick which can help to recognise patterns or see just how a game has evolved, important to point out that we include each one in a new line and we never errase the data.

### Exercise 6: Program an “intelligent” Pac-Man. To do so, modify the method `chooseAction()` from the BasicAgentAA class...
We have created the new method using an algorithm called Astar.
We have implemented it in a method which returns the path of the shortest way to any specific cell in the map, assuming that it is not a wall. This method can be called to get the path to any specific ghost.
We also use this method to get an accurate meassurement of the distance of each ghost taking walls into account. After calling the method all the ghosts, we look for the one that is closest and move torwards its direction. If for some reason another ghost gets closer during the process, the next tick we will change the target to be this new closest ghost.

To get more information on how we implemented the Astar algorithm, refer to the notes down bellow.

To calculate the ticks that it takes we have done it without specifying any map so using the default map.
With the static it takes 25 ticks which always is the same amount as there is only one optimized pattern.

With the random method it takes around 35 to 45 ticks which isn't very much, obviusly this mean will always be higher than in the static method as the ghost random moves will generate some contrary moves for the pacman agent.

### Exercise 7: The agent you just programmed does not use any machine learning technique. What advantages do you think machine learning may have to control Pac-Man?
We think that machine learning could behave in a way where it can predict according to the walls near the ghost the directions that it will take and we can use that to intercept them in their ways instead of going directly to their actual positions.
Also in some decision instead of the least distance to a ghost it could also take into account where it is more probable that some ghost will be in an specific time, so not focusing in the individuals but on the whole picture and calculating where the ghosts could be and with what probability.


---

# Notes
## Astar algorithm Explanation 
The Astar algorithm is a path-finding algorithm based on the Dijkstra's algorithm. The principal difference is that A* adds in a Heuristic of how close the selected node is from the target. In other words, the algorithm is biased into first exploring the nodes which are closest to the target node.
This heuristic is the Manhattan distance to the target.

To implement this algorithm we first transformed the map characters into a grid of nodes. That is, convert the map into a graph so we can run search algorithms.  

```py
        import AstarTest
        Agrid = AstarTest.AstarGrid(self.state.deepCopy())

```

As the import suggests, this classes, both the grid and the nodes are found in the `AstarTest` file. This file contains the classes and the methods necessary to run the algorithm.
A* runs on the grid of nodes (AstarGrid), and the nodes (AstarNodes) contain some relevant information (such as their parent during the search).

```py
class AstarNode:
    "Class representing nodes for the A* pathfinding algorithm"
    def __init__(self, position: Tuple[int, int] , isWall: bool) -> None:
        self.pos: Tuple[int, int] = position
        self.isWall = isWall

        # Set initial values for gCost and hCost
        self.nodeGcost: int = -1
        self.nodeHcost: int = -1

        # Set node parent to None
        self.nodeParent: AstarNode
```


The AstarGrid class transforms our map into a matrix where each elemtn on the matrix will be a node object that specifies their positions and more such a boolean to show if they are walls.
```py
class AstarGrid:
    "Class representing the node grid for the A* pathfinding algorithm"
    # NOTE: the maps counts (0, 0 as the bottom left)

    def __init__(self, gameState) -> None:
        self.map = gameState.getWalls()

        # Get the world size
        self.mapSize: Tuple[int, int] = (
                gameState.data.layout.width, 
                gameState.data.layout.height
                )

        # Set up everything for the grid of nodes
        self.nodeGrid: List[List[AstarNode]] = []

        # Inverts the keys and values of the Actions dictionary
            # To be used when translating positions of nodes to directions
        self.posToDirection = dict([(y, x) for x, y in list(Actions._directions.items())])
        
        # add the nodes
        self.addNodes()
```


For the function findPath we need to set the initial and target positions which may always be the position of a ghost.


```py
def findPath(self, startPos: Tuple[int, int], targetPos: Tuple[int, int]):
        """
        Implementation of the A* algorithm to find a path for two points in the pacman map

        Returns a list of Direction strings
        """
        startNode: AstarNode = self.getNodeFromPos(startPos)
        targetNode: AstarNode = self.getNodeFromPos(targetPos)

        # Create open and closed sets for the algorithm (list of nodes)
        openNodes: List[AstarNode] = []
        closedNodes: List[AstarNode] = []

        # Add the start Node to the open set
        openNodes.append(startNode)

        # Start the algorithm loop
        while (len(openNodes) > 0):
            # Start pointing at the starting node
            currentNode = openNodes[0]

            for i in range(1, len(openNodes)):
                # if the fcost of the next node is smaller than the one
                # for the current node, update it.
                # If fcosts are equal, compare hCost
                compareNode = openNodes[i]

                if (compareNode.fCost < currentNode.fCost) or \
                        (compareNode.fCost == currentNode.fCost \
                        and compareNode.hCost < currentNode.hCost):
                    currentNode = openNodes[i]

            # Remove the current node from open and add to closed
            openNodes.remove(currentNode)
            closedNodes.append(currentNode)

            # Check if we already arrived to the targetNode
            if currentNode == targetNode:
                return self.buildPathDirections(startNode, targetNode)

            # Get neighbors
            for neighbor in self.getNodeLegalNeighbors(currentNode):
                # Skip the neighbor if it is a wall or aleady visited
                if (neighbor.isWall) or (neighbor in closedNodes):
                    continue

                # Check if the new path is shorter (or node was unvisited)
                movementToNeighborCost: int = currentNode.gCost + 1

                if (movementToNeighborCost < neighbor.gCost) or (neighbor not in openNodes):
                    # Update gCost and hCost
                    neighbor.gCost = movementToNeighborCost
                    neighbor.hCost = util.manhattanDistance(neighbor.pos, targetPos)

                    # Set the current node as the parent of the precedent node
                    neighbor.parent = currentNode

                    # check if the neighbor is in the list of open nodes, and if not, add it
                    if neighbor not in openNodes:
                        openNodes.append(neighbor)
```