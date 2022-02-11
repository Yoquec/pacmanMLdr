# keyboardAgents.py
# -----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley.
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import Agent
from game import Directions
from game import GameStateData
import random


##Isa
import sys


class KeyboardAgent(Agent):
   # NOTE: Arrow keys also work.
    WEST_KEY  = 'a'
    EAST_KEY  = 'd'
    NORTH_KEY = 'w'
    SOUTH_KEY = 's'
    STOP_KEY = 'q'

    def __init__( self, index = 0 ):

        self.lastMove = Directions.STOP
        self.index = index
        self.keys = []

    def getAction( self, state):
        from graphicsUtils import keys_waiting
        from graphicsUtils import keys_pressed
        keys = keys_waiting() + keys_pressed()
        if keys != []:
            self.keys = keys

        legal = state.getLegalActions(self.index)
        move = self.getMove(legal)

        if move == Directions.STOP:
            # Try to move in the same direction as before
            if self.lastMove in legal:
                move = self.lastMove

        if (self.STOP_KEY in self.keys) and Directions.STOP in legal: move = Directions.STOP

        if move not in legal:
            move = random.choice(legal)

        self.lastMove = move
        return move

    def getMove(self, legal):
        move = Directions.STOP
        if   (self.WEST_KEY in self.keys or 'Left' in self.keys) and Directions.WEST in legal:  move = Directions.WEST
        if   (self.EAST_KEY in self.keys or 'Right' in self.keys) and Directions.EAST in legal: move = Directions.EAST
        if   (self.NORTH_KEY in self.keys or 'Up' in self.keys) and Directions.NORTH in legal:   move = Directions.NORTH
        if   (self.SOUTH_KEY in self.keys or 'Down' in self.keys) and Directions.SOUTH in legal: move = Directions.SOUTH
        return move        

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
        
