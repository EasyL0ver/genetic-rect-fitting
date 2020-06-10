import numpy as np
import random

class GABoolValueTemplate:
    def __init__(self):
        self.bits = 1

    def decode(self, bit_array):
        if len(bit_array) != self.bits:
            raise "Cannot decode, array length mismatch"
        return bool(bit_array[0])


class GAIntegerValueTemplate:
    def __init__(self, min_value, max_value, bits):
        diff = max_value - min_value
        self.bits = bits
        self.bit_factor = diff / (pow(2, bits) - 1)
        self.min_value = min_value
        self.max_value = max_value

    def decode(self, bit_array):
        if len(bit_array) != self.bits:
            raise "Cannot decode, array length mismatch"

        out = 0
        for bit in bit_array:
            out = (out << 1) | bit

        return int(round(self.min_value + out * self.bit_factor))


class GAFloatValueTemplate:
    def __init__(self, min_value, max_value, bits):
        self.min_value = min_value
        self.max_value = max_value
        self.bits = bits

        self.bit_factor = (max_value - min_value) / (pow(2, bits)  - 1)

    def decode(self, bit_array):
        if len(bit_array) != self.bits:
            raise "Cannot decode, array length mismatch"

        out = 0
        for bit in bit_array:
            out = (out << 1) | bit

        return self.min_value + out * self.bit_factor

class GAMultiValueTemplate:
    def __init__(self):
        self.values = dict()
        self.bits = 0

    def add_value(self, value_name, value_template):
        self.values[value_name] = value_template
        self.bits = self.bits + value_template.bits

    def decode(self, bit_array):
        if len(bit_array) != self.bits:
            raise "Cannot decode, array length mismatch"
        
        out = dict()
        index = 0

        for value_name, value_template in self.values.items():
            chunk = bit_array[index:index + value_template.bits]
            decoded = value_template.decode(chunk)

            out[value_name] = decoded
            index = index + value_template.bits

        return out

class Gene:
    def __init__(self, bit_string):
        self.bit_string = bit_string

    def __repr__(self):
        return str(self.bit_string)

    def copy(self):
        return Gene(self.bit_string.copy())

    def mutate(self, pmut):
        mutated = False
        for i in range(len(self.bit_string)):
            if random.random() < pmut:
                self.bit_string[i] = not self.bit_string[i]
                mutated = True
        return mutated

class Specimen:
    def __init__(self, genome, template):
        self.genome = genome
        self.template = template
        self.fitness = 0

    def __repr__(self):
        decoded = self.template.decode(self.genome.bit_string)
        return f"Specimen with fitness:{self.fitness} and value:{decoded}" 

    def mutate(self, pmut):
        return self.genome.mutate(pmut)

    def copy(self):
        return Specimen(self.genome.copy(), self.template)


    def decode(self):
        return self.template.decode(self.genome.bit_string)

    @staticmethod
    def create_random(template):
        random_string = np.random.choice([True, False], size=template.bits)
        return Specimen(Gene(random_string), template)

class RouletteSelector:
    def select(self, population):
        fitness_sum = sum(map(lambda x:x.fitness, population))
        selection_roll = random.random() * fitness_sum

        index = 0
        for specimen in population:
            index = index + specimen.fitness
            if index >= selection_roll:
                return specimen
        
        raise "Nothing chosen with roullette selecter"
            

class OnePointBinaryCrossover:
    def __init__(self, pcross):
        self.pcross = pcross
    def cross_over(self, a, b):
        if random.random() > self.pcross:
            return
        index = random.randint(1, len(a.genome.bit_string) - 1)
        tmp = b.genome.bit_string[:index].copy()
        b.genome.bit_string[:index], a.genome.bit_string[:index]  = a.genome.bit_string[:index], tmp


class PermutationCrossoverBin:
    def __init__(self, bit_arr):
        self.bit_arr = bit_arr

    def __repr__(self):
        out = 0
        for bit in self.bit_arr:
            out = (out << 1) | bit
        return f"B{str(out)}"

    def __str__(self):
        return self.__repr__()
    
    def compare_to(self, other):
        if not other:
            return False
            
        for i in range(len(self.bit_arr)):
            if self.bit_arr[i] != other.bit_arr[i]:
                return False
        return True

