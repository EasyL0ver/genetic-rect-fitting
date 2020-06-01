import numpy as np
import random

class GABoolValueTemplate:
    def __init__(self):
        self.bits = 1

    def decode(self, bit_array):
        if len(bit_array) != self.bits:
            raise "Cannot decode, array length mismatch"
        return bool(bit_array[0])
    

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

    def cross_over(self, other):
        index = random.randint(1, len(self.bit_string) - 1)
        tmp = other.bit_string[:index].copy()
        other.bit_string[:index], self.bit_string[:index]  = self.bit_string[:index], tmp

    def __repr__(self):
        return str(self.bit_string)

    def copy(self):
        return Gene(self.bit_string.copy())

    def mutate(self, pmut):
        for i in range(len(self.bit_string)):
            if random.random() < pmut:
                self.bit_string[i] = not self.bit_string[i]

class Specimen:
    def __init__(self, genome, template):
        self.genome = genome
        self.template = template
        self.fitness = 0

    def __repr__(self):
        decoded = self.template.decode(self.genome.bit_string)
        return f"Specimen with fitness:{self.fitness} and value:{decoded}" 

    def mate_with(self, other):
        self.genome.cross_over(other.genome)

    def mutate(self, pmut):
        self.genome.mutate(pmut)

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
            
class FitnessEvaluator:
    def evaluate(self, out, generation):
        return 10


class Simulation:
    def __init__(self, pop_size, template, fitness_function):
        self.template = template
        self.fitness_function = fitness_function

        self.pop = [None] * pop_size
        self.current_generation = 0
        self.generations = 100
        self.selector = None
        self.mutator = None
        self.crossover_rate = 0.6


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
            if random.random() < self.crossover_rate:
                mating_partner = self.selector.select(self.pop).copy()
                offspring = specimen.copy()

                offspring.mate_with(mating_partner) 

                new_specimen.append(offspring)              
            else:
                new_specimen.append(specimen)
        
        self.pop = new_specimen

    def mutation_step(self):
        for specimen in self.pop:
            self.mutator.mutate(specimen, self.current_generation)

            self.evaluate(specimen)

    def run(self):
        while self.current_generation < self.generations:
            self.breeding_step()
            self.mutation_step()

            self.current_generation = self.current_generation + 1
