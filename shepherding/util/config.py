import json
import os
import re

def load(json_path, complement=True):
    '''
    Read json, and then return dict
    '''
    json_dict = None
    try:
        with open(json_path, 'r') as f:
            json_dict = json.load(f)   
    except Exception:
        pass
    
    try:
        if complement == True:
            json_dict = complement_dict(json_dict)
    except Exception:
        pass
    
    return json_dict

def complement_dict(json_dict):
    '''
    Unenough configs are replaced by default.json
    '''
    with open("./config/default.json", 'r') as f:
        default_dict = json.load(f)

    for k in default_dict.keys():
        if k not in json_dict:
            json_dict[k] = default_dict[k]

    return json_dict

def write(json_path, dict):
    '''
    Ouput in dict format
    '''
    with open(json_path, 'w') as f:
        json.dump(dict, f)
    
def write_reshaped(json_path, dict):
    '''
    Ouput in reshaped dict format    
    '''
    with open(json_path, 'w') as f:
        dump_data = json.dumps(dict, indent=4)
        re_dump_data = re.sub('\[(.*?)\]',dashrepl, dump_data, flags=re.DOTALL)
        f.write(re_dump_data)

def dashrepl(matchobj):
    #print(matchobj)
    return matchobj.group(0).replace("\n", "").replace(" ", "")

def diff_from_defalut(self, defalut_params, params):
    '''
    Pick diffent from defalut.json
    '''
    diff_list = []
    for k in params.keys():
        if defalut_params[k] != params[k]:
            diff_list.append("{}:{}".format(k, params[k]))
    return diff_list