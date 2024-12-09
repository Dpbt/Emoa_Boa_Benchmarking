"""
About: python generator of third cost file for NY city map
Author: Denis Derkach
"""

import numpy as np
import re


def find_first_a_line(lines):
    for index, line in enumerate(lines):
        if line.strip().startswith('a'):
            return index
    return -1


def extract_edges_vertices(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('p sp'):
                match = re.search(r'p sp (\d+) (\d+)', line)
                if match:
                    return int(match.group(1)), int(match.group(2))
    return None, None


def generate_3(orig_file_path, new_file_path):

    with open(orig_file_path, mode="r") as fres:
        lines = fres.readlines()

    index = find_first_a_line(lines)
    num_ver, num_edges = extract_edges_vertices(orig_file_path)

    temp_lines = np.zeros(num_edges)
    deg_arr = np.zeros(num_ver + 1)

    for i in range(index, len(lines)):
        temp_lines[i - 7] = int(lines[i].split(" ")[1])

    for i in range(1, num_ver):
        deg = int(np.sum(temp_lines == i))
        deg_arr[i] = deg

    with open(new_file_path, mode="w") as new_file:
        for i in range(7):
            new_file.write(lines[i])

        for line in lines[7:]:
            match = re.match(r'a (\d+) (\d+) (\d+)', line)
            if match:
                x, y, z = map(int, match.groups())
                new_z = (deg_arr[x] + deg_arr[y]) / 2
                new_line = f'a {x} {y} {new_z}\n'
                new_file.write(new_line)
            else:
                new_file.write(line + '\n')


if __name__ == '__main__':

    orig_file_path = "../data/USA-road-d.NY.gr"
    new_file_path = "../data/USA-road-deg.NY.gr"

    generate_3(orig_file_path, new_file_path)


