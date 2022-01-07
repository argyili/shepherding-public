import math
import random
import numpy as np
import random
import sys

# Proposal shepherding model
class Switching_Shepherd:
    def __init__(self, param):
        self.NAME = 'switching'
        self.sheeps = []
        self.shepherds = []
        self.goal = param['goal']

        self.STRATEGIES = ['drive', 'collect']
        self.strategy = ''
        self.farthest_sheep = None
        self.flock_center = np.array([0, 0])
        self.flock_size = 0
        self.threshold = param['switching_threshold']
        self.interval = param['switching_interval']
        self.R = 60

    ''' Update basic information every time before updating target '''
    def update(self, sheeps, shepherds):
        self.sheeps = sheeps
        self.shepherds = shepherds
        self.update_target_sheep()

    def get_flock_center(self, shepherd):
        self.flock_center = np.array([0, 0])
        for i in range(len(self.sheeps)):
            # Limit detect distance
            d_shepherd = np.linalg.norm(self.sheeps[i].position - shepherd.position)
            if d_shepherd > self.R: continue
            self.flock_center = np.add(self.flock_center, self.sheeps[i].position)
        self.flock_center = np.divide(self.flock_center, len(self.sheeps))
    
    def judge_flock_size(self, shepherd):
        size = 0
        for i in range(len(self.sheeps)):
            # Limit detect distance
            d_shepherd = np.linalg.norm(self.sheeps[i].position - shepherd.position)
            if d_shepherd > self.R: continue
            dis = np.linalg.norm(self.sheeps[i].position - self.flock_center)
            if dis > size:
                size = dis
                self.farthest_sheep = self.sheeps[i]
        self.flock_size = size

    def get_target_position(self, shepherd):
        dis = 0
        if self.flock_size == 0:
            return

        if self.flock_size < self.threshold:
            # Drive
            self.strategy = self.STRATEGIES[0]
            dis = self.flock_center - self.goal
            shepherd.target_sheep = None
            shepherd.target_position = self.flock_center + self.interval * dis / np.linalg.norm(dis)
        else:
            # Collect
            self.strategy = self.STRATEGIES[1]
            dis = self.farthest_sheep.position - self.flock_center
            # No exact target sheep while collecting
            shepherd.target_sheep = self.farthest_sheep
            shepherd.target_position = self.farthest_sheep.position + self.interval * dis / np.linalg.norm(dis)

    ''' Selecting method is varied in each shepherding model '''
    def update_target_sheep(self):
        for i in range(len(self.shepherds)):
            shepherd = self.shepherds[i]
            self.get_flock_center(shepherd)
            self.judge_flock_size(shepherd)
            self.get_target_position(shepherd)



