#!/bin/bash

file="instances/sudoku_1.txt"
python3 main_benchmark.py -m "sudoku" -d $file -s "saves/scores_sudoku.csv" -p --no_arc_consistency > "logs/logs_sudoku/AC_FC.txt"
python3 main_benchmark.py -m "sudoku" -d $file -s "saves/scores_sudoku.csv" -p --no_arc_consistency > "logs/logs_sudoku/no_AC_FC.txt"
python3 main_benchmark.py -m "sudoku" -d $file -s "saves/scores_sudoku.csv" -p --no_forward_checking > "logs/logs_sudoku/AC_no_FC.txt"
python3 main_benchmark.py -m "sudoku" -d $file -s "saves/scores_sudoku.csv" -p --no_forward_checking > "logs/logs_sudoku/no_AC_no_FC.txt"
