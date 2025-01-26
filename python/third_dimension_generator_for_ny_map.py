"""
About: Python generator of the third cost file for the NY city map.
Author: Denis Derkach
Date: Monday, January 27, 2025
"""

import numpy as np
import re
from typing import List, Tuple, Any


def find_first_a_line(lines: List[str]) -> int:
    """
    Finds the index of the first line in the list that starts with "a".

    :param lines: A list of strings representing lines from a file.
    :return: The index of the first line starting with "a", or -1 if not found.
    """
    for index, line in enumerate(lines):
        if line.strip().startswith("a"):
            return index
    return -1


def extract_edges_vertices(file_path: str) -> Tuple[Any, Any]:
    """
    Extracts the number of vertices and edges from a graph file.

    :param file_path: The path to the graph file.
    :return: A tuple containing the number of vertices and edges.
             Returns (None, None) if the information cannot be found.
    """
    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("p sp"):
                match = re.search(r"p sp (\d+) (\d+)", line)
                if match:
                    return int(match.group(1)), int(match.group(2))
    return None, None


def generate_3(orig_file_path: str, new_file_path: str) -> None:
    """
    Generates a new graph file with updated edge weights based on vertex degrees.

    The new weight for each edge is calculated as the average of the degrees of its endpoints.

    :param orig_file_path: The path to the original graph file.
    :param new_file_path: The path where the new graph file will be saved.
    :return: None
    """

    with open(orig_file_path, mode="r") as fres:
        lines = fres.readlines()

    index = find_first_a_line(lines)
    num_ver, num_edges = extract_edges_vertices(orig_file_path)

    temp_lines = np.zeros(num_edges)
    deg_arr = np.zeros(num_ver + 1)

    # Fill temporary lines with edge data
    for i in range(index, len(lines)):
        temp_lines[i - 7] = int(lines[i].split(" ")[1])

    # Calculate degrees of each vertex
    for i in range(1, num_ver):
        deg = int(np.sum(temp_lines == i))
        deg_arr[i] = deg

    # Write new graph file with updated weights
    with open(new_file_path, mode="w") as new_file:
        for i in range(7):
            new_file.write(lines[i])

        for line in lines[7:]:
            match = re.match(r"a (\d+) (\d+) (\d+)", line)
            if match:
                x, y, z = map(int, match.groups())
                new_z = (deg_arr[x] + deg_arr[y]) / 2
                new_line = f"a {x} {y} {new_z}\n"
                new_file.write(new_line)
            else:
                new_file.write(line + "\n")


if __name__ == "__main__":
    # Example of usage
    orig_file_path_example = "../data/USA-road-d.NY.gr"
    new_file_path_example = "../data/USA-road-deg.NY.gr"

    generate_3(orig_file_path=orig_file_path_example, new_file_path=new_file_path_example)
