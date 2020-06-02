import pkga as ga
import plot_squares
import random
from itertools import groupby
from geometry import Square, PlacedSquare
from rect_fitting import OrderedSquare, SQMutator, SquareFittingEvaluator


parent_square = PlacedSquare(0, 0, 500, 500)
test_data = [Square(150,150), Square(300,300), Square(100,100)]
mapped_test = [OrderedSquare(150,150,1), OrderedSquare(300,300,2), OrderedSquare(100,100,3)]
test_data = []
for i in range(30):
    test_data.append(Square(random.randint(30,200), random.randint(30,200)))
evaluator = SquareFittingEvaluator(parent_square, test_data)


solution_template = ga.GAMultiValueTemplate()
for i in range(len(test_data)):
    order_value = ga.GAFloatValueTemplate(0, 100, 6)
    flip_value = ga.GABoolValueTemplate()
    square_template = ga.GAMultiValueTemplate()
    square_template.add_value("order", order_value)
    square_template.add_value("flip", flip_value)
    solution_template.add_value(i, square_template)


s = ga.Simulation(10, solution_template, evaluator)
s.crossover_rate = 0.7
s.selector = ga.RouletteSelector()
s.mutator = SQMutator(0.03)
s.initialize()
s.run()

specimens = list(sorted(s.pop, key=lambda x:x.fitness, reverse=True))
best = specimens[0]

mapped_best = evaluator.map_data(best)
rectangles = evaluator.place_rectangles(mapped_best)

zero_fitness_specimens = list(filter(lambda x:x.fitness == 0, specimens))
print(specimens)
print("Zero fitness specimens: " + str(len(zero_fitness_specimens)))
print("Best fitness:" + str(best.fitness))

plot_squares.plot_outcome(parent_square, rectangles)




        

