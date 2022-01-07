from .farthest import Farthest_Shepherd
from .switching import Switching_Shepherd

''' Select shepherd method'''
def select_shepherd_model(name, init_param):
    if name == "switching":
        return Switching_Shepherd(init_param)
    elif name == "farthest":
        return Farthest_Shepherd(init_param)
    else:
        raise Exception('Invalid shepherd model selected')
