import random
from python.map_generator import grid_generator

def ny_tests_generator(num_tests: int = 50,
                       left_vertex_boundary: int = 1,
                       right_vertex_boundary: int = 264346,
                       time_limit: int = 600):
    tests = []

    for exp_number in range(1, num_tests + 1):
        first_vertex = random.randint(left_vertex_boundary, right_vertex_boundary)
        second_vertex = random.randint(left_vertex_boundary, right_vertex_boundary)

        emoa_test = [exp_number, "emoa", "NY", time_limit, first_vertex, second_vertex,
                     "../data_out/technical_txts/NY_results.txt",
                     ["../data/USA-road-d.NY.gr", "../data/USA-road-t.NY.gr", "../data/USA-road-deg.NY.gr"]]

        boa_test = [exp_number, "boa", "NY", time_limit, first_vertex, second_vertex,
                    "../data_out/technical_txts/NY_results.txt",
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
                               time_limit: int = 600):

    tests = []
    walls_percent = int(walls_ratio * 100)

    for exp_number in range(1, num_tests + 1):

        map_name = f"../data/generated_maps/{num_dims}_dims/{walls_percent}_walls_ratio/{map_name_local}_{num_dims}_{width}_{height}_{walls_percent}_{exp_number}"

        _, _ = grid_generator(width=width,
                              height=height,
                              num_dims=num_dims,
                              walls=walls,
                              walls_ratio=walls_ratio,
                              map_name=map_name)

        map_names_list = []

        for dim in range(1, num_dims + 1):
            map_names_list.append(map_name+f"_{dim}.gr")

        emoa_test = [exp_number, "emoa", f"simple map {num_dims} dims", time_limit, start, finish,
                     f"../data_out/technical_txts/simple_map_{num_dims}.txt", map_names_list]

        boa_test = [exp_number, "boa", f"simple map {num_dims} dims", time_limit, start, finish,
                    f"../data_out/technical_txts/simple_map_{num_dims}.txt", map_names_list]

        tests.append(emoa_test)
        tests.append(boa_test)

    return tests

if __name__ == "__main__":
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

