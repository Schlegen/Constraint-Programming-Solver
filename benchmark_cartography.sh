#!/bin/bash

# data_list=("instances/carto_myciel4_opti5.txt" "instances/carto_queen5_5_opti5.txt" "instances/carto_le450_5a_opti5.txt")
# for file in ${data_list[@]}; do
#     for color in {4..6}; do 
#         for var_heuristic in {1..4}; do
#             for val_heuristic in {1..2}; do
#                 echo $file $color $var_heuristic $val_heuristic
#                 python3 main_benchmark.py -m "cartography" -d $file -s "saves/scores_cartography.csv" -p $color -var $var_heuristic -val $val_heuristic > "logs/logs_carto/${color}_${var_heuristic}.txt"
#             done
#         done
#     done
# done

data_list=("instances/carto_queen6_6_opti7.txt" "instances/carto_queen7_7_opti7.txt")
for file in ${data_list[@]}; do
    for color in {6..8}; do 
        for var_heuristic in 2; do
            for val_heuristic in 1; do
                echo $file $color $var_heuristic $val_heuristic
                python3 main_benchmark.py -m "cartography" -d $file -s "saves/scores_cartography.csv" -p $color -var $var_heuristic -val $val_heuristic > "logs/logs_carto/${color}_${var_heuristic}.txt"
            done
        done
    done
done

# file="instances/carto_le450_25a_opti25.txt"
# for color in {25..26}; do 
#     for var_heuristic in {1..4}; do
#         for val_heuristic in {1..2}; do
#             echo $file $color $var_heuristic $val_heuristic
#             python3 main_benchmark.py -m "cartography" -d $file -s "saves/scores_cartography.csv" -p $color -var $var_heuristic -val $val_heuristic > "logs/logs_carto/${color}_${var_heuristic}.txt"
#         done
#     done
# done
