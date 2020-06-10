import unittest
import rect_fitting
from pkga import Gene, Specimen, PermutationCrossover

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


  





unittest.main()