import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as anim
import time

''' Recorded simulation data into csv files '''

''' Initiliaze plot line by csv '''
def init_plot_line_csv(ax, param, sheeps_color, sheeps_pos, shepherds_color, shepherds_pos):
    # Sheep
    for i in range(len(sheeps_color)):
        ax.plot(sheeps_pos[i][0], sheeps_pos[i][1], sheeps_color[i] + 'o', alpha=0.5) 
    # Shepherd
    for i in range(len(shepherds_color)):
        # shepherd_color = shepherds[i][0]
        # shepherd_pos = shepherds[i][1]
        ax.plot(shepherds_pos[i][0], shepherds_pos[i][1], shepherds_color[i] + 'o', alpha=0.5)
    # Goal
    goal_zone = patches.Circle(param["goal"], param["goal_radius"], ec="k", fc='white', alpha=1)
    ax.add_patch(goal_zone)
    # x,y axis range
    xy_range = param["sheep_initial_pos_radius"] + 40
    ax.set_xlim(-xy_range, xy_range)
    ax.set_ylim(-xy_range, xy_range)
    ax.set_aspect('equal') 

''' Initiliaze plot line by csv, more obvious '''
def init_plot_line_csv_spec(ax, param, sheeps_color, sheeps_pos, shepherds_color, shepherds_pos):
    # Sheep
    for i in range(len(sheeps_color)):
        ax.plot(sheeps_pos[i][0], sheeps_pos[i][1], sheeps_color[i] + 'o', alpha=0.5) 
    # Shepherd
    for i in range(len(shepherds_color)):
        # shepherd_color = shepherds[i][0]
        # shepherd_pos = shepherds[i][1]
        ax.plot(shepherds_pos[i][0], shepherds_pos[i][1], shepherds_color[i] + 'o', alpha=0.9, markersize=10)
    # Goal
    goal_zone = patches.Circle(param["goal"], param["goal_radius"], ec="k", fc='white', alpha=1)
    ax.add_patch(goal_zone)
    # x,y axis range
    xy_range = param["sheep_initial_pos_radius"] + 40
    ax.set_xlim(-xy_range, xy_range)
    ax.set_xticks([-100, 100])
    ax.set_ylim(-xy_range, xy_range)
    ax.set_yticks([-100, 100])
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.set_aspect('equal') 

''' Initiliaze trace by csv '''
def init_trace_csv(ax, param, sheeps_color, sheeps_pos, shepherds_color, shepherds_pos):
    # Sheep
    for i in range(len(sheeps_color)):
        # Only k, not sheeps_color[i]
        ax.plot(sheeps_pos[i][0], sheeps_pos[i][1], 'k' + 'o', alpha=0.1, markersize='1') 
    
    # Shepherd
    for i in range(len(shepherds_color)):
        # shepherd_color = shepherds[i][0]
        # shepherd_pos = shepherds[i][1]
        ax.plot(shepherds_pos[i][0], shepherds_pos[i][1], shepherds_color[i] + 'o', alpha=0.4, markersize='4')

    # Goal
    goal_zone = patches.Circle(param["goal"], param["goal_radius"], ec="k", fc='white', alpha=1)
    
    ax.add_patch(goal_zone)
    # x,y axis range
    xy_range = param["sheep_initial_pos_radius"] + 40
    ax.set_xlim(-xy_range, xy_range)
    ax.set_xticks([-100, 100])
    ax.set_ylim(-xy_range, xy_range)
    ax.set_yticks([-100, 100])
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.set_aspect('equal') 

''' Figure out which sheep is target sheep '''
def check_target(sheeps, target_sheep):
    for i in range(len(sheeps)):
        # 2D space with x,y attribute
        if sheeps[i].position[0] == target_sheep.position[0] and sheeps[i].position[1] == target_sheep.position[1]:
            return i 
    return 0

''' Write a line into csv in each step '''
def write_line_csv(writer, sheeps, shepherds):
    # k for sheep, r for alive shepherds, c for fault shepherds
    s = ["k " + str(sheeps[i].position) for i in range(len(sheeps))] 
    for i in range(len(shepherds)):
        # Plot special color dot at target sheep
        if shepherds[i].target_sheep and shepherds[i].target_sheep != []:
            target = check_target(sheeps, shepherds[i].target_sheep)
            s[target] = s[target].replace('k', 'y') 

    writer.writerow(s)

''' Write last line into csv with a result '''
def write_last_line_csv(writer, result):
    writer.writerow(result)