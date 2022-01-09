#!/bin/bash

for nqueens in {1..15};
do  
    for var_heuristic in {1..4}; do
        echo $nqueens $var_heuristic
        python3 main_benchmark.py -m "queens" -s "saves/scores_queens.csv" -p $nqueens -var $var_heuristic > "logs/logs_queens/${nqueens}_${var_heuristic}.txt"
    done
done