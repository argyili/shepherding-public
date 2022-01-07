from itertools import count
import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import imageio
import math
from .plot_ss import * 

def count_line(file_path):
    with open(file_path) as f:
        for line_count, _ in enumerate(f, 1):
            pass
    return line_count

def read_file(path):
    list = []
    with open(path, mode='r') as f:
        reader = csv.reader(f)
        # Start from line 1, line 1 not existed
        for row in reader:
            list.append(row)
    f.close()
    return list

def read_line(path, idx):
    with open(path, mode='r') as f:
        reader = csv.reader(f)
        # Start from line 1, line 1 not existed
        line_count = 1
        while True:
            if line_count == idx:
                break
            f.readline()
            line_count += 1
        return next(reader)

''' Return last line number and its content '''
def read_last_line(file_path):
    line_count = count_line(file_path)
    return read_line(file_path, line_count)

''' Turn string to colored np.array '''
def str_to_color_nparray(str):
    color = str[0]
    np_str = str[3:-1].split()
    # print("str:{} re:{}".format(str, str[1:-1]))
    l = [float(np_str[i]) for i in range(len(np_str))]
    return  color, np.array(l)

''' Bar plot with array and corresponding nums '''    
def bar_plot(array, nums):
    fig, ax = plt.subplots()
    ax.bar(nums, array)
    # ax.ste_xticks(nums)
    return fig, ax 

''' Get a calculated or integrated list for one exact shepherd agent number shepherding with all combination of sheep agent numbers, averaged by multiple trails '''
def get_full_list(directory_path, shepherd_nums):
    list = []
    # Shepherd number starts from 1
    for i in shepherd_nums:
        file_path = directory_path + "/data/" + str(i) + ".csv"
        list.append(read_file(file_path))
    return list

def cal_success(list):
    length = len(list)
    succ_length = length
    succ_list = []
    for line in list:
        if line[3] == 'False':
            succ_length -= 1
        else:
            succ_list.append(line)
    succ_rate = succ_length / length
    return succ_rate, succ_list

''' 
Integrate trials with same configuration for shepherd number and sheep number
Calculate average time and distance in succeeded trial, appending success rate
'''
def integrate_trial(list):
    res = [None] * 8;
    res[0] = list[0][0];
    res[1] = list[0][1];
    res[2] = list[0][2];
    succ_rate, succ_list = cal_success(list)
    # Change to success rate instead of success boolean flag
    res[3] = succ_rate
    if len(succ_list) > 0:
        # step index
        res[4] = sum(int(line[-2]) for line in succ_list) / len(succ_list)
        var_line = []
        for line in succ_list:
            var_line.append(int(line[-2]))
        res[5] = np.var(var_line)
        # distance index
        res[6] = sum(int(line[-1]) for line in succ_list) / len(succ_list)
        var_line = []
        for line in succ_list:
            var_line.append(int(line[-1]))
        res[7] = np.var(var_line)
    else:
        res[4] = 0
        res[5] = 0
        res[6] = 0
        res[7] = 0
    
    res[4] = str(math.ceil(res[4]))
    res[5] = str(math.ceil(res[5]))
    res[6] = str(math.ceil(res[6]))
    res[7] = str(math.ceil(res[7]))
    return res

''' Summarize each trial information from the last step at each csv file, repeat for trial number '''
def full_csv(directory_path, shepherd_num, sheep_num, trials):
    with open("{}/data/{}.csv".format(directory_path, shepherd_num), mode='a') as f:
        list=[]
        for trial in trials:
            file_path = "{}/data/{}sh{}tr{}.csv".format(directory_path, shepherd_num, sheep_num, trial)
            line = read_last_line(file_path)
            list.append(line)
        int_list = integrate_trial(list)
        writer = csv.writer(f)
        writer.writerow(int_list)

# Draw graphs below

''' Output all result data into one result.csv  '''
def write_csv(directory_path, file_path, shepherd_nums):
    with open(file_path, mode='a') as f:
        list=[]
        # Add csv head
        list.append(['shepherd', 'sheep', 'method', 'rate', 'step', 'var_step', 'distance', 'var_dis'])
        for shepherd_num in shepherd_nums:
            file_path = "{}/data/{}.csv".format(directory_path, shepherd_num)
            line = read_last_line(file_path)
            list.append(line)
        writer = csv.writer(f)
        writer.writerows(list)

