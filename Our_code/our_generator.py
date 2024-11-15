import numpy as np


def print_matrix_as_cards(matrix):
    max_width = len(str(max(max(row) for row in matrix)))
    border = '+' + '-' * (max_width + 2) + '+'

    for row in matrix:
        print(border * len(row))

        for num in row:
            print(f'|{num:^{max_width + 2}}|', end='')
        print()

    print(border * len(matrix[0]))


def get_neighbors(x: int, y: int, width: int, height: int):
    successors = []
    delta = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for dx, dy in delta:
        new_x = x + dx
        new_y = y + dy

        if 0 <= new_x < width and 0 <= new_y < height:
            successors.append((new_x, new_y))

    return successors


def create_gr_files(weights, width, height, num_dims, weight_range, walls, walls_ratio, num_vertices, num_edges, map_name):
    for i, dictionary in enumerate(weights):
        filename = f"{map_name}_{i + 1}.gr"

        with open(filename, 'w') as file:
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
                   map_name: str = "map.txt"):

    num_edges_1 = ((width - 2) + (height - 2)) * 2 * 3
    num_edges_2 = 4 * 2
    num_edges_3 = (width - 2) * (height - 2) * 4
    num_edges = int((num_edges_1 + num_edges_2 + num_edges_3) / 2)
    # print(num_edges)

    num_vertices = width * height

    if walls:
        walls_list = np.random.choice(range(2, num_vertices - 1), size=round(num_vertices * walls_ratio), replace=False)
    else:
        walls_list = []
    # print(walls_list)

    random_weights = np.random.randint(1, weight_range, size=(num_dims, num_edges))
    # print(random_weights)

    list_of_weights = list({} for _ in range(num_dims))
    curr_edge = 0
    map = list([] for _ in range(height))

    for j in range(height):
        for i in range(width):
            vertex_number = j * width + i + 1

            if vertex_number in walls_list:
                map[j].append("#")
                continue
            map[j].append("*")

            neighbors = get_neighbors(i, j, width, height)
            # print(i, j)
            # print(vertex_number)
            # print(neighbors)

            for new_x, new_y in neighbors:
                new_vertex_number = new_y * width + new_x + 1

                if (vertex_number, new_vertex_number) not in list_of_weights[0] and new_vertex_number not in walls_list:
                    for n in range(num_dims):
                        curr_weight = int(random_weights[n][curr_edge])
                        list_of_weights[n][(vertex_number, new_vertex_number)] = curr_weight
                        list_of_weights[n][(new_vertex_number, vertex_number)] = curr_weight
                        # print(vertex_number, new_vertex_number, n, curr_weight)
                    curr_edge += 1

    num_edges = int(len(list_of_weights[0]) / 2)

    create_gr_files(list_of_weights, width, height, num_dims, weight_range,
                    walls, walls_ratio, num_vertices, num_edges, map_name)

    return list_of_weights, map[::-1]


if __name__ == "__main__":

    lis, map = grid_generator(4, 4, 3, walls=True, walls_ratio=0.2, map_name="../data/example_map")

    # print(*lis, sep='\n')
    print_matrix_as_cards(map)
