import unittest
import rect_fitting
from pkga import Gene, Specimen, PermutationCrossover
import pkga as ga
from rect_fitting import PermutationSquareInitializer

class TestPermutationCrossOver(unittest.TestCase):
    def byte_array(self, size, int_array):
        format = '{:0' + str(size) + 'b}'
        specimen_arr = [None] * (len(int_array) * size)

        w_index = 0
        for i in range(len(int_array)):
            bitnum = [bool(int(x)) for x in format.format(int_array[i])]
            for bit in bitnum:
                specimen_arr[w_index] = bit
                w_index += 1

        return specimen_arr

    def int_array(self, size, byte_array):
        ints = []
        for i in range(0, len(byte_array) , size):
            slc = byte_array[i:i+size]
            out = 0
            for bit in slc:
                out = (out << 1) | bit
            ints.append(out)
        return ints

    def test_byte_array(self):
        out = self.byte_array(2, [3,1,0,2])
        expected = [True, True, False, True, False, False, True, False]

        self.assertListEqual(out, expected)

    def test_int_array(self):
        out = self.int_array(2, [True, True, False, True, False, False, True, False])
        expected = [3,1,0,2]

        self.assertListEqual(out, expected)


    def test_middle_crossover(self):
        arr_a = [False, False, False, True, True, True, True, False]
        arr_b = [True, True, False, False, False, True, True, False]
        g_a = Gene(arr_a)
        g_b = Gene(arr_b)
        s_a = Specimen(g_a, None)
        s_b = Specimen(g_b, None)
        cross = PermutationCrossover(1, 2, 4)

        expected_a = [False,False, False, True, True, True, True, False]

        cross.inner_cross_over(s_a, s_b, 1, 3)

        self.assertListEqual(expected_a, s_a.genome.bit_string)

    def test_zero_crossover(self):
        s_a = Specimen(Gene(self.byte_array(2, [0,2,3,1])), None)
        s_b = Specimen(Gene(self.byte_array(2, [3,2,0,1])), None)

        cross = PermutationCrossover(1, 2, 4)
        cross.inner_cross_over(s_a, s_b, 1, 4)

        e_a = [0,2,3,1]

        self.assertListEqual(s_a.genome.bit_string, self.byte_array(2,e_a))

    def test_too_large_size(self):
        s_a = Specimen(Gene(self.byte_array(9, [0,2,3,1])), None)
        s_b = Specimen(Gene(self.byte_array(9, [3,2,0,1])), None)

        cross = PermutationCrossover(1, 2, 4)
        cross.inner_cross_over(s_a, s_b, 1, 4)

        e_a = [0,2,3,1]

        self.assertListEqual(s_a.genome.bit_string, self.byte_array(9,e_a))


class TestSpecimenInitialization(unittest.TestCase):
    def create_template(self, count, bits):
        solution_template = ga.GAMultiValueTemplate()
        max_val = pow(2, bits)
        for i in range(count):
            order_value = ga.GAIntegerValueTemplate(0, max_val, bits)
            flip_value = ga.GABoolValueTemplate()
            square_template = ga.GAMultiValueTemplate()
            square_template.add_value("sqr_id", order_value)
            square_template.add_value("flip", flip_value)
            solution_template.add_value(i, square_template)

        return solution_template
    def create_specimen(self, count, bits):
        a = PermutationSquareInitializer(count, bits)
        t = self.create_template(count, bits)
        s = a.create_specimen(t)
        return s

    def run_count(self, count, bits):
        s = self.create_specimen(count, bits)
        t = self.create_template(count, bits)
        b = s.genome.bit_string
        values = t.decode(s.genome.bit_string)
        numerical = list(map(lambda x: x[1]['sqr_id'], values.items()))
        numerical = sorted(numerical)

        for i in range(count):
            self.assertEqual(i, numerical[i])


    def test_permutations_valid(self):
        self.run_count(4, 3)

    def string_with_fixed_random_values(self, p, f, c):
        a = PermutationSquareInitializer(c,3)
        return a.generate_string(p, f)

    def test_fixed_vals(self):
        p = [2,3,0,1]
        f = [True, True, True, False]
        expected = [False, True, False, True, False, True, True, True, False, False, False, True, False, False, True, False ]

        res = self.string_with_fixed_random_values(p,f,4)

        self.assertListEqual(res, expected)

    def test_fixed_vals2(self):
        p = [4,2,3,0,1]
        f = [False, False, False, False, False]
        exp = [True, False, False, False, False, True, False, False, False, True, True, False, False, False, False, False, False, False, True, False]

        res = self.string_with_fixed_random_values(p,f,5)

        self.assertListEqual(res, exp)

    def test_template_decoding(self):
        p = [2,3,0,1]
        f = [True, True, True, False]
        expected = [False, True, False, True, False, True, True, True, False, False, False, True, False, False, True, False ]

        template = self.create_template(4, 3)

        result = template.decode(expected)
        numerical = list(map(lambda x: x[1]['sqr_id'], result.items()))

        self.assertListEqual(p, numerical)

    def test_template_decoding2(self):
        p = [4,2,3,0,1]
        f = [False, False, False, False, False]
        exp = [True, False, False, False, False, True, False, False, False, True, True, False, False, False, False, False, False, False, True, False]

        template = self.create_template(5, 3)

        result = template.decode(exp)
        numerical = list(map(lambda x: x[1]['sqr_id'], result.items()))

        self.assertListEqual(p, numerical)





#a = TestSpecimenInitialization()
#a.test_template_decoding2()

unittest.main()