''' Draw average movement distance for shepherds in trials '''
def success_rate_plot(directory_path, shepherd_nums, sheep_nums, full_list):
    graph_path = directory_path + '/graph/rate'
    os.makedirs(graph_path)
    base = shepherd_nums[0]
    for i in shepherd_nums:
        list = full_list[i - base]
        arr = np.reshape(np.take(np.asarray(list), [3], axis=1), -1).astype(np.float).tolist()
        df = pd.DataFrame({"sheep number": sheep_nums, "success rate": arr})
        ax = sns.barplot(x="sheep number", y="success rate", palette="Blues_r", data=df)
        ax.set_title('average success rate when shepherd number is ' + str(i))  
        fig_path_sh = "{}/shd{}.png".format(graph_path, str(i))
        plt.savefig(fig_path_sh)
        ax.clear()

    base = sheep_nums[0]
    for i in sheep_nums:
        list = []
        for j in range(len(full_list)):
            list.append(full_list[j][i - base])
        arr = np.reshape(np.take(np.asarray(list), [3], axis=1), -1).astype(np.float).tolist()
        df = pd.DataFrame({"shepherd number": shepherd_nums, "success rate": arr})
        ax = sns.barplot(x="shepherd number", y="success rate", palette="Blues_r", data=df)
        ax.set_title('average success rate when sheep number is ' + str(i))
        fig_path_sh = "{}/shp{}.png".format(graph_path, str(i))
        plt.savefig(fig_path_sh)
        ax.clear()
    return

''' Draw success time for shepherds in trials '''
def success_time_plot(directory_path, shepherd_nums, sheep_nums, full_list):
    graph_path = directory_path + '/graph/succ'
    os.makedirs(graph_path)
    base = shepherd_nums[0]
    for i in shepherd_nums:
        list = full_list[i - base]
        arr = np.reshape(np.take(np.asarray(list), [-2], axis=1), -1).astype(np.float).tolist()
        df = pd.DataFrame({"sheep number": sheep_nums, "success steps": arr})
        ax = sns.barplot(x="sheep number", y="success steps", palette="Blues_r", data=df)
        ax.set_title('success steps for sheep when shepherd number is ' + str(i))
        fig_path_sh = "{}/shd{}.png".format(graph_path, str(i))
        plt.savefig(fig_path_sh)
        ax.clear()

    base = sheep_nums[0]
    for i in sheep_nums:
        list = []
        for j in range(len(full_list)):
            list.append(full_list[j][i - base])
        arr = np.reshape(np.take(np.asarray(list), [-2], axis=1), -1).astype(np.float).tolist()
        df = pd.DataFrame({"shepherd number": shepherd_nums, "success steps": arr})
        ax = sns.barplot(x="shepherd number", y="success steps", palette="Blues_r", data=df)
        ax.set_title('success steps for shepherd when sheep number is ' + str(i))
        fig_path_sh = "{}/shp{}.png".format(graph_path, str(i))
        plt.savefig(fig_path_sh)
        ax.clear()
    return

''' Draw average movement distance for shepherds in trials '''
def average_distance_plot(directory_path, shepherd_nums, sheep_nums, full_list):
    graph_path = directory_path + '/graph/dis'
    os.makedirs(graph_path)
    base = shepherd_nums[0]
    for i in shepherd_nums:
        list = full_list[i - base]
        arr = np.reshape(np.take(np.asarray(list), [-1], axis=1), -1).astype(np.float).tolist()
        df = pd.DataFrame({"sheep number": sheep_nums, "average distance": arr})
        ax = sns.barplot(x="sheep number", y="average distance", palette="Blues_r", data=df)
        ax.set_title('average shepherding distance for sheep when shepherd number is ' + str(i))  
        fig_path_sh = "{}/shd{}.png".format(graph_path, str(i))
        plt.savefig(fig_path_sh)
        ax.clear()

    base = sheep_nums[0]
    for i in sheep_nums:
        list = []
        for j in range(len(full_list)):
            list.append(full_list[j][i - base])
        arr = np.reshape(np.take(np.asarray(list), [-1], axis=1), -1).astype(np.float).tolist()
        df = pd.DataFrame({"shepherd number": shepherd_nums, "average distance": arr})
        ax = sns.barplot(x="shepherd number", y="average distance", palette="Blues_r", data=df)
        ax.set_title('average shepherding distance for shepherd when sheep number is ' + str(i))
        fig_path_sh = "{}/shp{}.png".format(graph_path, str(i))
        plt.savefig(fig_path_sh)
        ax.clear()
    return

