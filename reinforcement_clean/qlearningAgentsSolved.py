# qlearningAgents.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Agente Aprendizaje-Q

      Funciones que hay que llenar:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Variables de instancia a las que tienes acceso
        - self.epsilon (probabilidad de exploracion)
        - self.alpha (razon de aprendizaje)
        - self.discount (razon de descuento)

      Funciones que deberias usar
        - self.getLegalActions(state)
          que regresa la lista de acciones de un estado
    """
    def __init__(self, **args):
        "Puedes inicializar tus valores Q aqui..."
        ReinforcementAgent.__init__(self, **args)
        "*** TU CODIGO AQUI ***"
        self.qValues = util.Counter()

    def getQValue(self, state, action):
        """
          Regresa Q(state,action)
          Debe regresar 0.0 si nunca hemos visto ese estado
          o el valor del nodo Q de otra forma
        """
        "*** YOUR CODE HERE ***"
        return self.qValues[(state,action)]


    def computeValueFromQValues(self, state):
        """
          Regresa max_action Q(state,action)
          donde el max es sobre las acciones legales
          Notese que si no hay acciones legales, como 
          en el estado terminal, debes regresar 0.0
        """
        "*** YOUR CODE HERE ***"
        values = []
        legales = self.getLegalActions(state)
        if len(legales) < 1:
            return 0.0
        for accion in self.getLegalActions(state):
            values.append(self.qValues[(state,accion)])
        return max(values.values())


    def computeActionFromQValues(self, state):
        """
          Computa la mejor accion para tomar en cada estado
          Note que si no hay acciones legales, como en el estado terminal,
          debe regresarse None
        """
        "*** YOUR CODE HERE ***"
        values = util.Counter()
        legales = self.getLegalActions(state)
        if legales == ():
            return None
        for accion in self.getLegalActions(state):
            values[accion] = self.qValues[(state,accion)]

        return values.argMax()


    def getAction(self, state):
        """
          Computa la accion a tomar en el estado actual. Con 
          probabilidad self.epsilon, debemos tomar una accion aleatoria
          y tomar la mejor politica en otro caso
          Notese que si no hay valores legales, debe regresarse None

          PISTA: Puede que quieras usar util.flipCoin(prob)
          HINT: Para seleccionar de forma random en una lista, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** TU CODIGO AQUI ***"
        if util.flipCoin(self.epsilon):
            action = random.choice(legalActions)
        else:
            action = self.computeActionFromQValues(state)

        return action

    def update(self, state, action, nextState, reward):
        """
          La clase padre llama a esto para observar una transicion
          state = action => nextState y recompensa (reward).
          Deberias hacer tu actualizacion Q aqui. 

          NOTE: Nunca llames a esta funcion
          El sistema lo hara por ti
        """
        "*** TU CODIGO AQUI***"
        sample = reward + self.discount * self.computeValueFromQValues(nextState)
        self.qValues[(state,action)] = (1 - self.alpha) * self.qValues[(state,action)] + self.alpha*sample
        return

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactamente igual que QLearningAgent, pero con parametros default diferentes"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        Estos parametros por defecto pueden cambiarse desde la linea de comandos
        Por ejemplo, para cambiar el factor de exploracion, intente:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - factor de aprendizaje
        epsilon  - factor de exploracion
        gamma    - factor de descuento
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simplemente llama al metodo getAction ya implementado y luego informa al padre
        la accion para pacman, no cambie o quite este metodo
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass