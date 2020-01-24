'''
Creates and stores data sets for dynamic variants of the  sphere, 
rosenbrock, rastrigin, and griewank function with the DSB generator.
The entries in the data sets are stored per change period.

Contains also functionality for computing the fitness during the runtime. 

With create_problems() the data sets are created. There the desired parameters
have to be specified.

Created on Jan 23, 2020

@author: ameier
'''

import copy
import datetime
import os
import sys
import warnings

from code.dsb import generate_sine_fcts_for_multiple_dimensions
from code.fitnessfunctions import sphere, rosenbrock, rastrigin,\
    get_original_global_opt_pos_and_fit, griewank
import numpy as np


sys.path.append(os.path.abspath(os.pardir))


def create_problems():
    '''
    Computes for each change the global optimum position. 
    '''

    day, time = get_current_day_time()
    # -------------------------------------------------------------------------

    # parameters to adjust
    n_chg_periods = 10000
    dims = [2, 5, 10, 20]
    functions = [sphere, rastrigin, rosenbrock]
    lbound = 0
    ubound = 900

    desired_curv = 10
    desired_med_vel = 2.0
    max_n_functions = 4
    n_base_time_points = 100
    # -------------------------------------------------------------------------

    # path to data set directory to store data sets there
    # ".../DSB/DSB/code"
    split_path = os.path.abspath(os.pardir).split('/')
    # ".../DSB/DSB"
    path_to_dynopt = '/'.join(split_path[:-1])

    # store global optimum fitness (stays same for all changes)
    global_opt_fit = np.array(n_chg_periods * [0])

    # create data sets
    for func in functions:
        # output path
        func_name = func.__name__
        output_dir_path = path_to_dynopt + "/datasets/" + func_name + "/"
        if not os.path.exists(output_dir_path):
            os.makedirs(output_dir_path)

        for dim in dims:
            # output file name
            ds_file_name = output_dir_path + func_name + "_d-" + \
                str(dim) + "_chgperiods-" + str(n_chg_periods) + \
                "_" + day + '_' + time + ".npz"

            # same seed for different functions so that the movement is same
            np_rand_gen = np.random.RandomState(234012)
            seed = np_rand_gen.randint(4)

            # global optimum position in unmoved function
            orig_global_opt_position, _ = get_original_global_opt_pos_and_fit(
                func, dim)

            # compute optimum movement
            opts = []
            opts.append(copy.copy(orig_global_opt_position))
            opts, fcts_params_per_dim, step_size = generate_sine_fcts_for_multiple_dimensions(dim, n_chg_periods, seed,
                                                                                              n_base_time_points,
                                                                                              lbound, ubound, desired_curv,
                                                                                              desired_med_vel, max_n_functions)
            opts = np.array(opts)

            # save optimum sequence
            np.savez(ds_file_name, global_opt_fit_per_chgperiod=global_opt_fit,
                     global_opt_pos_per_chgperiod=opts, orig_global_opt_pos=orig_global_opt_position,
                     fcts_params_per_dim=fcts_params_per_dim,
                     step_size=step_size)


###############################################################################
# for fitness computation, e.g. in an evolution strategy
###############################################################################
def original_fitness(x, problem):
    '''
    Computes fitness for this individual.
    Assumes that the individual/fitness function is not moved.
    '''
    # TODO(dev) extend by new fitness functions
    if problem == "sphere":
        return sphere(x)
    elif problem == "rosenbrock":
        return rosenbrock(x)
    elif problem == "rastrigin":
        return rastrigin(x)
    elif problem == "griewank":
        return griewank(x)
    else:
        msg = "original_fitness(): unknown problem " + problem
        warnings.warn(msg)


def compute_fitness(x, gen, problem, global_opt_pos_per_gen, orig_opt_pos):
    '''
    Computes the fitness of the passed individual. Depends on the current
    generation.
    @param x: individual
    @param gen: current generation
    @param problem: name of fitness function: sphere, rosenbrock, rastrigin, griewank
    @param global_opt_pos_per_gen: 2d numpy array, contains the global optimum
    position for each generation
    @param orig_opt_pos: global optimum position of unmoved fitness landscape 
    '''
    # compute optimum movement
    # (since new optimum position was computed by adding the movement to the
    # original one, backwards the movement can be computed by substraction)
    optimum_movement = global_opt_pos_per_gen[gen] - orig_opt_pos
    # move individual, so that its fitness can be computed with the original
    # function
    moved_x = x - optimum_movement
    return original_fitness(moved_x, problem)


###############################################################################
# date and time
###############################################################################
def get_current_day_time():
    current_date = datetime.datetime.now()
    day = str(current_date.year) + '-' + \
        str(current_date.month).zfill(2) + '-' + str(current_date.day).zfill(2)
    time = str(current_date.hour).zfill(2) + ':' + \
        str(current_date.minute).zfill(2)
    return day, time

###############################################################################


if __name__ == '__main__':
    create_problems()
