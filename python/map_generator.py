"""
About: Python module for generating grids with optional walls and random weights,
       and printing them as formatted matrices.
Author: Denis Derkach
"""

import numpy as np
from typing import List, Dict, Tuple


def print_matrix_as_cards(matrix: List[List[str]]) -> None:
    """
    Prints a 2D matrix as cards with borders.

    :param matrix: A 2D list of strings representing the matrix to be printed.
    :return: None
    """
    max_width = len(str(max(max(row) for row in matrix)))
    border = "+" + "-" * (max_width + 2) + "+"

    for row in matrix:
        print(border * len(row))

        for num in row:
            print(f"|{num:^{max_width + 2}}|", end="")
        print()

    print(border * len(matrix[0]))


def get_neighbors(x: int, y: int, width: int, height: int) -> List[Tuple[int, int]]:
    """
    Returns the valid neighboring coordinates of a cell in a grid.

    :param x: The x-coordinate of the cell.
    :param y: The y-coordinate of the cell.
    :param width: The width of the grid.
    :param height: The height of the grid.
    :return: A list of tuples representing the coordinates of valid neighbors.
    """
    successors = []
    delta = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for dx, dy in delta:
        new_x = x + dx
        new_y = y + dy

        if 0 <= new_x < width and 0 <= new_y < height:
            successors.append((new_x, new_y))

    return successors


def create_gr_files(weights: List[Dict[Tuple[int, int], int]],
                    width: int,
                    height: int,
                    num_dims: int,
                    weight_range: int,
                    walls: bool,
                    walls_ratio: float,
                    num_vertices: int,
                    num_edges: int,
                    map_name: str) -> None:
    """
    Creates .gr files for each dimension of the generated graph.

    :param weights: A list of dictionaries containing edge weights for each dimension.
    :param width: The width of the grid.
    :param height: The height of the grid.
    :param num_dims: The number of dimensions (weight sets).
    :param weight_range: The range of weights for edges.
    :param walls: Indicates if walls are present in the grid.
    :param walls_ratio: The ratio of walls to total vertices.
    :param num_vertices: Total number of vertices in the graph.
    :param num_edges: Total number of edges in the graph.
    :param map_name: The base name for the generated files.
    :return: None
    """
    for i, dictionary in enumerate(weights):
        filename = f"{map_name}_{i + 1}.gr"

        with open(filename, "w") as file:
            file.write("c Generated map\n")
            file.write(
                f"c Size: {width} * {height}, weights in range: 1 to {weight_range - 1}, walls: {walls}, with ratio {walls_ratio}\n")
            file.write(f"c dim {i + 1} of {num_dims}\n")
            file.write("c\n")
            file.write(f"p sp {num_vertices} {num_edges}\n")
            file.write(f"c graph contains {num_vertices} nodes and {num_edges} arcs\n")
            file.write("c\n")

            for (x, y), z in dictionary.items():
                file.write(f"a {x} {y} {z}\n")


def grid_generator(width: int = 10,
                   height: int = 10,
                   num_dims: int = 3,
                   weight_range: int = 11,
                   walls: bool = False,
                   walls_ratio: float = 0.2,
                   map_name: str = "map.txt") -> List[List[str]]:
    """
    Generates a grid with optional walls and random weights.

    :param width: The width of the grid.
    :param height: The height of the grid.
    :param num_dims: The number of dimensions (weight sets).
    :param weight_range: The range of weights for edges.
    :param walls: Indicates if walls should be included in the generated map.
    :param walls_ratio: The ratio of walls to total vertices in the generated map.
    :param map_name: The base name for generated .gr files.
    :return: A 2D list representing the generated grid.
    """

    # Calculate number of edges based on dimensions
    num_edges_1 = ((width - 2) + (height - 2)) * 2 * 3
    num_edges_2 = 4 * 2
    num_edges_3 = (width - 2) * (height - 2) * 4
    num_edges = int((num_edges_1 + num_edges_2 + num_edges_3) / 2)

    num_vertices = width * height

    # Generate wall positions if required
    if walls:
        walls_list = np.random.choice(range(2, num_vertices - 1), size=round(num_vertices * walls_ratio), replace=False)
    else:
        walls_list = []

    # Generate random weights
    random_weights = np.random.randint(1, weight_range, size=(num_dims, num_edges))

    list_of_weights = [{} for _ in range(num_dims)]

    curr_edge = 0
    generated_map = [[] for _ in range(height)]

    # Populate the grid and generate weights
    for j in range(height):
        for i in range(width):
            vertex_number = j * width + i + 1

            if vertex_number in walls_list:
                generated_map[j].append("#")
                continue

            generated_map[j].append("*")

            neighbors = get_neighbors(i, j, width, height)

            for new_x, new_y in neighbors:
                new_vertex_number = new_y * width + new_x + 1

                if (vertex_number, new_vertex_number) not in list_of_weights[0] and new_vertex_number not in walls_list:
                    for n in range(num_dims):
                        curr_weight = int(random_weights[n][curr_edge])
                        list_of_weights[n][(vertex_number, new_vertex_number)] = curr_weight
                        list_of_weights[n][(new_vertex_number, vertex_number)] = curr_weight
                    curr_edge += 1

    num_edges = int(len(list_of_weights[0]) / 2)

    create_gr_files(list_of_weights, width, height, num_dims, weight_range,
                    walls, walls_ratio, num_vertices, num_edges, map_name)

    return generated_map[::-1]


if __name__ == "__main__":
    # Example of usage
    generated_map = grid_generator(15, 15, 3,
                                   walls=True,
                                   walls_ratio=0.2,
                                   map_name="../data/generated_maps/generation_example_map/example_map")

    print_matrix_as_cards(generated_map)