''' Composite plot only for shepherds '''
def composite_plot(directory_path, shepherd_nums, sheep_nums, full_list):
    graph_path = directory_path + '/graph/compo'
    os.makedirs(graph_path)
    base = shepherd_nums[0]

    base = sheep_nums[0]
    for i in sheep_nums:
        f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(24, 8), sharex=True)
        list = []
        for j in range(len(full_list)):
            list.append(full_list[j][i - base])
        arr = np.reshape(np.take(np.asarray(list), [3], axis=1), -1).astype(np.float).tolist()
        df = pd.DataFrame({"success rate": arr})
        sns.lineplot(data=df, ax=ax1)
        
        list = []
        for j in range(len(full_list)):
            list.append(full_list[j][i - base])
        arr = np.reshape(np.take(np.asarray(list), [-2], axis=1), -1).astype(np.float).tolist()
        df = pd.DataFrame({"success steps": arr})
        sns.lineplot(data=df, ax=ax2)

        list = []
        for j in range(len(full_list)):
            list.append(full_list[j][i - base])
        arr = np.reshape(np.take(np.asarray(list), [-1], axis=1), -1).astype(np.float).tolist()
        df = pd.DataFrame({"average distance": arr})
        sns.lineplot(data=df, ax=ax3)

        plt.suptitle('sheep number is ' + str(i))
        fig_path_sh = "{}/shp{}.png".format(graph_path, str(i))
        plt.savefig(fig_path_sh)
        ax1.clear()
        ax2.clear()
        ax3.clear()
    return

''' Plot all graphs here '''
def plot_graph(directory_path, shepherd_nums, sheep_nums):
    sns.set(style="white")
    full_list = get_full_list(directory_path, shepherd_nums)
    print(full_list)
    success_rate_plot(directory_path, shepherd_nums, sheep_nums, full_list)
    success_time_plot(directory_path, shepherd_nums, sheep_nums, full_list)
    average_distance_plot(directory_path, shepherd_nums, sheep_nums, full_list)
    composite_plot(directory_path, shepherd_nums, sheep_nums, full_list)

def generate_gif_csv(png_path, gif_file_path, frame):
    ''' Generate gif by existed graphs '''
    frames_path = png_path + "/{i}.png"
    with imageio.get_writer(gif_file_path, mode='I', fps=10) as writer:
        for i in range(frame):
            writer.append_data(imageio.imread(frames_path.format(i=i)))

# def csv_trace(directory_path, shepherd_nums, sheep_nums, trial_nums, param):
#     csv_one_trace(directory_path, shepherd_nums[-1], sheep_nums[-1], trial_nums, param)

''' Draw one trace gif through graphs by trace '''
''' shepherd number, sheep number and trial number are all above 0 '''
def first_graph_plot(directory_path, shepherd_num, sheep_num, trial_nums, param):
    sns.set(style="white")
    min_line = 10000 
    trial_num = trial_nums[0]
    for i in trial_nums:
        file_path = directory_path + "/data/" + "{}sh{}tr{}.csv".format(str(shepherd_num), str(sheep_num), str(i))
        cnt = count_line(file_path)
        # if cnt > max_line:
        #     max_line = cnt
        #     trial_num = i
        if cnt < min_line:
            min_line = cnt
            trial_num = i
    print(trial_num)
    file_path = directory_path + "/data/" + "{}sh{}tr{}.csv".format(str(shepherd_num), str(sheep_num), str(trial_num))
    with open(file_path) as f:
        reader = csv.reader(f, delimiter=',')
        # For trace
        sheeps_color = []
        sheeps_pos = []
        shepherds_color = []
        shepherds_pos = []
        index = 0
        # row_num = 0
        log_png_path = directory_path + "/png/{}sh{}tr{}".format(str(shepherd_num), str(sheep_num), str(trial_num))
        os.makedirs(log_png_path)
        for row in reader:
            # For trace
            sheeps_color_row = []
            sheeps_pos_row = []
            shepherds_color_row = []
            shepherds_pos_row = []
            for i in range(0, sheep_num):
                color, pos = str_to_color_nparray(row[i])
                sheeps_color.append(color)
                sheeps_pos.append(pos)
                sheeps_color_row.append(color)
                sheeps_pos_row.append(pos)
            for i in range(sheep_num, sheep_num + shepherd_num):   
                color, pos = str_to_color_nparray(row[i])
                shepherds_color.append(color)
                shepherds_pos.append(pos)
                shepherds_color_row.append(color)
                shepherds_pos_row.append(pos)

            fig_row, ax_row = plt.subplots(figsize=(8,8))
            init_plot_line_csv_spec(ax_row, param, sheeps_color_row, sheeps_pos_row, shepherds_color_row, shepherds_pos_row)
            fig_path = log_png_path + "/{}_0.pdf".format(str(index))
            # print(fig_path)
            fig_row.savefig(fig_path)
            index += 1
            ax_row.clear()
            plt.clf()
            plt.close()
            break
    f.close()
    return

