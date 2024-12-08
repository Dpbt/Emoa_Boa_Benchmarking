"""
About: python helper APIs
Author: Zhongqiang (Richard) Ren and Denis Derkach
"""
import random
import numpy as np
import subprocess
import pandas as pd
from tqdm import tqdm
from joblib import Parallel, delayed
import time

from Our_code.NY_tests_generator import ny_tests_generator


def getResult(res_file: str):
    """
    """
    res_dict = dict()
    with open(res_file, mode="r") as fres:
        lines = fres.readlines()
        temp = lines[1].split(':')
        res_dict["n_generated"] = int(temp[1])
        temp = lines[2].split(':')
        res_dict["n_expanded"] = int(temp[1])
        temp = lines[3].split(':')
        res_dict["n_domCheck"] = int(temp[1])
        temp = lines[4].split(':')
        res_dict["rt_initHeu"] = float(temp[1])
        temp = lines[5].split(':')
        res_dict["rt_search"] = float(temp[1])
        temp = lines[6].split(':')
        res_dict["timeout"] = int(temp[1])
        temp = lines[7].split(':')
        res_dict["num_nondom_labels_max"] = float(temp[1])
        temp = lines[8].split(':')
        res_dict["num_nondom_labels_avg"] = float(temp[1])
        temp = lines[9].split(':')
        res_dict["num_solutions"] = int(temp[1])

        start_idx = 10
        res_dict["paths"] = dict()
        res_dict["costs"] = dict()
        for i in range(res_dict['num_solutions']):
            # sol ID
            temp = lines[start_idx+3*i].split(":")
            solID = int(temp[1])
            # cost vector
            temp = lines[start_idx+3*i+1].split(",")
            cvec = list()
            cvec.append( int(float(temp[0][1:])))
            for j in range(1,len(temp)-1):
                cvec.append(int(float(temp[j])))
            res_dict["costs"][solID] = np.array(cvec)
            # path
            temp = lines[start_idx+3*i+2].split(' ')
            res_dict["paths"][solID] = list(map(int, list(temp[:-1])))
    return res_dict


def run_algorithm(cg_list: list, exe_path: str, res_path: str, vo: int, vd: int, tlimit: int):
    """
    """
    cmd = [str(vo), str(vd), str(tlimit), str(len(cg_list))] + cg_list
    cmd.append(res_path)

    cmd_s = ' '.join(cmd)

    cmd = ["C:\\Program Files\\Git\\bin\\bash.exe",
           "-c",
           f"C:/Users/denis/CLionProjects/Emoa_heu/cmake-build-debug/{exe_path} " + cmd_s]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.wait()
    out = getResult(res_path)

    return out


def test_system(tests: list, display_progress: bool = False):
    exp_num = 0
    test_results = pd.DataFrame(columns=['test_number', 'algorithm', 'map_name', 'num_dims', 'time_limit',
                                         'start', 'goal', 'n_generated', 'n_expanded',
                                         'heuristic_time', 'search_time', 'timeout', 'num_nondom_labels_max',
                                         'num_nondom_labels_avg', 'num_solutions',
                                         'solutions_labels'])

    if display_progress:
        iterator = tqdm(tests, desc="Выполнение тестов")
    else:
        iterator = tests

    for test in iterator:
        exp_num += 1

        test_number, algorithm, map_name, time_limit, start, goal, result_file, maps = test

        if algorithm == "emoa":
            exe_path = "run_emoa.exe"
        elif algorithm == "boa":
            exe_path = "run_boalex.exe"
        else:
            raise ValueError("Error: no such algorithm")

        out = run_algorithm(cg_list=maps,
                            exe_path=exe_path,
                            res_path=result_file,
                            vo=start,
                            vd=goal,
                            tlimit=time_limit)

        new_row = {'test_number': test_number,
                   'algorithm': algorithm,
                   'map_name': map_name,
                   'num_dims': len(maps),
                   'time_limit': time_limit,
                   'start': start,
                   'goal': goal,
                   'n_generated': out["n_generated"],
                   'n_expanded': out["n_expanded"],
                   'heuristic_time': out["rt_initHeu"],
                   'search_time': out["rt_search"],
                   'timeout': out["timeout"],
                   'num_nondom_labels_max': out["num_nondom_labels_max"],
                   'num_nondom_labels_avg': out["num_nondom_labels_avg"],
                   'num_solutions': out["num_solutions"],
                   'solutions_labels': out["paths"].keys()}

        test_results = pd.concat([test_results, pd.DataFrame([new_row])], ignore_index=True)

    return test_results


def parallel_run(tests: list, batch_size: int = 1, n_jobs: int = 1, display_progress: bool = False):

    random.shuffle(tests)

    num_batch = int(len(tests)/batch_size) if len(tests) % batch_size == 0 else int(len(tests)/batch_size) + 1
    tests_with_batch = [tests[i * batch_size : (i + 1) * batch_size] for i in range(num_batch)]

    with Parallel(n_jobs=n_jobs, verbose=11, backend='threading') as parallel:
        results = parallel(delayed(test_system)(test_batch, display_progress=display_progress) for test_batch in tests_with_batch)

    test_results = pd.concat(results, ignore_index=True)

    return test_results



if __name__ == "__main__":
    random.seed(20)
    pd.set_option('display.max_columns', None)

    # tests = [["emoa", "NY", 600, 1, 5000, "../data_out/NY-result.txt",
    #           ["../data/USA-road-d.NY.gr", "../data/USA-road-t.NY.gr", "../data/USA-road-deg.NY.gr"]],
    #          ["emoa", "NY", 600, 2, 6000, "../data_out/NY-result.txt",
    #           ["../data/USA-road-d.NY.gr", "../data/USA-road-t.NY.gr", "../data/USA-road-deg.NY.gr"]],
    #          ["emoa", "NY", 600, 1, 3000, "../data_out/NY-result.txt",
    #           ["../data/USA-road-d.NY.gr", "../data/USA-road-t.NY.gr", "../data/USA-road-deg.NY.gr"]],
    #          ["emoa", "NY", 600, 100, 6500, "../data_out/NY-result.txt",
    #           ["../data/USA-road-d.NY.gr", "../data/USA-road-t.NY.gr", "../data/USA-road-deg.NY.gr"]],
    #          ["emoa", "NY", 600, 4, 5500, "../data_out/NY-result.txt",
    #           ["../data/USA-road-d.NY.gr", "../data/USA-road-t.NY.gr", "../data/USA-road-deg.NY.gr"]],]
    #
    # tests = [[1, "emoa", "NY", 600, 1, 5000, "../data_out/NY-result.txt",
    #           ["../data/USA-road-d.NY.gr", "../data/USA-road-t.NY.gr", "../data/USA-road-deg.NY.gr"]],
    #          [1, "boa", "NY", 600, 1, 5000, "../data_out/NY-result.txt",
    #           ["../data/USA-road-d.NY.gr", "../data/USA-road-t.NY.gr", "../data/USA-road-deg.NY.gr"]]]

    tests = ny_tests_generator(num_tests=50)

    test_results = parallel_run(tests[80:100], batch_size=1, n_jobs=5, display_progress=False)
    test_results.to_csv('../data_out/NY_test_results_3.csv', index=False)
    print(test_results)

