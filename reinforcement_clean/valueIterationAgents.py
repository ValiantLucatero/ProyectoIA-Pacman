# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        Un ValueIterationAgent toma un proceso de decision de Markov
        (ver mdp.py) en la inicializacion y corre iteracion de valores
        para un numero dado de iteraciones usando un factor de descuento
        dado
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Agente de iteracion de valores. Debe tomar un mdp
          en construccion, ejecutar un numero indicado de iteraciones
          y actuar acorde con la politica restante

          Algunos metodos utiles que vas a usar
              mdp.getStates()                Estados
              mdp.getPossibleActions(state)  Acciones
              mdp.getTransitionStatesAndProbs(state, action)  Funcion de transicion
              mdp.getReward(state, action, nextState)    Funcion de recompensas
              mdp.isTerminal(state)     Funcion de terminales
        """
        self.mdp = mdp                #MDP
        self.gamma = discount         #Factor de descuento gamma
        self.iterations = iterations  #Numero de veces que se iterara para sacar los valores
        self.values = util.Counter()  #Un contador es un diccionario que siempre inicializa en 0
        #Voy a almacenar los valores Q de cada estado
        #Las llaves van a ser los estados
        #Voy a hacer self.iterations iteraciones
        for i in range(self.iterations):
            #Vector auxiliar para guardar los valores V de esta iteracion
            valores_kmas1 = util.Counter()
            #Por cada estado
            for estado in mdp.getStates():
                #Si el estado es un estado terminal, lo ignoro
                if mdp.isTerminal(estado): continue
                    #Voy a obtener el valor a partir de los valores Q
            valor = -(float('inf'))
            #Iterando sobre todas las acciones posibles desde ese estado
            for accion in mdp.getPossibleActions(estado):
                #Con cada accion calculo Q(estado,accion) y actualizo valor
                valor = max(valor,self.computeQValueFromValues(estado,accion))
                #Ya con el valor, lo guardo en mi vector auxiliar
            valores_kmas1[estado] = valor
        #Ya que obtuve todos los valores para esta Iteracion, actualizo self.values
        for estado in valores_kmas1:
            self.values[estado] = valores_kmas1[estado]

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Computa el valor-Q de una accion en el estado
          desde la funcion de valores en self.values
        """
        "*** Tu codigo aqui ***"
        valorQ = 0.0
        for estadoSig,T in self.mdp.getTransitionStatesAndProbs(state,action):
            recompensa = self.mdp.getReward(state,action,estadoSig)
            vSig = self.getValue(estadoSig)
            valorQ += T*(recompensa + self.gamma*vSig)
        return valorQ

    def computeActionFromValues(self, state):
        """
          Funcion que realiza EXTRACCION DE POLITICAS

          La politica es la mejor accion en el estado dado
          de acuerdo a los valores actualmente guardados en self.values.

          Puedes romper los empates en el modo que quieras
          Nota que si no hay mas acciones legales, como en el
          estado terminal, debes regresar None.
        """
        "*** Tu codigo aqui ***"
        if self.mdp.isTerminal(state):
            return None
        self.valoresQ = util.Counter()
        for accion in self.mdp.getPossibleActions(state):
            self.valoresQ[(state,accion)] = self.computeQValueFromValues(state,accion)
        mejorEstado,mejorAccion = self.valoresQ.argMax()
        return mejorAccion

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Regresa la politica en ese estado."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
