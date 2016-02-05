# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm 
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState() -> Start: (5,5) // this is a tuple 
  print "Is the start a goal?", problem.isGoalState(problem.getStartState()) -> Is the start a goal? False
  print "Start's successors:", problem.getSuccessors(problem.getStartState()) -> Start's successors: [((5, 4), 'South', 1), ((4, 5), 'West', 1)]

  """
  "*** YOUR CODE HERE ***"
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  n = Directions.NORTH
  e = Directions.EAST

  visited = [] # a list of tuples I have been to (x,y)
  frontier = util.Stack() # a stack of tuples to visit ( (x,y), [s,w,n,e], 1 )
  
  startState = problem.getStartState() # starting coords
  
  if problem.isGoalState(startState): # no moves needed if start at goal
      return moves
      
  frontier.push( (startState,[],0) )

  while(not frontier.isEmpty()):
       current = frontier.pop() 
       state = current[0] # grab the COORDINATE we're on right now
       moves = current[1] # grab the current list of MOVES taken to get to this spot
       if problem.isGoalState(state): 
           return moves
           # raw_input("Press enter to continue...")
           # break
       if state in visited:  # DON'T go to a coord you've already visited
           continue
       visited.append(state)
       options = problem.getSuccessors(state) # options is a list of choices
       for i in options:
           newState = i[0]
           newMove = i[1] 
           newMoves = moves[:]
           if newState not in visited:
               if newMove == "South":
                   newMoves.append(s)
               elif newMove == "West":
                   newMoves.append(w)
               elif newMove == "North":
                   newMoves.append(n)
               else:
                   newMoves.append(e)
               print( (newState, newMoves) )
               frontier.push( (newState, newMoves, 0) )
    
               
  util.raiseNotDefined()

def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
