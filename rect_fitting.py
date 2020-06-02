from geometry import Square, PlacedSquare

class OrderedSquare(Square):
    def __init__(self, width, height, order, flip=False):
        self.order = order
        
        if flip:
            Square.__init__(self, width, height)
        else:
            Square.__init__(self, height, width)
    
    def __repr__(self):
        return f"{Square.__repr__(self)} order: {self.order}"


    def place(self, parent_square, placed_squares):
        placed_squares = sorted(placed_squares, key=lambda x:x.y_pos + x.height)

        for square in placed_squares:
            p = square.lower_right[1]
            t = p + self.height
            r = square.lower_right[0]
            l = r - self.width

            on_this_square = list(filter(lambda x:x.is_within(p,t) and x!=square and x.x_pos + x.width < l, placed_squares))
            if len(on_this_square) == 0:
                x_p = 0
            else:
                rightmost = max(on_this_square, key=lambda x:x.lower_right[0])
                x_p = rightmost.lower_right[0]

            sqr = PlacedSquare(x_p, square.lower_right[1], self.width, self.height)

            parent_overlap = sqr.check_overlap(parent_square)
            if parent_overlap != sqr.area:
                continue
            
            overlap_detected = False
            for compared in placed_squares:
                if compared == square:
                    continue
                
                overlap = sqr.check_overlap(compared)
                if overlap != 0:
                    overlap_detected = True

            if overlap_detected:
                continue
            return sqr

class SQMutator:
    def __init__(self, default_mutation_rate):
        self.default_mutation_rate = default_mutation_rate
    def mutate(self, specimen, generation):
        mutation_rate = self.default_mutation_rate
        specimen.mutate(mutation_rate)

class SquareFittingEvaluator:
    def __init__(self, parent_square, fit_squares):
        self.fit_squares = fit_squares
        self.parent_square = parent_square

    def map_data(self, decoded_specimen):
        placed_squares = []
        for key, value in decoded_specimen.decode().items():
            matching_square = self.fit_squares[key]
            placed = OrderedSquare(matching_square.width, matching_square.height, value["order"], value["flip"])
            placed_squares.append(placed)
        return placed_squares

    def place_rectangles(self, rectangles):
        top_boundary = PlacedSquare(0,0, self.parent_square.width, 0)
        placed_rects = [top_boundary]

        for rect in sorted(rectangles, key=lambda r:r.order):
            placed = rect.place(self.parent_square, placed_rects)

            if placed:
                placed_rects.append(placed)

        return placed_rects[1:]

    def calc_fitness(self, placed_rectangles):
        areas = map(lambda x: x.area, placed_rectangles)
        return sum(areas)

    def evaluate(self, out, generation):
        rectangles = self.map_data(out)
        placed_rects = self.place_rectangles(rectangles)

        return self.calc_fitness(placed_rects)