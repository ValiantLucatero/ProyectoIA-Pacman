# -*- coding: utf-8 -*-
# search.py
# ---------
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
En search.py, implementamos los algoritmos de busqueda genericos, que son 
llamados por los agentes Pacman (en searchAgents.py)
"""

import util

class SearchProblem:
    """
    Esta clase establece la estructura de un problema de busqueda,
    pero no implementa ninguno de los metodos.

    No es necesario que modifiques absolutamente nada de esta clase, jamas.
    """

    def getStartState(self):
        """
        Regresa el estado inicial del problema de busqueda
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Estado de busqueda

        Regresa True si, y solo si, el estado es una meta valida.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: estado de busqueda

        Para un estado dado, esto deberia regresar una lista de tripletas
        (successor, action, stepCost)
        donde

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' Es el sucesor del estado actual
        'action' es la accion requerida para llegar ahi y 'stepCost' es el costo
        de expandir ese nodo
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: Una lista de acciones por hacer

        Este metodo regresa el costo total de una secuencia particular de acciones
        Debe estar compuesta por movimientos legales.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Tu algorimto debe regresar una lista de acciones que alcancen la meta
    Asegurate de implementar el algoritmo de busqueda por grafo

    Para iniciar, puede que te interese probar estos comandos simples para
    entender el problema que esta siendo pasado

    print "Inicio:", problem.getStartState()
    print "El inicio es una meta?", problem.isGoalState(problem.getStartState())
    print "Sucesores del inicio:", problem.getSuccessors(problem.getStartState())
    """
    "*** Tu codigo aqui ***"
    contenedor = util.Stack()
    contenedor.push((problem.getStartState(),[]))
    revisados = set()
    while True:
        if contenedor.isEmpty():
            return []
        #A esto equivaldria la asignacion multiple de python
        #nodo = contenedor.pop()
        #estado = nodo[0]
        #path = nodo[1]
        estado,path = contenedor.pop()
        if problem.isGoalState(estado):
            return path
        if estado not in revisados:
            revisados.add(estado)
            sucesores = problem.getSuccessors(estado)
            if sucesores != []:
                for hijo in sucesores:
                    estadoSig = hijo[0]
                    pathAlHijo = path + [hijo[1]]
                    contenedor.push((estadoSig,pathAlHijo))

def breadthFirstSearch(problem):
    """Busca el nodo menos profundo"""
    "*** Tu codigo aqui***"
    contenedor = util.Queue()
    contenedor.push((problem.getStartState(),[]))
    revisados = set()
    while True:
        if contenedor.isEmpty():
            return []
        estado,path = contenedor.pop()
        if problem.isGoalState(estado):
            return path
        if estado not in revisados:
            revisados.add(estado)
            sucesores = problem.getSuccessors(estado)
            if sucesores != []:
                for hijo in sucesores:
                    estadoSig = hijo[0]
                    pathAlHijo = path + [hijo[1]]
                    contenedor.push((estadoSig,pathAlHijo))

def uniformCostSearch(problem):
    """Busca el nodo con el costo menor."""
    "*** YOUR CODE HERE ***"
    contenedor = util.PriorityQueue()
    visitados = set()
    contenedor.push((problem.getStartState(),[],0),0)
    while True:
        if contenedor.isEmpty():
            return []
        estado,path,costoPlan = contenedor.pop()
        if problem.isGoalState(estado):
            return path
        if not estado in visitados:
            visitados.add(estado)
            sucesores = problem.getSuccessors(estado)
            if sucesores != []:
                for hijo in sucesores:
                    estadoSig = hijo[0]
                    if not estadoSig in visitados:
                        pathAlHijo = path + [hijo[1]]
                        costoHastaElHijo = hijo[2] + costoPlan
                        contenedor.push((estadoSig,pathAlHijo,costoHastaElHijo),costoHastaElHijo)

def nullHeuristic(state, problem=None):
    """
    Heuristica trivial
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Busca el nodo que tiene la menor combinacion de costo y heuristica primero."""
    "*** TU CODIGO AQUI ***"
    contenedor = util.PriorityQueue()
    visitados = set()
    contenedor.push((problem.getStartState(),[],0),0+heuristic(problem.getStartState(),problem))
    while True:
        if contenedor.isEmpty():
            return []
        estado,path,costoPlan = contenedor.pop()
        if problem.isGoalState(estado):
            return path
        if not estado in visitados:
            visitados.add(estado)
            sucesores = problem.getSuccessors(estado)
            if sucesores != []:
                for hijo in sucesores:
                    estadoSig = hijo[0]
                    if not estadoSig in visitados:
                        pathAlHijo = path + [hijo[1]]
                        costoHastaElHijo = hijo[2] + costoPlan
                        contenedor.push((estadoSig,pathAlHijo,costoHastaElHijo),costoHastaElHijo+heuristic(estadoSig,problem))



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
