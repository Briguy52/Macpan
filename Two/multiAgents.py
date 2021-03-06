# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates() # has len 1
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    # Add some more useful info from pacman.py's GameState
    newScore = successorGameState.getScore()

    if successorGameState.isWin():
        return 99999999
    if successorGameState.isLose():
        return -99999999

    distanceFromGhosts = 0
    for i in newGhostStates:
        distanceFromGhosts += util.manhattanDistance(i.getPosition(),newPos)

    distanceFromFood = 1
    for i in newFood.asList():
        distanceFromFood += util.manhattanDistance(i,newPos)

    distanceFromCapsules = 1
    for i in successorGameState.getCapsules():
        distanceFromCapsules += util.manhattanDistance(i,newPos)

    return distanceFromGhosts + newScore + 1/distanceFromFood + 1/distanceFromCapsules

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    numAgents = gameState.getNumAgents()
    totalGhosts = numAgents - 1

    def getMax(state, depth):
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        moves = state.getLegalActions(0) # get moves to choose from
        bestScore = -99999999999 # Pacman wants to MAX score
        for move in moves:
            successor = state.generateSuccessor(0, move)
            bestScore = max(bestScore, getMin(successor, depth, 1))
        return bestScore

    def getMin(state, depth, agentIndex):
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        if agentIndex > totalGhosts: # run out of ghosts, call Pacman
            return getMax(state, depth-1)
        else:
            bestScore = 999999999999 # Ghosts want to MIN score
            moves = state.getLegalActions(agentIndex) # get moves to choose from
            for move in moves:
                successor = state.generateSuccessor(agentIndex,move)
                bestScore = min(bestScore, getMin(successor, depth, agentIndex+1))
            return bestScore


    moves = gameState.getLegalActions(0) # get moves to choose from

    bestMove = Directions.STOP # always valid
    bestScore = -99999999999

    for move in moves:
        successor = gameState.generateSuccessor(0,move) # Pacman goes first
        score = getMin(successor, self.depth, 1)
        if score > bestScore:
            bestMove = move
            bestScore = score
    print bestScore
    return bestMove

    util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    numAgents = gameState.getNumAgents()
    totalGhosts = numAgents - 1

    # pseudocode from: https://courses.cs.washington.edu/courses/cse473/12sp/slides/09-alphabeta.pdf
    def getMax(state, depth, alpha, beta):
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        moves = state.getLegalActions(0) # get moves to choose from
        bestScore = -99999999999 # Pacman wants to MAX score
        for move in moves:
            successor = state.generateSuccessor(0,move)
            bestScore = max(bestScore, getMin(successor, depth, 1, alpha, beta))
            if bestScore >= beta:
                return bestScore
            alpha = max(bestScore, alpha)
        return bestScore

    def getMin(state, depth, agentIndex, alpha, beta):
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        if agentIndex > totalGhosts: # run out of ghosts, call Pacman
            return getMax(state, depth-1, alpha, beta)
        else:
            bestScore = 999999999999 # Ghosts want to MIN score
            moves = state.getLegalActions(agentIndex) # get moves to choose from
            for move in moves:
                successor = state.generateSuccessor(agentIndex,move)
                bestScore = min(bestScore, getMin(successor, depth, agentIndex+1, alpha, beta))
                if bestScore <= alpha:
                    return bestScore
                beta = min(bestScore, beta)
            return bestScore

    moves = gameState.getLegalActions(0) # get moves to choose from

    bestMove = Directions.STOP # always valid
    bestScore = -99999999999999
    alpha = -99999999999999
    beta = 99999999999999

    for move in moves:
        successor = gameState.generateSuccessor(0,move) # Pacman goes first
        score = getMin(successor, self.depth, 1, alpha, beta)
        if score > bestScore:
            bestMove = move
            bestScore = score
        if bestScore >= beta:
            return bestMove
        alpha = max(bestScore, alpha)
    # print bestScore
    return bestMove

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    numAgents = gameState.getNumAgents()
    totalGhosts = numAgents - 1

    def getMax(state, depth):
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        moves = state.getLegalActions(0) # get moves to choose from
        bestScore = -99999999999 # Pacman wants to MAX score
        for move in moves:
            successor = state.generateSuccessor(0, move)
            bestScore = max(bestScore, getMin(successor, depth, 1))
        return bestScore

    def getMin(state, depth, agentIndex):
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        bestScore = 0
        if agentIndex > totalGhosts: # run out of ghosts, call Pacman
            moves = state.getLegalActions(0) # get moves to choose from
            bestScore += getMax(state, depth-1)

        else:
            moves = state.getLegalActions(agentIndex) # get moves to choose from
            for move in moves:
                successor = state.generateSuccessor(agentIndex,move)
                bestScore += getMin(successor, depth, agentIndex+1)

        return bestScore/len(moves)


    moves = gameState.getLegalActions(0) # get moves to choose from

    bestMove = Directions.STOP # always valid
    bestScore = -99999999999

    for move in moves:
        successor = gameState.generateSuccessor(0,move) # Pacman goes first
        score = getMin(successor, self.depth, 1)
        if score > bestScore:
            bestMove = move
            bestScore = score
    return bestMove


    util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()
