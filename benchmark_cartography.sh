#!/bin/bash

data_list=("instances/carto_myciel4_opti5.txt" "instances/carto_queen5_5_opti5.txt" "instances/carto_le450_5a_opti5.txt" "instances/carto_le450_25a_opti25.txt")

for file in ${data_list[@]}; do
    for color in {4..7}; do 
        for var_heuristic in {1..4}; do
            for val_heuristic in {1..2}; do
                echo $file $color $var_heuristic $val_heuristic
                python3 main_benchmark.py -m "cartography" -d $file -s "saves/scores_cartography.csv" -p $color -var $var_heuristic -val $val_heuristic > "logs/logs_carto/${color}_${var_heuristic}.txt"
            done
        done
    done
done