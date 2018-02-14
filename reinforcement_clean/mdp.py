# mdp.py
# ------
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


import random

class MarkovDecisionProcess:

    def getStates(self):
        """
        Regresa una lista de todos los estados en el MDP
        No es posible para MDPs muy largos
        """
        abstract

    def getStartState(self):
        """
        Regresa el estado inicial del MDP
        """
        abstract

    def getPossibleActions(self, state):
        """
        Regresa la lista de acciones posibles del MDP
        """
        abstract

    def getTransitionStatesAndProbs(self, state, action):
        """
        Regresa una lista de pares (siguiente,prob)
        representando los estados alcanzables desde "state"
        si tomo "action" junto con sus probabilidades

        Note that in Q-Learning and reinforcment
        learning in general, we do not know these
        probabilities nor do we directly model them.
        """
        abstract

    def getReward(self, state, action, nextState):
        """
        Obten la recompensa de la transicion con
        ese estado, accion, y siguiente

        Not available in reinforcement learning.
        """
        abstract

    def isTerminal(self, state):
        """
        Returns true if the current state is a terminal state.  By convention,
        a terminal state has zero future rewards.  Sometimes the terminal state(s)
        may have no possible actions.  It is also common to think of the terminal
        state as having a self-loop action 'pass' with zero reward; the formulations
        are equivalent.
        """
        abstract
