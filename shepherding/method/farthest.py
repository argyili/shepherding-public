import math
import random
import numpy as np
import random
import sys

# Proposal shepherding model
class Farthest_Shepherd:
    def __init__(self, param):
        self.NAME = 'farthest'
        self.sheeps = []
        self.shepherds = []
        self.goal = param['goal']
        
        self.R = 60
        self.K_OFFSET = 2

    ''' Update basic information every time before updating target '''
    def update(self, sheeps, shepherds):
        self.sheeps = sheeps
        self.shepherds = shepherds
        self.update_target_sheep()

    ''' Selecting method is varied in each shepherding model '''
    def update_target_sheep(self):
        for i in range(len(self.shepherds)):
            shepherd = self.shepherds[i]
            max = -sys.maxsize
            target_sheep = -1
            for j in range(len(self.sheeps)):
                # Limit detect distance
                d_shepherd = np.linalg.norm(self.sheeps[j].position - shepherd.position)
                # if d_shepherd > self.R: continue
                d_goal =  np.linalg.norm(self.sheeps[j].position - self.goal)
                if d_goal > max:
                    max = d_goal
                    target_sheep = j
            
            shepherd.target_sheep = self.sheeps[target_sheep]
            self.update_target_position(shepherd)

    def update_target_position(self, shepherd):
        position = shepherd.target_sheep.position
        if shepherd.target_sheep:
            shepherd.target_position = position + (position - shepherd.goal) / np.linalg.norm(position - shepherd.goal) * self.K_OFFSET