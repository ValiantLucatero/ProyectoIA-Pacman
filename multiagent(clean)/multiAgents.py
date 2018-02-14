# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

#Traduccion al espanol por Juan Antonio Fonseca Mendez (juan@proteco.mx)
#Para el curso de Inteligencia Artificial 2 2016


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      Un agente reflejo escoge una accion en cada punto de eleccion examinando
      sus alternativas via una funcion de evaluacion de estado.

      El siguiente codigo se provee como una guia. Eres libre de cambiarlo
      en cualquier forma que encuentres conveniente, mientras no toques los encabezados.
    """


    def getAction(self, gameState):
        """
        No necesitas cambiar este metodo, pero si quieres, adelante.
        You do not need to change this method, but you're welcome to.

        getAction escoge entre las mejores opciones de acuerdo a la funcion de evaluacion.

        Justo como en el proyecto anterior, getAction toma un GameState y regresa
        alguna Directions.X para alguna X en el conjunto {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        ## Recolecta los movimientos legales y estados sucesores
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        ## Escoge una de las mejores acciones
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        "Anade mas de tu codigo aqui si lo deseas"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Disenia una mejor funcion de evaluacion aqui.

        La funcion de evaluacion recibe los actuales y propuestos GameStates
        sucesores (descritos en pacman.py) y regresa un numero, donde mas alto es mejor.

        El codigo abajo extrae algo de informacion util del estado, como
        la comida restante (newFood) y la posicion de pacman despues de moverse (newPos).
        newScaredTimes tiene el numero de movimientos que cada fantasma va a permanecer
        asustado porque Pacman se comio una pildora especial.

        Imprime estas variables para ver que te dan y luego combinalas para crear una
        funcion de evaluacion maestra.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** Tu codigo aqui ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      Esta funcion de evaluacion solo regresa el puntaje del estado
      El puntaje es el mismo que se ve en la GUI.

      Esta funcion de evaluacion esta prevista para su uso con agentes de
      busqueda con adversarios (no agentes reflejo).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      Esta clase provee algunos elementos comunes para todos tus buscadores
      multiagente. Cualquier metodo definido aqui estara disponible para
      el MinimaxPacmanAgent, AlphaBetaPacmanAgent y ExpectimaxPacmanAgent.

      No *necesitas* cambiar algo aqui, pero puedes si quieres, anadir funciones
      a todos tus agentes de busqueda con adversarios. Por favor no borres nada, eso si

      Nota: esta es una clase abstracta: una que no debe ser instanciada nunca.
      Solo esta parcialmente especificada y diseniada para ser heredada. Agent (en game.py)
      es otra clase abstracta.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman siempre es el agente de indice 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Tu agente Minimax
    """

    def getAction(self, gameState):
        """
          Regresa la accion minimax para el gameState actual usando self.depth
          y self.evaluationFunction.

          Aqui hay algunos metodos que pueden ser utiles cuando se implemente minimax.

          gameState.getLegalActions(agentIndex):
            Regresa una lista de acciones legales para un agente.
            agentIndex=0 es Pacman, los fantasmas son >= 1

          gameState.generateSuccessor(agentIndex, action):
            Regresa el estado de juego sucesor despues de que un agente toma una accion

          gameState.getNumAgents():
            Regresa el numero total de agentes en este juego

          gameState.isWin():
            Regresa si un estado de juego es uno de haber ganado

          gameState.isLose():
            Regresa si un estado de juego es que perdio pacman
        """
        "*** Tu codigo aqui ***"
        def maxvalue(gameState, depth, numghosts):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            v = -(float("inf"))
            legalActions = gameState.getLegalActions(0)
            for action in legalActions:
                v = max(v, minvalue(gameState.generateSuccessor(0, action), depth - 1, 1, numghosts))
            return v

        def minvalue(gameState, depth, agentindex, numghosts):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            v = float("inf")
            legalActions = gameState.getLegalActions(agentindex)
            if agentindex == numghosts:
                for action in legalActions:
                    v = min(v, maxvalue(gameState.generateSuccessor(agentindex, action), depth - 1, numghosts))
            else:
                for action in legalActions:
                    v = min(v, minvalue(gameState.generateSuccessor(agentindex, action), depth, agentindex + 1, numghosts))
            return v
        legalActions = gameState.getLegalActions()
        numghosts = gameState.getNumAgents() - 1
        bestaction = Directions.STOP
        score = -(float("inf"))
        for action in legalActions:
            nextState = gameState.generateSuccessor(0, action)
            prevscore = score
            score = max(score, minvalue(nextState, self.depth, 1, numghosts))
            if score > prevscore:
                bestaction = action
        return bestaction
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Tu agente minimax con poda alpha beta (question 3)
    """

    def getAction(self, gameState):
        """
          Regresa la accion minimax usando self.depth y self.evaluationFunction
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** Tu codigo aqui ***"
        util.raiseNotDefined()

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    print "Posicion: ",str(newPos)
    print "Comida: ",newFood.asList()
    print "Estado fantasmas: ", newGhostStates
    print "Tiempos de susto: ", newScaredTimes
    print ":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"

    valor = 0

    valor += 20* currentGameState.getScore()

    minDistPil = (float('inf'))

    for pildora in newFood.asList()+currentGameState.getCapsules():
		minDistPil = min(manhattanDistance(newPos,pildora),minDistPil)

    valor += 10 * 1/minDistPil

    fantDist = []

    for fantasma in newGhostStates:
		fantDist.append(manhattanDistance(fantasma.getPosition(),newPos))

    for val in range(len(fantDist)):
		if newScaredTimes[val] == 0 and fantDist[val] < 2:
			valor -= 30* 1/max(fantDist[val],0.00001)
		else:
			valor += newScaredTimes[val] * 1/max(fantDist[val],0.00001)

    return valor

# Abbreviation
better = betterEvaluationFunction
