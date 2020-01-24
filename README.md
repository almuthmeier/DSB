DSB (Dynamic Sine Benchmark)
==================================================================================================

In [1] we proposed the Dynamic Sine Benchmark (DSB) as dynamic optimization benchmark especially suited for the evaluation of prediction-based optimization heuristics. In the meantime, we improved the generator and fixed some bugs. This project contains the updated code of the DSB generator, while the original code can be accessed in our project [DynOpt](https://github.com/almuthmeier/DynOpt)). 

DSB moves static fitness functions, like Sphere or Rastrigin, in the solution space, while the fitness landscape's shape remains unchanged. For each movement of the fitness function, DSB defines an anchor point that determines the fitness landscape's position in the solution space. The anchor points are sampled from trigonometric functions, and the difficulty of the dynamics can be quantified by the parameters velocity and curviness. A detailed description of DSB can be found in this [document](link).

[1] A. Meier, O. Kramer: Predictive Uncertainty Estimation with Temporal Convolutional Networks for Dynamic Evolutionary Optimization, ICANN 2019.

## Requirements & Installation
In order to run this python project you need a python installation and numpy. The code has been tested with:  
    - Python 3.5.2  
    - Ubuntu 16.04  
    
## Package Structure
- DSB/  
    - code/  
        - dsb.py (generates one DSB instance)   
        - fitnessfunctions.py (standard fitness functions)  
        - generator.py (calls dsb.py, generates sequentially multiple DSB instances, e.g. for different dimensionalities or fitness functions)  
    - datasets/ (is created automatically when the code is run; contains the generated data sets)   

## Usage
1. Define your settings in generator.py. Example:
    - n_chg_periods = 10000 (number of change periods, i.e. number of anchor points)
    - dims = [2, 5, 10, 20] (dimensionalities for that a data set should be created)
    - functions = [sphere, rastrigin, rosenbrock] (fitness functions for that a data set should be created)
    - lbound = 0 (lower bound of solution space)
    - ubound = 900 (upper bound of solution)
    - desired_curv = 10 (desired curviness)
    - desired_med_vel = 2.0 (desired median velocity)
    - max_n_functions = 4 (maximum number of component functions; doesn't need to be changed)
    - n_base_time_points = 100 (number samples in base interval; should left unchanged)

2. Run generator.py. For each combination of fitness function and dimensionality a data set is generated. The output files have unique names containing the fitness function, dimensionality, number change periods, date, and time. An example would be: rastrigin_d-20_chgperiods-10000_2020-01-23_15:32.npz.

3. Use the generated anchor points to move fitness functions in your application, i.e., load the generated .npz-file(s) by numpy.


## Content of Output Files
The generated data set files contain five elements:     
    - **fcts_params_per_dim**: 3d array, format [dimensionality, number component functions, 5]. Contains for each dimension the parameters of the generating functions.     
    - **orig_global_opt_pos**: 1d array, format [dimensionality]. Contains global optimum position of the unmoved fitness function.     
    - **global_opt_fit_per_chgperiod**: 1d array, format [number of change periods]. Contains for each change period the optimum fitness.   
    - **global_opt_pos_per_chgperiod**: 2d array, format [number of change periods, dimensionality]. Contains for each change period the optimum position.      
    - **step_size**: scalar. The sampling step size.    