""" Generate a gif for shortest trace """
def csv_trace(directory_path, shepherd_num, sheep_num, trial_nums, param):
    sns.set(style="white")
    max_line = 0
    # Set 10000 as default minimun line number
    min_line = 10000 
    trial_num = trial_nums[0]
    for i in trial_nums:
        file_path = directory_path + "/data/" + "{}sh{}tr{}.csv".format(str(shepherd_num), str(sheep_num), str(i))
        cnt = count_line(file_path)
        # if cnt > max_line:
        #     max_line = cnt
        #     trial_num = i
        if cnt < min_line:
            min_line = cnt
            trial_num = i
    print(trial_num)
    
    # Trial number also starts from 0
    file_path = directory_path + "/data/" + "{}sh{}tr{}.csv".format(str(shepherd_num), str(sheep_num), str(trial_num))
    with open(file_path) as f:
        reader = csv.reader(f, delimiter=',')
        fig, ax = plt.subplots(figsize=(8,8))
        # For trace
        sheeps_color = []
        sheeps_pos = []
        shepherds_color = []
        shepherds_pos = []
        index = 0
        # row_num = 0
        log_png_path = directory_path + "/png/{}sh{}tr{}".format(str(shepherd_num), str(sheep_num), str(trial_num))
        # os.makedirs(log_png_path)
        for row in reader:
            if len(row) != sheep_num + shepherd_num:
                break
            # For trace
            sheeps_color_row = []
            sheeps_pos_row = []
            shepherds_color_row = []
            shepherds_pos_row = []
            for i in range(0, sheep_num):
                color, pos = str_to_color_nparray(row[i])
                sheeps_color.append(color)
                sheeps_pos.append(pos)
                sheeps_color_row.append(color)
                sheeps_pos_row.append(pos)
            for i in range(sheep_num, sheep_num + shepherd_num):                    
                color, pos = str_to_color_nparray(row[i])
                shepherds_color.append(color)
                shepherds_pos.append(pos)
                shepherds_color_row.append(color)
                shepherds_pos_row.append(pos)

            fig_row, ax_row = plt.subplots(figsize=(8,8))
            init_plot_line_csv(ax_row, param, sheeps_color_row, sheeps_pos_row, shepherds_color_row, shepherds_pos_row)
            fig_path = log_png_path + "/{}.png".format(str(index))
            # print(fig_path)
            fig_row.savefig(fig_path)
            index += 1
            ax_row.clear()
            plt.clf()
            plt.close()
            
        # png_path = directory_path + "/png"
        generate_gif_csv(log_png_path, directory_path + "/gif/{}sh{}tr{}.gif".format(str(shepherd_num), str(sheep_num), str(trial_num)), index)

        init_trace_csv(ax, param, sheeps_color, sheeps_pos, shepherds_color, shepherds_pos)
        
        fig_path = directory_path + "/gif/{}sh{}tr{}.pdf".format(str(shepherd_num), str(sheep_num), str(trial_num))
        # row_num = row_num + 1
        fig.savefig(fig_path) 
        ax.clear()
        plt.clf()
        plt.close()
    f.close()

# ''' Draw all trace gifs through graphs by trace '''
# def csv_all_trace(directory_path, shepherd_num, sheep_num, trial_num, param):
#     for shepherd in range(shepherd_num):
#         for sheep in range(sheep_num):
#             for trial in range(trial_num):
#                 print(shepherd)
#                 # csv_trace(directory_path, shepherd, sheep, trial, param)
