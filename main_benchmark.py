from objects.variable import Variable
from objects.domain import Domain
from objects.wrapper import cartography_constraints
from csp import CSP
from utils.parser import parse_carto
from cartography import Cartography
from queens import Queens

import pandas as pd
import argparse
import time
import numpy as np
import os

import matplotlib.pyplot as plt
import networkx as nx
from random import randint
import matplotlib.pyplot as plt

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", help="problem to be solved",
                        choices=["queens", "cartography"], default="quens")
    parser.add_argument("-d", "--data_path", help="path to the instance", type=str, default="instances/carto_queen5_5_opti5.txt")
    parser.add_argument("-s", "--save_file", help="Path to the score file", type=str, default="data/scores_carto.csv")
    parser.add_argument("-t", "--timelimit", help="Time limit (seconds)", type=int, default=200)
    parser.add_argument("-p", "--parameter", help="number of queens or number of colors", type=int, default=4)
    parser.add_argument("-var", "--var_heuristic", help="which heuristic to branch on the variables", type=int, default=1)
    parser.add_argument("-val", "--val_heuristic", help="which heuristic to branch on the values", type=int, default=1)
    #option pour lancer les benchmarks
    args = parser.parse_args()

    data_file = args.data_path
    save_file = args.save_file
    mode = args.mode
    param = args.parameter

    mode_var_heuristic=args.var_heuristic
    mode_val_heuristic=args.val_heuristic
    
    time_limit = args.timelimit


    # mode queens
    if mode == "cartography":
        
        cartography = Cartography(nb_colors=param, file_name=data_file)
        #print(f"Solving Cartography Problem with n = {param} colors and instance {file.split('/')[1]}...")
        solution, termination_status, execution_time, n_branching = cartography.main(instantiation=dict(), mode_var_heuristic=mode_var_heuristic, mode_val_heuristic=mode_val_heuristic, time_limit=time_limit)
    
        

        #stockage des valeurs
        terminated = True #TODO: changer les returns de la fonction
        solution_found = solution
        execution_time = execution_time
        n_colors = param


        df = pd.read_csv(save_file, sep=";")
        df = df.set_index(["instance", "n_colors", "mode_var_heuristic", "mode_val_heuristic"])

        index = (data_file, param, mode_var_heuristic, mode_val_heuristic)

        if df.index.isin([index]).any():
            df.at[index, "solution_found"] = solution
            df.at[index, "termination_status"] = termination_status
            df.at[index, "convergence_time (s)"] = execution_time
            df.at[index, "time_limit (s)"] = time_limit
            df.at[index, "n_nodes_open"] = n_nodes_open
            df.reset_index(inplace=True)

        else:
            df.reset_index(inplace=True)
            df = df.append({"instance": data_file, "n_colors": n_colors,"mode_var_heuristic":mode_var_heuristic, 
            "mode_val_heuristic":mode_val_heuristic, "termination_status": termination_status, "convergence_time (s)":execution_time, 
            "n_nodes_open": n_branching, "time_limit (s)": time_limit, "solution_found" : solution
            },
                            ignore_index=True)

        df.to_csv(save_file, sep=";", index=False)

    if mode == "queens":
        
        queens = Queens(nb_columns=param)

        solution, termination_status, execution_time, n_branching = queens.main(instantiation=dict(), mode_var_heuristic=mode_var_heuristic,
                                    mode_val_heuristic=mode_val_heuristic, time_limit=time_limit)

        #stockage des valeurs
        
        solution_found = solution
        nqueens = param


        df = pd.read_csv(save_file, sep=";")
        df = df.set_index(["nqueens", "mode_var_heuristic", "mode_val_heuristic"])

        index = (param, mode_var_heuristic, mode_val_heuristic)

        if df.index.isin([index]).any():
            df.at[index, "solution_found"] = solution
            df.at[index, "termination_status"] = termination_status
            df.at[index, "time_limit (s)"] = time_limit
            df.at[index, "convergence_time (s)"] = execution_time
            df.at[index, "n_nodes_open"] = n_branching
            df.reset_index(inplace=True)

        else:
            df.reset_index(inplace=True)
            df = df.append({"nqueens": param, "mode_var_heuristic":mode_var_heuristic, "mode_val_heuristic":mode_val_heuristic, 
            "termination_status": termination_status, "convergence_time  (s)":execution_time, "n_nodes_open": n_branching,
            "solution_found" : solution, "time_limit  (s)": time_limit},
                            ignore_index=True)

        df.to_csv(save_file, sep=";", index=False)



