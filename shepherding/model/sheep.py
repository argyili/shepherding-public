import math
import random
import numpy as np

class Sheep:
    def __init__(self, param, i):
        # Initialize
        self.R = 20
        self.no = i
        self.p1 = param["sheep_param"][0]
        self.p2 = param["sheep_param"][1]
        self.p3 = param["sheep_param"][2]
        self.p4 = param["sheep_param"][3]
        self.position = np.array([0, 0])
        self.velocity = np.array([0, 0])
        # if distance is smaller than limit, see it as limit for stability
        self.limit = 3
        self.reset(param, i,  0)
    
    ''' Reset only when initializing '''
    def reset(self, param, i, trial):
        # trail is only useful of setting seed for random
        random.seed(i + trial)
        base_position = np.array(param["sheep_initial_pos_base"])
        r = math.sqrt(random.uniform(0, param["sheep_initial_pos_radius"] ** 2))
        theta = random.uniform(-math.pi, math.pi)
        self.position = base_position + np.array([r * math.cos(theta), r * math.sin(theta)])
        self.velocity = np.array([0, 0])

    ''' Repulsion from other sheep '''
    def separation(self, sheeps):
        if len(sheeps) == 0:
            return np.array([0,0])
        u = np.array([0,0])
        u1 = np.array([0,0])
        for other in sheeps:
            u = other.position - self.position
            if np.linalg.norm(u) > self.limit:
                u1 = u1 + (u / np.power(np.linalg.norm(u), 3) )
            else:
                unit_u1 = u / np.linalg.norm(u)
                u1 = u1 + ((unit_u1 * self.limit) / np.power(np.linalg.norm(unit_u1 * self.limit), 3) )
        
        return  - u1 / len(sheeps)

    ''' Alignment with other sheep velocity ''' 
    def alignment(self, sheeps):
        if len(sheeps) == 0:
            return np.array([0,0])
        u = np.array([0,0])
        u1 = np.array([0,0])
        for other in sheeps:
            u = other.velocity
            if np.linalg.norm(u) > 0:
                u1 = u1 + (u / np.linalg.norm(u))
        return - u1 / len(sheeps)

    ''' Cohesion from other sheep '''
    def cohesion(self, sheeps):
        if len(sheeps) == 0:
            return np.array([0,0])
        u = np.array([0,0])
        u1 = np.array([0,0])
        for other in sheeps:
            u = other.position - self.position
            if np.linalg.norm(u) > 0:
                u1 = u1 + (u / np.linalg.norm(u))

        return u1 / len(sheeps)

    ''' Repulsion from other shepherds, aggregation '''
    def repulsion_from_shepherds(self, shepherds):
        if len(shepherds) == 0:
            return np.array([0,0])

        u1 = np.array([0,0])
        for i in range(len(shepherds)):        
            u = shepherds[i].position - self.position
            if np.linalg.norm(u) > self.limit:
                u1 = u1 + (u / np.power(np.linalg.norm(u), 3) )
            else:
                unit_u1 = u / np.linalg.norm(u)
                u1 = u1 + ((unit_u1 * self.limit) / np.power(np.linalg.norm(unit_u1 * self.limit), 3) )

        # If average
        return - u1 /len(shepherds)
        # If sum
        # return - u1
        # return - u1 / math.sqrt(len(shepherds))
    
    ''' Find other agents (sheep or shepherds) whose distance is closer than threshold '''
    def agents_in_region(self, agents):
        in_agents = []
        for other in agents:
            d = np.linalg.norm(other.position - self.position)
            if d < self.R and d != 0:
                in_agents.append(other)
        return in_agents

    ''' Update by considering all forces '''
    def update(self, sheeps, shepherds):

        near_sheeps = self.agents_in_region(sheeps)
        near_shepherds = self.agents_in_region(shepherds)

        v1 = self.p1 * self.separation(near_sheeps)
        v2 = self.p2 * self.alignment(near_sheeps)
        v3 = self.p3 * self.cohesion(near_sheeps)
        v4 = self.p4 * self.repulsion_from_shepherds(near_shepherds)
        v = v1 + v2 + v3 + v4
        
        self.velocity = v 
        self.position = self.position + v 