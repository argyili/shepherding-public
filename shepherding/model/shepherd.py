import math
import random
import numpy as np
import random

# Proposal shepherding model
class Shepherd:
    def __init__(self, param, i):
        self.R = 60
        self.p1 = param["shepherd_param"][0]
        self.p2 = param["shepherd_param"][1]
        self.p3 = param["shepherd_param"][2]
        self.p4 = param["shepherd_param"][3]
        self.goal = param['goal']
        self.goal_radius = param['goal_radius']
        self.limit = 3

        self.reset(param, i, 0)

    def reset(self, param, i, trial):
        self.sheeps = []
        self.target_sheep = None
        # Target position from target sheep
        self.target_position = np.array([0, 0])
        self.min_dis_from_sheep = 0
        self.max_dis_from_sheep = 0
        # Movement distance in one time
        self.step_distance = 0

        # Set initial positions
        random.seed(i + trial)
        base_position = np.array(param['shepherd_initial_pos_base'])

        # Generated with a hollow ring
        r = 0
        if 'shepherd_initial_pos_vacuum' in param:
            r = math.sqrt(random.uniform((param['shepherd_initial_pos_vacuum'] ** 2), param['shepherd_initial_pos_radius'] ** 2))
        else:
            r = math.sqrt(random.uniform(0, param['shepherd_initial_pos_radius'] ** 2))
        
        theta = random.uniform(-math.pi, math.pi)

        # Partly surrounded with a direction
        if 'shepherd_initial_direction' in param:
            # From bottom
            if param['shepherd_initial_direction'] == 'top_right':
                if theta < -0.25*math.pi or  theta > 0.75*math.pi:
                    theta -= math.pi

            # From top
            if param['shepherd_initial_direction'] == 'bottom_left':
                if theta > -0.25*math.pi and theta < 0.75*math.pi:
                    theta -= math.pi
                
        self.position = base_position + np.array([r * math.cos(theta), r * math.sin(theta)])
        self.velocity = np.array([0, 0])
        self.is_success = False

    ''' Attraction received from target position '''
    def attractive(self):
        u = self.target_position - self.position
        if np.linalg.norm(u) > 0:
            u = u / np.linalg.norm(u)
        return  u

    ''' Repulsion from all sheep in average '''
    def repulsive_from_allsheep(self, sheeps):
        if len(sheeps) == 0:
            return np.array([0,0])
        u = np.array([0,0])
        u1 = np.array([0,0])
        for sheep in sheeps:
            u = sheep.position - self.position
            if np.linalg.norm(u) > self.limit:
                u1 = u1 + (u / np.power(np.linalg.norm(u), 3) )
            else:
                unit_u1 = u / np.linalg.norm(u)
                u1 = u1 + ((unit_u1 * self.limit) / np.power(np.linalg.norm(unit_u1 * self.limit), 3) )           

        # return  - u1 / math.sqrt(len(sheeps))
        return  - u1 / len(sheeps)

    def repulsive_from_goal(self):
        u = self.goal - self.position 
        if np.linalg.norm(u) > 0:
            u = u / np.linalg.norm(u)
        return - u

    ''' Repulsion from other shepherd in average '''
    def repulsive_from_othershepherds(self, shepherds):
        if len(shepherds) == 0:
            return np.array([0,0])
        u = np.array([0,0])
        u1 = np.array([0,0])
        for shepherd in shepherds:
            u = shepherd.position - self.position
            if np.linalg.norm(u) > self.limit:
                u1 = u1 + (u / np.power(np.linalg.norm(u), 3) )
            else:
                unit_u1 = u / np.linalg.norm(u)
                u1 = u1 + ((unit_u1 * self.limit) / np.power(np.linalg.norm(unit_u1 * self.limit), 3) )
            # if np.linalg.norm(u) > 1:
            #     u1 = u1 + (u / np.power(np.linalg.norm(u), 3) )
            # else:
            #     u1 = u1 + u
        dis_goal = np.linalg.norm(self.goal - self.position)
        return - u1 / len(shepherds) * dis_goal
        # return - u1 / len(shepherds)

    def get_minandmax_dis_from_sheep(self):
        min_dis = np.linalg.norm(self.sheeps[0].position - self.position)
        max_dis = 0
        for i in range(len(self.sheeps)):
            d =  np.linalg.norm(self.sheeps[i].position - self.position)
            if d < min_dis:
                min_dis = d
            if d > max_dis:
                max_dis = d
        self.min_dis_from_sheep = min_dis
        self.max_dis_from_sheep = max_dis

    ''' Find other agents (sheep or shepherds) whose distance is closer than threshold '''
    def agents_in_region(self, agents):
        in_agents = []
        for other in agents:
            d = np.linalg.norm(other.position - self.position)
            if d < self.R and d != 0:
                in_agents.append(other)
        return in_agents

    ''' Update one shepherd '''
    def update(self, sheeps, shepherds):
        if len(sheeps) == 0:
            return

        self.sheeps = sheeps
        self.judge_success()
        if self.is_success:
            return
        self.shepherds = shepherds
        self.get_minandmax_dis_from_sheep()
        near_sheep = self.agents_in_region(sheeps)
        near_shepherds = self.agents_in_region(shepherds)

        v1 = self.p1 * self.attractive()
        v2 = self.p2 * self.repulsive_from_allsheep(near_sheep)
        v3 = self.p3 * self.repulsive_from_goal()
        v4 = self.p4 * self.repulsive_from_othershepherds(near_shepherds)
        v = v1 + v2 + v3 + v4

        self.velocity = v 
        self.step_distance = np.linalg.norm(v)
        self.position = self.position + v

    def judge_success(self):
        success = True
        for i in range(len(self.sheeps)):
            u = self.sheeps[i].position - self.goal
            d = np.linalg.norm(u)
            if d > self.goal_radius:
                success = False
        self.is_success = success