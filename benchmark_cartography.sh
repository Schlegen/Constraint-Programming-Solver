#!/bin/bash

data_list=("instances/carto_myciel4_opti5.txt" "instances/carto_queen5_5_opti5.txt")

for file in ${data_list[@]}; do
    for color in {5..7}; do 
        for var_heuristic in {1..4}; do
            echo $file $var_heuristic
            python3 main_benchmark.py -m "cartography" -d $file -s "saves/scores_cartography.csv" -p $color -var $var_heuristic > "logs/logs_carto/${color}_${var_heuristic}.txt"
        done
    done
done