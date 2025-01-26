"""
About: Python generator for test cases of graph algorithms using NY city map and simple maps
Author: Denis Derkach
"""

import random
from python.map_generator import grid_generator
from typing import List, Any


def ny_tests_generator(num_tests: int = 50,
                       left_vertex_boundary: int = 1,
                       right_vertex_boundary: int = 264346,
                       time_limit: int = 600) -> List[List[Any]]:
    """
    Generates a list of test cases for the NY graph.

    Each test case consists of two entries (for EMOA and BOA algorithms) with randomly selected vertices.

    :param num_tests: The number of test cases to generate.
    :param left_vertex_boundary: The minimum vertex index.
    :param right_vertex_boundary: The maximum vertex index.
    :param time_limit: The time limit for each test case in seconds.
    :return: A list of test cases, where each test case is a list containing information about the test.
    """
    tests = []

    for exp_number in range(1, num_tests + 1):
        first_vertex = random.randint(left_vertex_boundary, right_vertex_boundary)
        second_vertex = random.randint(left_vertex_boundary, right_vertex_boundary)

        emoa_test = [exp_number, "emoa", "NY", time_limit, first_vertex, second_vertex,
                     ["../data/USA-road-d.NY.gr", "../data/USA-road-t.NY.gr", "../data/USA-road-deg.NY.gr"]]

        boa_test = [exp_number, "boa", "NY", time_limit, first_vertex, second_vertex,
                    ["../data/USA-road-d.NY.gr", "../data/USA-road-t.NY.gr", "../data/USA-road-deg.NY.gr"]]

        tests.append(emoa_test)
        tests.append(boa_test)

    return tests


def simple_map_tests_generator(num_tests: int = 50,
                               start: int = 1,
                               finish: int = 225,
                               width: int = 15,
                               height: int = 15,
                               num_dims: int = 3,
                               walls: bool = False,
                               walls_ratio: float = 0.0,
                               map_name_local: str = "example_map",
                               time_limit: int = 600) -> List[List[Any]]:
    """
    Generates a list of test cases for simple maps.

    Each test case consists of two entries (for EMOA and BOA algorithms) using generated maps.

    :param num_tests: The number of test cases to generate.
    :param start: The starting vertex index for the tests.
    :param finish: The finishing vertex index for the tests.
    :param width: The width of the generated map.
    :param height: The height of the generated map.
    :param num_dims: The number of dimensions (weight sets) in the generated map.
    :param walls: Indicates if walls should be included in the generated map.
    :param walls_ratio: The ratio of walls to total vertices in the generated map.
    :param map_name_local: The base name for the generated maps.
    :param time_limit: The time limit for each test case in seconds.
    :return: A list of test cases, where each test case is a list containing information about the test.
    """

    tests = []
    walls_percent = int(walls_ratio * 100)

    for exp_number in range(1, num_tests + 1):
        map_name = f"../data/generated_maps/{num_dims}_dims/{walls_percent}_walls_ratio/{map_name_local}_{num_dims}_{width}_{height}_{walls_percent}_{exp_number}"

        _ = grid_generator(width=width,
                           height=height,
                           num_dims=num_dims,
                           walls=walls,
                           walls_ratio=walls_ratio,
                           map_name=map_name)

        map_names_list = [f"{map_name}_{dim}.gr" for dim in range(1, num_dims + 1)]

        emoa_test = [exp_number, "emoa", f"simple map {num_dims} dims", time_limit, start, finish,
                     map_names_list]

        boa_test = [exp_number, "boa", f"simple map {num_dims} dims", time_limit, start, finish,
                    map_names_list]

        tests.append(emoa_test)
        tests.append(boa_test)

    return tests


if __name__ == "__main__":
    # Example of usage
    tests_array = simple_map_tests_generator(num_tests=2,
                                             start=1,
                                             finish=225,
                                             width=15,
                                             height=15,
                                             num_dims=4,
                                             walls=False,
                                             walls_ratio=0.2,
                                             map_name_local="simple_map",
                                             time_limit=600)

    for test in tests_array:
        print(test)
