import random

def ny_tests_generator(num_tests: int = 50,
                       left_vertex_boundary: int = 1,
                       right_vertex_boundary: int = 264346,
                       time_limit: int = 600):
    tests = []

    for exp_number in range(1, num_tests + 1):
        first_vertex = random.randint(left_vertex_boundary, right_vertex_boundary)
        second_vertex = random.randint(left_vertex_boundary, right_vertex_boundary)

        emoa_test = [exp_number, "emoa", "NY", time_limit, first_vertex, second_vertex,
                     "../data_out/NY-result.txt",
                     ["../data/USA-road-d.NY.gr", "../data/USA-road-t.NY.gr", "../data/USA-road-deg.NY.gr"]]

        boa_test = [exp_number, "boa", "NY", time_limit, first_vertex, second_vertex,
                    "../data_out/NY-result.txt",
                    ["../data/USA-road-d.NY.gr", "../data/USA-road-t.NY.gr", "../data/USA-road-deg.NY.gr"]]

        tests.append(emoa_test)
        tests.append(boa_test)

    return tests


if __name__ == "__main__":
    tests_array = ny_tests_generator()
    for test in tests_array:
        print(test)