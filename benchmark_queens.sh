#!/bin/bash

for nqueens in {19..20};
do  
    for var_heuristic in {1..4}; do
        for val_heuristic in {1..2}; do
            echo $nqueens $var_heuristic $val_heuristic
            python3 main_benchmark.py -m "queens" -s "saves/scores_queens.csv" -p $nqueens -var $var_heuristic -val $val_heuristic > "logs/logs_queens/${nqueens}_${var_heuristic}.txt"
        done
    done
done