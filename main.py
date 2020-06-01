import pkga as ga
import plot_squares
import random            
#testowe duzy kwadrat 500, 500
#3 prostokaty 200,100 : 300,50: 100: 100

class FitSquare:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def place(self, x_pos, y_pos, flip=False):
        if not flip:
            return PlacedSquare(x_pos, y_pos, self.width, self.height)
        else:
            return PlacedSquare(x_pos, y_pos, self.height, self.width)

class PlacedSquare:
    def __init__(self, x_pos, y_pos, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.area = width * height
        self.upper_left = x_pos, y_pos
        self.lower_right = x_pos + width, y_pos + height
    #todo metoda plot ?

    def check_overlap(self, other):
        a = min(self.lower_right[0], other.lower_right[0])
        b = max(self.upper_left[0], other.upper_left[0])
        c = max(0, a - b)
        d = min(self.lower_right[1], other.lower_right[1])
        e = max(self.upper_left[1], other.upper_left[1])
        f = max(0, d - e)

        return c * f

class SQMutator:
    def __init__(self, default_mutation_rate):
        self.default_mutation_rate = default_mutation_rate
    def mutate(self, specimen, generation):
        mutation_rate = self.default_mutation_rate

        if specimen.fitness == 0:
            mutation_rate = 0.5

        specimen.mutate(mutation_rate)


class SquareFittingEvaluator:
    def __init__(self, parent_square, fit_squares):
        self.fit_squares = fit_squares
        self.parent_square = parent_square

    def map_data(self, decoded_specimen):
        placed_squares = []
        for key, value in decoded_specimen.decode().items():
            if not value["exist"]:
                continue

            matching_square = self.fit_squares[key]
            placed = matching_square.place(value['x'], value['y'], flip=value['flip'])
            placed_squares.append(placed)
        return placed_squares


    def evaluate(self, out, generation):
        rectangles = self.map_data(out)
        non_overlappping_area_sum = 0

        #todo use overlap sum for handicap function
        overlap_sum = 0
        for r1 in rectangles:
            if(r1.check_overlap(self.parent_square) != r1.area):
                overlap_sum += 10000

            for r2 in rectangles:
                if r1 == r2:
                    continue
                overlap = r1.check_overlap(r2)
                overlap_sum += overlap
                non_overlappping_area_sum += r1.area - overlap

        return max(0,non_overlappping_area_sum - pow(overlap_sum, 2))

parent_square = PlacedSquare(0, 0, 500, 500)
test_data = []
for i in range(7):
    h = random.randint(30,300)
    w = random.randint(30,300)
    test_data.append(FitSquare(h,w))
evaluator = SquareFittingEvaluator(parent_square, test_data)


solution_template = ga.GAMultiValueTemplate()
for i in range(len(test_data)):

    range_offset = min(test_data[i].width, test_data[i].height)
    # todo replace 500 literal with actual value
    x_value = ga.GAFloatValueTemplate(0, 500 - range_offset, 8)
    y_value = ga.GAFloatValueTemplate(0, 500 - range_offset, 8)
    exist_value = ga.GABoolValueTemplate()
    flip_value = ga.GABoolValueTemplate()
    square_template = ga.GAMultiValueTemplate()
    square_template.add_value("x", x_value)
    square_template.add_value("y", y_value)
    square_template.add_value("exist", exist_value)
    square_template.add_value("flip", flip_value)
    solution_template.add_value(i, square_template)


s = ga.Simulation(200, solution_template, evaluator)
s.crossover_rate = 0.7
s.selector = ga.RouletteSelector()
s.mutator = SQMutator(0.05)
s.initialize()
s.run()

specimens = list(sorted(s.pop, key=lambda x:x.fitness, reverse=True))
best = specimens[0]

zero_fitness_specimens = list(filter(lambda x:x.fitness == 0, specimens))
print(specimens)
print("Zero fitness specimens: " + str(len(zero_fitness_specimens)))
print("Best fitness:" + str(best.fitness))
plot_squares.plot_specimen(best, test_data, 500, 500)



        

