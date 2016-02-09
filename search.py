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
       if state in visited:  # DON'T go to a coord you've already visited
           continue
       visited.append(state)
       options = problem.getSuccessors(state) # options is a list of choices
       for i in options:
           newState = i[0]
           newMove = i[1] 
           newMoves = moves[:]
           if newState not in visited:
               newMoves.append(newMove)
               frontier.push( (newState, newMoves, 0) )
    
  print "No solution found"              
  util.raiseNotDefined()

def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  visited = [] # a list of tuples I have been to (x,y)
  frontier = util.Queue() # a stack of tuples to visit ( (x,y), [s,w,n,e], 1 )
  
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
       if state in visited:  # DON'T go to a coord you've already visited
           continue
       visited.append(state)
       options = problem.getSuccessors(state) # options is a list of choices
       for i in options:
           newState = i[0]
           newMove = i[1] 
           newMoves = moves[:]
           if newState not in visited:
               newMoves.append(newMove)
               frontier.push( (newState, newMoves, 0) )
  
  print "No solution found"  
             
  util.raiseNotDefined()
  
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  
  # Format for nodes: ( (x,y) , [path], totalCost ) - now BOTH path and cost increment!
  # goal: minimize totalCost
  # return: [path]
  
  visited = [] # a list of tuples I have been to of form (x,y)
  
  def getTotalCost( successor ):
      return successor[2]
  
  frontier = util.PriorityQueueWithFunction(getTotalCost) # a PQ list of neighboring states (make sure to CHECK FOR VISITED!) - PQ gets you the lowest with pop()
  moves = []
  
  startState = problem.getStartState() # starting coords
  
  if problem.isGoalState(startState): # no moves needed if start at goal
      return moves
      
  frontier.push( (startState, moves, 0) ) # push starting state with a TOTAL COST OF 0

  while(not frontier.isEmpty()):
       current = frontier.pop() # gets you the node with the lowest TOTAL COST (weighting factor)
       state = current[0] # grab the COORDINATE we're on right now
       moves = current[1] # grab the current list of MOVES taken to get to this spot
       cost = current[2] # grab the TOTAL COST so far
       if problem.isGoalState(state): 
           return moves
       if state in visited:  # DON'T go to a coord you've already visited
           continue
       visited.append(state)
       options = problem.getSuccessors(state) # options is a list of choices
       for i in options:
           newState = i[0]
           newMove = i[1] 
           newCost = i[2]
           newMoves = moves[:]
           if newState not in visited:
               newMoves.append(newMove)
               frontier.push( (newState, newMoves, cost + newCost) )
  
  print "No solution found" 
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
  
  # 'lowest combined cost' --> use UCS algo
  # 'lowest heuristic' 
      # def manhattanHeuristic(position, problem, info={}):
      #    "The Manhattan distance heuristic for a PositionSearchProblem"
      #    xy1 = position
      #    xy2 = problem.goal
      #    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
      
  # total cost: UCS cost + heuristic 
  
  # Format for nodes: ( (x,y) , [path], totalCost ) - now BOTH path and cost increment!
  # goal: minimize totalCost
  # return: [path]
  
  visited = [] # a list of tuples I have been to of form (x,y)
  
  def getTotalCost( successor ):
      return successor[2]
  
  frontier = util.PriorityQueueWithFunction(getTotalCost) # a PQ list of neighboring states (make sure to CHECK FOR VISITED!) - PQ gets you the lowest with pop()
  moves = []
  
  startState = problem.getStartState() # starting coords
  
  if problem.isGoalState(startState): # no moves needed if start at goal
      return moves
      
  frontier.push( (startState, moves, heuristic(startState,problem) ) ) # push starting state with a TOTAL COST OF 0 + heuristic 

  while(not frontier.isEmpty()):
       current = frontier.pop() # gets you the node with the lowest TOTAL COST (weighting factor)
       state = current[0] # grab the COORDINATE we're on right now
       moves = current[1] # grab the current list of MOVES taken to get to this spot
       cost = current[2] # grab the TOTAL COST so far
       if problem.isGoalState(state): 
           return moves
       if state in visited:  # DON'T go to a coord you've already visited
           continue
       visited.append(state)
       options = problem.getSuccessors(state) # options is a list of choices
       for i in options:
           newState = i[0]
           newMove = i[1] 
           newCost = i[2]
           newMoves = moves[:]
           if newState not in visited:
               newMoves.append(newMove)
               frontier.push( (newState, newMoves, cost + newCost + heuristic(newState,problem)) )
  
  print "No solution found" 
  util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
