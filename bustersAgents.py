from __future__ import print_function
from tkinter.tix import Tree
from typing import Tuple, List
# import csv bustersAgents.py
# ----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from builtins import range
from builtins import object
import util
from game import Agent
from game import Directions
from keyboardAgents import KeyboardAgent
import inference
import busters
from AstarTest import AstarNode, AstarGrid

class NullGraphics(object):
    "Placeholder for graphics"
    def initialize(self, state, isBlue = False):
        pass
    def update(self, state):
        pass
    def pause(self):
        pass
    def draw(self, state):
        pass
    def updateDistributions(self, dist):
        pass
    def finish(self):
        pass

class KeyboardInference(inference.InferenceModule):
    """
    Basic inference module for use with the keyboard.
    """
    def initializeUniformly(self, gameState):
        "Begin with a uniform distribution over ghost positions."
        self.beliefs = util.Counter()
        for p in self.legalPositions: self.beliefs[p] = 1.0
        self.beliefs.normalize()

    def observe(self, observation, gameState):
        noisyDistance = observation
        emissionModel = busters.getObservationDistribution(noisyDistance)
        pacmanPosition = gameState.getPacmanPosition()
        allPossible = util.Counter()
        for p in self.legalPositions:
            trueDistance = util.manhattanDistance(p, pacmanPosition)
            if emissionModel[trueDistance] > 0:
                allPossible[p] = 1.0
        allPossible.normalize()
        self.beliefs = allPossible

    def elapseTime(self, gameState):
        pass

    def getBeliefDistribution(self):
        return self.beliefs


class BustersAgent(object):
    "An agent that tracks and displays its beliefs about ghost positions."

    def __init__( self, index = 0, inference = "ExactInference", ghostAgents = None, observeEnable = True, elapseTimeEnable = True):
        inferenceType = util.lookup(inference, globals())
        self.inferenceModules = [inferenceType(a) for a in ghostAgents]
        self.observeEnable = observeEnable
        self.elapseTimeEnable = elapseTimeEnable

    def registerInitialState(self, gameState):
        "Initializes beliefs and inference modules"
        import __main__
        self.display = __main__._display
        for inference in self.inferenceModules:
            inference.initialize(gameState)
        self.ghostBeliefs = [inf.getBeliefDistribution() for inf in self.inferenceModules]
        self.firstMove = True

    def observationFunction(self, gameState):
        "Removes the ghost states from the gameState"
        agents = gameState.data.agentStates
        gameState.data.agentStates = [agents[0]] + [None for i in range(1, len(agents))]
        return gameState

    def getAction(self, gameState):
        "Updates beliefs, then chooses an action based on updated beliefs."
        #for index, inf in enumerate(self.inferenceModules):
        #    if not self.firstMove and self.elapseTimeEnable:
        #        inf.elapseTime(gameState)
        #    self.firstMove = False
        #    if self.observeEnable:
        #        inf.observeState(gameState)
        #    self.ghostBeliefs[index] = inf.getBeliefDistribution()
        #self.display.updateDistributions(self.ghostBeliefs)
        return self.chooseAction(gameState)

    def chooseAction(self, gameState):
        "By default, a BustersAgent just stops.  This should be overridden."
        return Directions.STOP

