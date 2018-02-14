# -*- coding: utf-8 -*-
# searchAgents.py
# ---------------
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

#Traducido al español por Juan Antonio Fonseca Méndez
#Para el curso de Inteligencia Artificial PROTECO 2016 UNAM



"""
Este archivo contiene todos los agentes que pueden ser seleccionados para controlar
a Pacman. Para seleccionar un agente, usa la opcion -p al correr pacman.py. 
Los argumentos pueden ser pasados a tu agente usando -a. Por ejemplo, para cargar
el agente SearchAgent(agente basico de busqueda) que usa dfs, corre el siguiente
comando:

> python pacman.py -p SearchAgent -a fn=depthFirstSearch

Los comandos para invocar otras estrategias de busqueda pueden ser encontradas en
la descripcion del proyecto

Por favor, solo cambia las partes del archivo que se te piden, busca las lineas
que dicen
"*** TU CODIGO AQUI ***"
Las partes que tienes que llenar estan mas o menos a 3/4 del archivo hacia abajo
Sigue la descripcion del proyecto para mas detalles

Buena suerte y buena busqueda
"""

from game import Directions
from game import Agent
from game import Actions
import util
import time
import search

class GoWestAgent(Agent):
    "Un agente que va al este hasta que no puede mas"

    def getAction(self, state):
        "El agente recibe un GameState (definido en pacman.py)."
        if Directions.WEST in state.getLegalPacmanActions():
            return Directions.WEST
        else:
            return Directions.STOP

#######################################################
# Esta porcion del codigo esta escrita para ti, pero  #
# solo funcionara despues de que llenes search.py     #
#######################################################

class SearchAgent(Agent):
    """
    Este agente de busqueda muy general encuentra un camino usando el 
    algoritmo proporcionado para un problema de busqueda proporcionado,
    despues regrea las acciones para seguir ese camino

    Por defecto, este agente corre DFS en un PositionSearchProblem para 
    encontrar la posición (1,1)

    Las opciones para fn incluyen:
    depthFirstSearch o dfs
    breadthFirstSearch o bfs

    Nota: NO DEBERIAS cambiar ningun codigo en SearchAgent
    """

    def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
        # Advertencia: un poco de magia avanzada de Python se usa abajo para encontrar las funciones y problemas correctos

        # Obtiene la funcion de busqueda del nombre y la heuristica
        if fn not in dir(search):
            raise AttributeError, fn + ' is not a search function in search.py.'
        func = getattr(search, fn)
        if 'heuristic' not in func.func_code.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
            elif heuristic in dir(search):
                heur = getattr(search, heuristic)
            else:
                raise AttributeError, heuristic + ' is not a function in searchAgents.py or search.py.'
            print('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))
            # Nota: este pequeno truco pythonero combina el algoritmo de busqueda y la heuristica
            self.searchFunction = lambda x: func(x, heuristic=heur)

        # Obtiene el tipo de problema de busqueda del nombre
        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError, prob + ' is not a search problem type in SearchAgents.py.'
        self.searchType = globals()[prob]
        print('[SearchAgent] using problem type ' + prob)

    def registerInitialState(self, state):
        """
        Este es el primer momento en que el agente ve la distribucion del tablero
        Aqui, escogemos un camino a la meta. En esta fase, el agente debe procesar
        el camino a la meta y guardarlo en una variable local.
        Todo el trabajo se hace en este metodo!!

        state: un objeto GameState (de pacman.py)
        """
        if self.searchFunction == None: raise Exception, "No search function provided for SearchAgent"
        starttime = time.time()
        problem = self.searchType(state) # Hace un problema de busqueda nuevo
        self.actions  = self.searchFunction(problem) # Encuentra un camino, aqui se manda a llamar lo que ya programamos
        totalCost = problem.getCostOfActions(self.actions)
        print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
        if '_expanded' in dir(problem): print('Search nodes expanded: %d' % problem._expanded)

    def getAction(self, state):
        """
        Regresa la siguiente accion del camino elegido anteriormente
        (en registerInitialState). Regresa Directions.STOP si no hay 
        mas acciones que tomar

        state: un objeto GameState (pacman.py)
        """
        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP

class PositionSearchProblem(search.SearchProblem):
    """
    Un problema de busqueda define un espacio de estados, estado inicial, prueba
    de meta, funcion de sucesores y funcion de costos. Este problema de busqueda
    puede ser usado para encontrar caminos a un punto en particular en el tablero
    de pacman.
    El espacio de estados consiste en las posiciones (x,y) en un juego de pacman

    Nota: este problema de busqueda esta completamente especificado, no necesitas cambiarlo
    """

    def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True, visualize=True):
        """
        Almacena el inicio y la meta

        gameState: un objeto GameState (pacman.py)
        costFn: una funcion del estado de busqueda (tupla) a un numero no negativo
        goal: una posicion en el gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print 'Warning: this does not look like a regular search maze'

        # PAra visualizacion
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # NO LO CAMBIES

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable

        return isGoal

    def getSuccessors(self, state):
        """
        Regresa los estados sucesores, las acciones que estos requieren y costo de 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append( ( nextState, action, cost) )

        # Bookkeeping for display purposes
        self._expanded += 1 # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999.
        """
        if actions == None: return 999999
        x,y= self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x,y))
        return cost

class StayEastSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the West side of the board.

    The cost function for stepping into a position (x,y) is 1/2^x.
    """
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: .5 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn, (1, 1), None, False)

class StayWestSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the East side of the board.

    The cost function for stepping into a position (x,y) is 2^x.
    """
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: 2 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn)

def manhattanHeuristic(position, problem, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def euclideanHeuristic(position, problem, info={}):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

#########################################################
# Esta porcion esta incompleta. Hora de escribir codigo #
#########################################################
#Tarea 1 y 2 del proyecto AQUI
class CornersProblem(search.SearchProblem):
    """
    Este problema de busqueda encuentra caminos pasando todas las esquinas
    de la distribucion

    Debes seleccionar un espacio de estados adecuado y una funcion de sucesion
    """

    def __init__(self, startingGameState):
        """
        Guarda las paredes, la posicion inicial de pacman y las esquinas
        Stores the walls, pacman's starting position and corners.

        Todas las variables llamadas "self." corresponden a atributos, por
        lo que se pueden utilizar en cualquiera de las funciones del problema
        """
        #Variable que almacena todas las variables como una matriz. Se puede usar en las otras fnciones
        self.walls = startingGameState.getWalls()
        #Posicion inicial de pacman que se puede usar en las demas funciones
        self.startingPosition = startingGameState.getPacmanPosition()
        top, right = self.walls.height-2, self.walls.width-2
        #Lista de todas las esquinas del mapa. Se pueden usar en las demas funciones
        self.corners = ((1,1), (1,top), (right, 1), (right, top))
        #Este for me permite determinar si en ese punto, SOLO PARA EL ESTADO INICIAL
        #hay comida en las esquinas
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print 'Warning: no food in corner ' + str(corner)
        self._expanded = 0 # NO LO CAMBIES; numero de nodos expandidos
        # Por favor anade aqui cualquier codigo que te gustaria usar en la
        # inicializacion del problema
        "*** TU CODIGO AQUI ***"

    def getStartState(self):
        """
        Regresa el estado inicial (en el espacio de busqueda, no en el estado total de pacman)
        """
        "*** TU CODIGO AQUI ***"
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
        Regresa si el estado actual es una meta del problema
        """
        "*** TU CODIGO AQUI ***"
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
        Regresa los estados sucesores, las acciones que requiere cada uno, y un costo de 1
        Returns successor states, the actions they require, and a cost of 1.

         Revisar de nuevo search.py para recordar como debe estar organizado lo que regresa
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            # Anade un estado sucesor a la lista solo si la accion es legal. 
            # Aqui hay un fragmento de codigo para darse cuenta si la nueva posicion pega
            # en una pared
            #   x,y = currentPosition
            #   dx, dy = Actions.directionToVector(action)
            #   nextx, nexty = int(x + dx), int(y + dy)
            #   hitsWall = self.walls[nextx][nexty]   #hitsWall es un booleano

            "*** TU CODIGO AQUI ***"

        self._expanded += 1 # DO NOT CHANGE
        return successors

    def getCostOfActions(self, actions):
        """
        Regresa el costo de una secuencia particular de acciones. Si esas acciones
        incluyen un movimiento ilegal, regresa 9999999. Esta funcion se implemnto 
        por ti
        """
        if actions == None: return 999999
        x,y= self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)


def cornersHeuristic(state, problem):
    """
    TAREA 2
    Una heuristica para el CornersProblem que TU definiste
      state: El estado actual en la busqueda (depende de la estructura que escogiste)

      problem: La instancia del CornersProblem para la distribucion actual.

    Esta funcion debe siempre regresar un numero que sea un limite inferior en el
    camino mas corto del estado a la meta del problema. Debe ser admisible
    """
    corners = problem.corners # Estas son las esquinas del problemar coordinates
    walls = problem.walls # Estas son las paredes del laberinto, como una Grid (pacman.py)

    "*** TU CODIGO AQUI ***"
    return 0 # Solucion trivial actual. Eliminar cuando hayes creado tu solucion

class AStarCornersAgent(SearchAgent):
    "Un SearchAgent para el problema de la comida usando A* y foodHeuristic"
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, cornersHeuristic)
        self.searchType = CornersProblem

