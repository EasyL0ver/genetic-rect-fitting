import pkga as ga
import plot_squares
import random
from itertools import groupby
from geometry import Square, PlacedSquare
import rect_fitting as rf
from rect_fitting import OrderedSquare, SQMutator, SquareFittingEvaluator, PermutationSquareInitializer
import time
import gaio
import sys
import os

print(f"Running script in working directory: {os.getcwd()}")

g_start_time = time.time()
g_dead_line = g_start_time + 0.1 * 60
g_parent_w = 2800
g_parent_h = 2070
g_show_plot = False
g_monitor_conv = False
g_input_path = "maleplyty.txt"
g_output_path  = "output.txt"
g_plot_path = "./plots/"

la = len(sys.argv)
if la >= 2:
    g_input_path = sys.argv[0]
if la >= 3:
    g_output_path = sys.argv[1]


parent_square = PlacedSquare(0, 0, g_parent_w, g_parent_h)
fit_squares = gaio.prepare_input_data(g_input_path)
evaluator = SquareFittingEvaluator(parent_square, fit_squares)

solution_template = ga.GAMultiValueTemplate()
for i in range(len(fit_squares)):
    order_value = ga.GAIntegerValueTemplate(0, 64, 6)
    flip_value = ga.GABoolValueTemplate()
    square_template = ga.GAMultiValueTemplate()
    square_template.add_value("sqr_id", order_value)
    square_template.add_value("flip", flip_value)
    solution_template.add_value(i, square_template)

s = ga.Simulation(500, solution_template, evaluator)
s.crossover_operator = ga.PermutationCrossover(1, 7, len(fit_squares))
s.selector = ga.RouletteSelector()
s.mutator = rf.PermutationWithFlipMutator(0.03, 7, len(fit_squares))
s.monitor = g_monitor_conv
s.initialize(PermutationSquareInitializer(len(fit_squares), 6))

while time.time() < g_dead_line:
    s.step()

best = s.get_ordered_specimens()[0]
mapped_best = evaluator.map_data(best)
rectangles = evaluator.place_rectangles(mapped_best)

print("Best fitness:" + str(best.fitness))
print("Program finished after: " + str(time.time() - g_start_time))
print(f"After: {s.current_generation} generations")

if g_monitor_conv:
    plot_squares.plot_convergence(s.monitor_logs, s.monitor_logs_avg)

plot_squares.print_coverage_data(parent_square, rectangles)
plot_squares.plot_outcome(parent_square, rectangles, g_plot_path, show=g_show_plot)

gaio.write_output_data(fit_squares, rectangles, g_output_path)