class BustersKeyboardAgent(BustersAgent, KeyboardAgent):
    "An agent controlled by the keyboard that displays beliefs about ghost positions."

    def __init__(self, index = 0, inference = "KeyboardInference", ghostAgents = None):
        KeyboardAgent.__init__(self, index)
        BustersAgent.__init__(self, index, inference, ghostAgents)
        self.countActions = 0

    # def getAction(self, gameState):
    #     return BustersAgent.getAction(self, gameState)
    def getAction(self, gameState, grid: AstarGrid):
        """Redefined getAction method to include the map grid. If it receives it,
        delete it"""
        if "Agrid" in globals() or "Agrid" in locals():
            del grid

        return self.chooseAction(gameState)

    def chooseAction(self, gameState):
        # Count a new action
        self.countActions += 1
        return KeyboardAgent.getAction(self, gameState)

    def printLineData(self, gameState) -> str :
        # define variable splits{{{
        pacman_pos = gameState.getPacmanPosition()

        # Check for legal movements
            # Create temp bool array
        legal = [False, False, False, False, False]
            # Get the game state array for the legal actions
        observed_legal = gameState.getLegalActions()

        if "North" in observed_legal:
            legal[0]=True
        if "South" in observed_legal:
            legal[1]=True
        if "East" in observed_legal:
            legal[2]=True
        if "West" in observed_legal:
            legal[3]=True
        if "Stop" in observed_legal:
            legal[4]=True

        # Fix getLivingGhosts()
            # It returns a list of length getNumAgents()
            # Where the first element (pacman) is always false
            # and depending on which ghosts are alive sets a bool
        ghost_living = [False, False, False, False]
        ghost_livingState = gameState.getLivingGhosts()

        for i in range(len(ghost_livingState) - 1):
            if ghost_livingState[i + 1]:
                ghost_living[i] = True

        # Fix ghostPosition 
            # Ghost positions are stricly positive, so 
            # negative values will indicate that the ghosts do
            # not exist
        ghost_positions = [
                [-1, -1],
                [-1, -1],
                [-1, -1],
                [-1, -1]
                ]
        ghost_positionsState = gameState.getGhostPositions()

            # Change the values in ghost_positions depending on the value of the gameState
        for i in range(len(ghost_positionsState)):
            gPos = ghost_positionsState[i]

            for j in range(2):
                ghost_positions[i][j] = gPos[j]

        # fix getGhostDirections()
            # Create an array to store the values for all the ghosts
        ghost_dirs = [None, None, None, None]
        ghost_dirsState = [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)]

            # Update list values
        for i in range(len(ghost_dirsState)):
            ghost_dirs[i] = ghost_dirsState[i]

        # Ghost distances
            # ghost directions
        ghost_dist = [-1, -1, -1, -1]
        ghost_distState = gameState.data.ghostDistances
            
        for i in range(len(ghost_distState)):
            ghost_dist[i] = ghost_distState[i]

        
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

    def printLineDataArff(self, gameState) -> str:
        # It will be the same method, but leaving a space between commas
        # as the adult-data.arff file shows (not necessary though)
        return self.printLineData(gameState).replace(",", ", ")

from distanceCalculator import Distancer
from game import Actions
from game import Directions
import random, sys

'''Random PacMan Agent'''
class RandomPAgent(BustersAgent):

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        
    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food
    
    ''' Print the layout'''  
    def printGrid(self, gameState):
        table = ""
        ##print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table
        
    def chooseAction(self, gameState):
        move = Directions.STOP
        legal = gameState.getLegalActions(0) ##Legal position from the pacman
        move_random = random.randint(0, 3)
        if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
        if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
        if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
        if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
        return move
        
class GreedyBustersAgent(BustersAgent):
    "An agent that charges the closest ghost."

    def registerInitialState(self, gameState):
        "Pre-computes the distance between every two points."
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)

    def chooseAction(self, gameState):
        """
        First computes the most likely position of each ghost that has
        not yet been captured, then chooses an action that brings
        Pacman closer to the closest ghost (according to mazeDistance!).

        To find the mazeDistance between any two positions, use:
          self.distancer.getDistance(pos1, pos2)

        To find the successor position of a position after an action:
          successorPosition = Actions.getSuccessor(position, action)

        livingGhostPositionDistributions, defined below, is a list of
        util.Counter objects equal to the position belief
        distributions for each of the ghosts that are still alive.  It
        is defined based on (these are implementation details about
        which you need not be concerned):

          1) gameState.getLivingGhosts(), a list of booleans, one for each
             agent, indicating whether or not the agent is alive.  Note
             that pacman is always agent 0, so the ghosts are agents 1,
             onwards (just as before).

          2) self.ghostBeliefs, the list of belief distributions for each
             of the ghosts (including ghosts that are not alive).  The
             indices into this list should be 1 less than indices into the
             gameState.getLivingGhosts() list.
        """
        pacmanPosition = gameState.getPacmanPosition()
        legal = [a for a in gameState.getLegalPacmanActions()]
        livingGhosts = gameState.getLivingGhosts()
        livingGhostPositionDistributions = \
            [beliefs for i, beliefs in enumerate(self.ghostBeliefs)
             if livingGhosts[i+1]]
        return Directions.NORTH

