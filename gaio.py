import geometry

def input_line_to_sqr(line):
    s = line.split()

    return geometry.Square(int(s[0]), int(s[1]))


def prepare_input_data(path):
    f = open(path)
    lines = f.readlines()

    return list(map(input_line_to_sqr, lines))

def write_output_data(input, result, write_path):
    result = result.copy()

    covered_area = sum(map(lambda x: x.area, result))

    output_data = str(covered_area) + "\n"
    for element in input:
        matching_result = next((e for e in result if e.is_equal(element)), None)

        w = element.width
        h = element.height

        if matching_result:
            result.remove(matching_result)
            x = matching_result.x_pos
            y = matching_result.y_pos
            f = matching_result.width != element.width
            output_data += f"{w} {h} {x} {y} {int(f)} \n"
        else:
            output_data += f"{w} {h} -1 -1 0 \n"
    
    f = open(write_path, 'w')
    f.write(output_data)