class PermutationCrossover:
    def __init__(self, pcross, bin_size, bin_amount):
        self.pcross = pcross
        self.bin_size = bin_size
        self.bin_amount = bin_amount

    def roll_cross_over_points(self):
        a = random.randint(0, self.bin_amount)
        b = random.randint(0, self.bin_amount)
        s = sorted([a, b])
        return s[0], s[1]

    def convert_to_bins(self, arr):
        bins = [None] * (len(arr) // self.bin_size)
        for i in range(len(bins)):
            sl = arr[i * self.bin_size:(i + 1) * self.bin_size]
            bins[i] = PermutationCrossoverBin(sl)
        return bins

    def set_substract(self, a_arr, b_arr):
        result = []
        for a in a_arr:
            found_in_b = False
            for b in b_arr:
                if b.compare_to(a):
                    found_in_b = True
                    break
            if not found_in_b:
                result.append(a)
        return result

    def inner_cross_over(self, a, b, pstart, pstop):
        ax = self.convert_to_bins(a.genome.bit_string)
        bx = self.convert_to_bins(b.genome.bit_string)

        child = [None] * len(ax)
        child[:pstart] = bx[:pstart]
        child[pstop:] = bx[pstop:]

        added = ax[pstart:pstop]
        removed = bx[pstart:pstop]
        #duplikaty to te ktore sa w dodanych lecz nie w usunietych
        #stracone to te ktore sa w usunietych lecz nie w dodanych
        duplicates = self.set_substract(added, removed)
        lost = self.set_substract(removed, added)

        for i in range(len(duplicates)):
            index = None
            for c in range(len(child)):
                if duplicates[i].compare_to(child[c]):
                    index = c
            child[index] = lost[i]
        
        child[pstart:pstop] = added

        return child

    def cross_over(self,a,b):
        if random.random() > self.pcross:
            return
        pstart, pstop = self.roll_cross_over_points()
        new_a = self.inner_cross_over(a,b,pstart,pstop)
        new_b = self.inner_cross_over(b,a,pstart,pstop)

        a.genome.bit_string = new_a
        b.genome.bit_string = new_b
        



        


    
class Simulation:
    def __init__(self, pop_size, template, fitness_function):
        self.template = template
        self.fitness_function = fitness_function

        self.pop = [None] * pop_size
        self.current_generation = 0
        self.generations = 100
        self.selector = None
        self.mutator = None
        self.crossover_operator = None
        self.monitor = False
        self.monitor_logs = []
        self.monitor_logs_avg = []

    def get_ordered_specimens(self):
        return list(sorted(self.pop, key=lambda x:x.fitness, reverse=True))

    def initialize(self):
        for i in range(len(self.pop)):
            self.pop[i] = Specimen.create_random(self.template)
            self.evaluate(self.pop[i])

    def evaluate(self, specimen):
        fitness = self.fitness_function.evaluate(specimen, 10)
        specimen.fitness = fitness

    def breeding_step(self):
        new_specimen = []
        for specimen in self.pop:
            mating_partner = self.selector.select(self.pop).copy()
            offspring = specimen.copy()
            self.crossover_operator.cross_over(mating_partner, offspring)

            new_specimen.append(offspring)
        
        self.pop = new_specimen

    def mutation_step(self):
        for specimen in self.pop:
            mutated = self.mutator.mutate(specimen, self.current_generation)

    def step(self):
        self.breeding_step()
        self.mutation_step()

        for specimen in self.pop:
            self.evaluate(specimen)

        self.current_generation = self.current_generation + 1

        if self.monitor:
            fitness_arr = list(map(lambda x:x.fitness, self.get_ordered_specimens()))
            fitness_mean = sum(fitness_arr) / len(fitness_arr)

            self.monitor_logs.append(fitness_arr[0])
            self.monitor_logs_avg.append(fitness_mean)


    def run(self):
        while self.current_generation < self.generations:
            self.breeding_step()
            self.mutation_step()

            for specimen in self.pop:
                self.evaluate(specimen)

            self.current_generation = self.current_generation + 1