class BasicAgentAA(BustersAgent):

    # FIXME: Tener en cuenta la reeimplemetación si alguna vez 
    # descomentamos lo de update beliefs the los agentes
    def getAction(self, gameState, grid: AstarGrid):
        "Redefined getAction method to include the map grid"
        return self.chooseAction(gameState, grid)

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        self.countActions = 0
        
    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food
    
    ''' Print the layout'''  
    def printGrid(self, gameState):
        table = ""
        #print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table


    def printInfo(self, gameState):# {{{
        print("---------------- TICK ", self.countActions, " --------------------------")
        # Map size
        width, height = gameState.data.layout.width, gameState.data.layout.height
        print("Width: ", width, " Height: ", height)
        # Pacman position
        print("Pacman position: ", gameState.getPacmanPosition()) # 
        # Legal actions for Pacman in current position
        print("Legal actions: ", gameState.getLegalPacmanActions()) # 
        # Pacman direction
        print("Pacman direction: ", gameState.data.agentStates[0].getDirection()) # (optional)
        # Number of ghosts
        print("Number of ghosts: ", gameState.getNumAgents() - 1)
        # Alive ghosts (index 0 corresponds to Pacman and is always false)
        print("Living ghosts: ", gameState.getLivingGhosts()) # (optional)
        # Ghosts positions
        print("Ghosts positions: ", gameState.getGhostPositions()) # 
        # Ghosts directions
        print("Ghosts directions: ", [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)])
        # Manhattan distance to ghosts
        print("Ghosts distances: ", gameState.data.ghostDistances) # 
        # Pending pac dots
        print("Pac dots: ", gameState.getNumFood()) # 
        # Manhattan distance to the closest pac dots
        print("Distance nearest pac dots: ", gameState.getDistanceNearestFood()) # 
        #FIXME: how is the getDistanceNearestFood method implemented??
        # Map walls
        print("Map:")
        print( gameState.getWalls())
        # Score
        print("Score: ", gameState.getScore())# }}}
        
        
    def chooseAction(self, gameState, grid: AstarGrid):
        # NOTE: added grid to be injected to the A*{{{
    
        # NOTE: call python busters.py -p BasicAgentAA -g RandomGhost
        self.countActions = self.countActions + 1
        self.printInfo(gameState)

        # NOTE: get the path to get to a ghost
        alive=[]
        ghosts=gameState.getLivingGhosts()
        for i in range(len(ghosts)):
            if ghosts[i]==True:
                alive.append(i)
        
        #We create the Astar algorithm for all the alive ghosts. Also store lengths
        paths=[]
        lengths=[999,999,999,999]

        for i in (alive):
            paths.append(grid.findPath(gameState.getPacmanPosition(), gameState.getGhostPositions()[i-1]))
            
        for i in range(len(alive)):
            lengths[alive[i]-1]=len(paths[i])
        #We calculate which is closer acording to the Astar
        minidx = lengths.index(min(lengths))
        #We get the index of path
        pathidx = alive.index(minidx+1)
        #We select the first movement of the shortest path
        action = paths[pathidx][0]

            
        #We thus calculated which is closer acording to Astar
        return action# }}}

    
    def printLineData(self, gameState) -> str :
        # define variable splits{{{
        pacman_pos = gameState.getPacmanPosition()

        # Check for legal movements
            # Create temp bool array
        legal = [False, False, False, False, False]
            # Get the game state array for the legal actions
        observed_legal = gameState.getLegalActions()

        if "North" in observed_legal:
            legal[0]=True
        if "South" in observed_legal:
            legal[1]=True
        if "East" in observed_legal:
            legal[2]=True
        if "West" in observed_legal:
            legal[3]=True
        if "Stop" in observed_legal:
            legal[4]=True

        # Fix getLivingGhosts()
            # It returns a list of length getNumAgents()
            # Where the first element (pacman) is always false
            # and depending on which ghosts are alive sets a bool
        ghost_living = [False, False, False, False]
        ghost_livingState = gameState.getLivingGhosts()

        for i in range(len(ghost_livingState) - 1):
            if ghost_livingState[i + 1]:
                ghost_living[i] = True

        # Fix ghostPosition 
            # Ghost positions are stricly positive, so 
            # negative values will indicate that the ghosts do
            # not exist
        ghost_positions = [
                [-1, -1],
                [-1, -1],
                [-1, -1],
                [-1, -1]
                ]
        ghost_positionsState = gameState.getGhostPositions()

            # Change the values in ghost_positions depending on the value of the gameState
        for i in range(len(ghost_positionsState)):
            gPos = ghost_positionsState[i]

            for j in range(2):
                ghost_positions[i][j] = gPos[j]

        # fix getGhostDirections()
            # Create an array to store the values for all the ghosts
        ghost_dirs = [None, None, None, None]
        ghost_dirsState = [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)]

            # Update list values
        for i in range(len(ghost_dirsState)):
            ghost_dirs[i] = ghost_dirsState[i]

        # Ghost distances
            # ghost directions
        ghost_dist = [-1, -1, -1, -1]
        ghost_distState = gameState.data.ghostDistances
            
        for i in range(len(ghost_distState)):
            ghost_dist[i] = ghost_distState[i]

        
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

    def printLineDataArff(self, gameState) -> str:
        # It will be the same method, but leaving a space between commas
        # as the adult-data.arff file shows (not necessary though)
        return self.printLineData(gameState).replace(",", ", ")
