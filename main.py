import os
import time
import datetime
import argparse 
import csv
from multiprocessing import Pool
from itertools import starmap

import shepherding as ss
from shepherding.util import analyze 
from shepherding.util import config
from shepherding.util import disk_info
    
''' Multiprocessing for running batch programs '''
def multiprocess(param, directory_path, is_gif):
    shepherds = range(param["shepherd_number"][0], param["shepherd_number"][1] + 1)
    sheeps = range(param["sheep_number"][0], param["sheep_number"][1] + 1)
    trials = range(param["trial_number"])

    ssTrail = ss.trial.Trial(param, directory_path) 
    values = [(sheep_num, shepherd_num, trial) for sheep_num in sheeps for shepherd_num in shepherds for trial in trials]
    
    start = time.time()
    with Pool(processes=param["process_number"]) as pool:
        pool.starmap(ssTrail.trial_loop_csv, values)
        [analyze.full_csv(directory_path, shepherd_num, sheep_num, trials) for shepherd_num in shepherds for sheep_num in sheeps]
    elapsed_time = time.time() - start

    # Generate kinds of graphs for analysis
    # Default from 0 or 1, suitable to shepherds, sheeps and trials
    gen_graph(directory_path, shepherds, sheeps, trials, param, is_gif)
    elapsed_time_graph = time.time() - elapsed_time

    return elapsed_time, elapsed_time_graph

''' Generate graph for visualizing after results '''
def gen_graph(directory_path, shepherd_nums, sheep_nums, trial_nums, param, is_gif=False):
    analyze.write_csv(directory_path, directory_path+"/result.csv", shepherd_nums)
    # Draw bar plot for multiple graphs by each evaluation index
    analyze.plot_graph(directory_path, shepherd_nums, sheep_nums)
    # Trace for each process
    
    if is_gif:
        analyze.first_graph_plot(directory_path, shepherd_nums[-1], sheep_nums[-1], trial_nums, param)
        analyze.csv_trace(directory_path, shepherd_nums[-1], sheep_nums[-1], trial_nums, param)
    else:
        analyze.first_graph_plot(directory_path, shepherd_nums[-1], sheep_nums[-1], trial_nums, param)
        # analyze.csv_key_trace(directory_path, shepherd_nums, sheep_nums, trial_nums, param)

def make_dir(param):
    '''
    Make directory by current time

    Format: yyyy_MMdd_HHMMSS
    ''' 
    now = datetime.datetime.now()
    now_string = now.strftime('%Y-%m%d-%H%M%S_' + param["shepherd_model"])  # yyyy_MMdd_HHMMSS形式
    directory_path = "log/{}".format(now_string)
    graph_path = "log/{}/graph".format(now_string)
    data_path = "log/{}/data".format(now_string)
    gif_path = "log/{}/gif".format(now_string)
    png_path = "log/{}/png".format(now_string)

    os.makedirs(graph_path) 
    os.makedirs(data_path)
    os.makedirs(gif_path)
    os.makedirs(png_path)
    return os.path.abspath(directory_path)

def get_param(param_file_path):
    '''
    Get parameter from json file
    '''
    param = config.load(param_file_path)
    return param

def arg_parse():
    '''
    Parse argument
    '''
    parser = argparse.ArgumentParser(description="Multiple Shepherding Program")
    parser.add_argument('-p', '--param_file_path', default="./config/default.json", help='parameter file path')
    parser.add_argument('-g', '--gif', action='store_true', help='generate gif and trace graph')
    return parser.parse_args()

if __name__ == '__main__':
    args = arg_parse()
    param = get_param(args.param_file_path)

    dir_path = make_dir(param)

    multiprocess(param, dir_path, args.gif)
    
    # Copy parameter again
    config.write_reshaped(dir_path + "/setting.json", param)

    # Disk info warning if necessary
    disk_info.warn_directory_size(dir_path)
    disk_info.warn_disk_usage(limit_percentage=80)