class FoodSearchProblem:
    """
    Un problema de busqueda asociado a encontrar un camino que recolecta toda la comida
    en un juego de pacman
    El problema ya esta implementado para ti

    En este problema, un estado de busqueda es una tupla (pacmanPosition, foodGrid)
        pacmanPosition: una tupla (x,y) de enteros especificando la posicion de Pacman
        foodGrid:       una Grid(ver game.py) de True o False, especificando la comida restante
    """
    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0 # DO NOT CHANGE
        self.heuristicInfo = {} # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        self._expanded += 1 # NO CAMBIAR
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append( ( ((nextx, nexty), nextFood), direction, 1) )
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x,y= self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost

class AStarFoodSearchAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, foodHeuristic)
        self.searchType = FoodSearchProblem

def foodHeuristic(state, problem):
    """
    Tu heuristica para el FoodSearchProblem va aqui.

    Esta heuristica debe ser consistente para asegurar que sea correcto. Primero
    intenta encontrar una heuristica admisible; casi todas las heuristica admisibles
    van a ser consistentes tambien

    Si usar A* siempre encuentra una solucion que es peor que la que encuentra UCS
    tu heuristica NO ES consistente, y probablemente ni siquiera sea admisible.
    Por otro lado, heuristicas inadmisibles o inconsistentes pueden encontrar soluciones
    optimas asi que ten cuidado

    El estado es una tupla (pacmanPosition,foodGrid) donde foodGrid es una Grid
    (ver game.py) (una matriz) ya sea de Verdadero o False. Puedes llamar el metodo
    foodGrid.asList() para obtener una lista de coordinadas con comida en su lugar.

    Si quieres acceder a informacion como las paredes, capsulas, etc., puedes 
    obtenerla del problema (parametro problem). 
    Por ejemplo, problem.walls te da una Grid de donde estan las paredes. 

    Si quieres "almacenar" informacion para ser reusada en otras llamadas a
    esta heuristica, entonces hay un diccionario llamado problem.heuristicInfo
    que puedes usar. Por ejemplo, si solo quieres contar las paredes una vez
    y guardar ese valor puedes escribir: 
    problem.heuristicInfo['wallCount'] = problem.walls.count()
    
    Llamadas subsecuentes a esta heuristica pueden acceder a 
    problem.heuristicInfo['wallCount']
    """
    position, foodGrid = state
    "*** TU CODIGO AQUI ***"
    return 0

class ClosestDotSearchAgent(SearchAgent):
    """Busqueda por toda la comida usando una secuencia de busquedas mas pequeñas"""
    def registerInitialState(self, state):
        self.actions = []
        currentState = state
        while(currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState) # La pieza faltante
            self.actions += nextPathSegment
            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    t = (str(action), str(currentState))
                    raise Exception, 'findPathToClosestDot returned an illegal move: %s!\n%s' % t
                currentState = currentState.generateSuccessor(0, action)
        self.actionIndex = 0
        print 'Path found with cost %d.' % len(self.actions)

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Aqui hay algunos elementos utiles del estado inicial
        #Posicion incial
        startPosition = gameState.getPacmanPosition()
        #Comida
        food = gameState.getFood()
        print food
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState)

        "*** TU CODIGO AQUI ***"
        #util.raiseNotDefined()

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    Un problema definido para encontrar un camino a cualquier comida.

    Este problema de busqueda es igual al PositionSearchProblem, pero tiene
    una prueba de meta diferente, que necesitas llenar abajo. El espacio de estados
    y la funcion de sucesion no necesitan ser cambiados.

    La definicion de la clase arriba, AnyFoodSearchProblem(PositionSearchProblem),
    hereda los metodos de PositionSearchProblem.

    Puedes usar este problema de busqueda para que al resolverlo con alguno de los algoritmos
    con la funcion:
    search.depthFirstSearch(este problema), o cualquiera de bfs o UCS
    Para A* es con
    search.aStarSearch(un problema de estos)

    Puedes usar este problema para ayudarte a llenar el metodo findPathToClosestDot.
    """

    def __init__(self, gameState):
        "Guarda informacion del gameState. No necesitas cambiar esto."
        # Guarda la comida para referencias futuras
        self.food = gameState.getFood()

        # Guarda informacion del PositionSearchProblem (no necesitas cambiarlo)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # NO CAMBIAR

    def isGoalState(self, state):
        """
        El estado es la posicion de Pacman. Llena esta funcion con una prueba de meta que
        completara la definicion de este problema.
        """
        x,y = state

        "*** TU CODIGO AQUI ***"
        util.raiseNotDefined()

def mazeDistance(point1, point2, gameState):
    """
    Regresa la distancia en pasos dentro del laberinto entre 2 puntos, usando las
    funciones de busqueda que ya tienes. El gameState puede ser cualquier estado del mundo
    La posicion de pacman en este estado es ignorada.

    Ejemplo de uso: mazeDistance( (2,4), (5,6), gameState)

    Este metodo puede ser util para la tarea 4.
    """
    x1, y1 = point1
    x2, y2 = point2
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
    return len(search.bfs(prob))
