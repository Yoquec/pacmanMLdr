"""
Authors: Alvaro Viejo and Alejandro Mayo

This file will include all the necessary elements for the A* search algorithm that
the pacman will use to hunt down all the ghosts
"""
from typing import List, Tuple

# import game
# Actions = game.Actions
# Directions = game.Directions
from game import Actions
from game import Directions


import util

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

    @property
    def gCost(self) -> int:
        "Distance from the starting node"
        return self.nodeGcost

    @gCost.setter
    def gCost(self, value) -> None:
        self.nodeGcost = value

    @property
    def hCost(self) -> int:
        "Distance from the end node"
        return self.nodeHcost

    @hCost.setter
    def hCost(self, value) -> None:
        self.nodeHcost = value

    @property
    def fCost(self) -> int:
        "Function to compute the fcost of a Node"
        if (self.hCost == -1) or (self.gCost == -1):
            return -1
        else:
            return self.gCost + self.hCost

    @property
    def parent(self):
        "Property to indicate the node's parent in the algorithm execution"
        return self.nodeParent

    @parent.setter
    def parent(self, node):
        self.nodeParent = node

    def __str__(self) -> str:
        return str(self.pos)



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



    def addNodes(self) -> None:
        """Method to populate the graph with all the walls and walkable paths.
           To be called inside the __init__ method"""
        # Add all the neighbors
        for j in range(self.mapSize[0]): #y
            # For any advancement in the y create a new column in the grid
            self.nodeGrid.append([])
            current_y = self.nodeGrid[j]
            for i in range(self.mapSize[1]): #x
                newNode = AstarNode((j,i), self.map[j][i])
                current_y.append(newNode)
                
        # NOTE: We do not need to add edges because we can sum values in x or y
        # component and search inside self.nodeGrid

    def getNodeFromPos(self, pos: Tuple[int, int]):
        return self.nodeGrid[pos[0]][pos[1]]

    def getNodeLegalNeighbors(self, node): #Get walls from self.map
        """Get legal neighboring nodes from a specified node"""
        x,y = node.pos
        x_int, y_int = int(x + 0.5), int(y + 0.5)
        neighborNodes: List[AstarNode] = []
        for dir, vec in Actions._directionsAsList:
            dx, dy = vec
            next_x = x_int + dx
            if next_x < 0 or next_x >= self.mapSize[0]: continue

            next_y = y_int + dy
            if next_y < 0 or next_y >= self.mapSize[1]: continue

            if not self.map[next_x][next_y]: neighborNodes.append(self.getNodeFromPos((next_x, next_y)))

        return neighborNodes

    # def restartHcost(self) -> None:
    #     "Set the Hcost of all nodes to the max for every iteration of  the algorithm"
    #     for i in range(self.mapSize[0]): #x
    #         for j in range(self.mapSize[1]): #y
    #             self.nodeGrid[i][j].hCost = maxsize


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
                movementToNeighborCost: int = currentNode.gCost +\
                        util.manhattanDistance(currentNode.pos, neighbor.pos)
                if (movementToNeighborCost < neighbor.gCost) or (neighbor not in openNodes):
                    # Update gCost and hCost
                    neighbor.gCost = movementToNeighborCost
                    neighbor.hCost = util.manhattanDistance(neighbor.pos, targetPos)

                    # Set the current node as the parent of the precedent node
                    neighbor.parent = currentNode

                    # check if the neighbor is in the list of open nodes, and if not, add it
                    if neighbor not in openNodes:
                        openNodes.append(neighbor)

    def getMovementVector(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> Tuple[int, int]:
        "Compute the distance vector of two nodes"
        return (pos2[0] - pos1[0], pos2[1] - pos1[1])

    def buildPathDirections(self, startNode: AstarNode, endNode: AstarNode) -> List[str]:
        """Method to build a path after the pacman Agent calls 
        findPath from it's position"""
        path: List[AstarNode] = []
        pathDir: List[str] = []
        
        # Trace the path backwards using the parents
        currentNode: AstarNode = endNode

        while not (currentNode is startNode):
            #NOTE: Path will be in reverse
            path.append(currentNode)
            # Go to the next node
            currentNode = currentNode.parent

        # Finally append the initial node
        path.append(startNode)

        # Now we have all the nodes, convert the nodes into directions
        for i in range(len(path) - 1):
            # Get the movement difference between the two nodes
            movement = self.getMovementVector(path[i + 1].pos, path[i].pos)
            # Convert the x, y tuple into a direction (NORTH, SOUTH, etc)
            dirMov = self.posToDirection[movement]
            pathDir.append(dirMov)


        # Return the reversed list
        return pathDir[::-1]

    def convertPathNodesToPathDirections(self, path: List[AstarNode]) -> List[Directions]:
        """Convert a trail of nodes into a direction path that
        Pacman can understand"""

        pathDir: List[Directions] = []

        for i in range(len(path) - 1):
            path[i]

        return pathDir
