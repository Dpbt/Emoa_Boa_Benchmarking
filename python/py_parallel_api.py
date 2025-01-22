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

from python.tests_generator import ny_tests_generator, simple_map_tests_generator


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
    test_results = pd.DataFrame(columns=['test_number', 'algorithm', 'map_name', 'num_dims',
                                         'heuristic_time', 'search_time', 'num_solutions', 'time_limit',
                                         'start', 'goal', 'n_generated', 'n_expanded',
                                         'timeout', 'num_nondom_labels_max', 'num_nondom_labels_avg'])

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
                   'num_solutions': out["num_solutions"]}

        test_results = pd.concat([test_results, pd.DataFrame([new_row])], ignore_index=True)

    return test_results


def parallel_run(tests: list, batch_size: int = 1, n_jobs: int = 1, display_progress: bool = False):

    random.shuffle(tests)

    for i in range(len(tests)):
        tests[i][6] = f"../data_out/technical_txts/simple_map_{i % 11}.txt"

    num_batch = int(len(tests)/batch_size) if len(tests) % batch_size == 0 else int(len(tests)/batch_size) + 1
    tests_with_batch = [tests[i * batch_size : (i + 1) * batch_size] for i in range(num_batch)]

    with Parallel(n_jobs=n_jobs, verbose=11, backend='threading') as parallel:
        results = parallel(delayed(test_system)(test_batch, display_progress=display_progress) for test_batch in tests_with_batch)

    test_results = pd.concat(results, ignore_index=True)

    return test_results



if __name__ == "__main__":
    random.seed(20)
    np.random.seed(20)
    pd.set_option('display.max_columns', None)

    # NY tests
    # tests = ny_tests_generator(num_tests=100)
    # tests = tests[150:200]
    # test_results = parallel_run(tests, batch_size=1, n_jobs=5, display_progress=False)
    # test_results = test_results.sort_values(by=['test_number', 'algorithm'])
    # test_results.to_csv('../data_out/NY_results/NY_test_results_2_2.csv', index=False)
    # print(test_results)

    # Simple maps tests
    """
    num_dims
    3: 30
    4: 15 
    5: 12/13
    6: 10/11
    7: 9/10
    8: 8 мало, 9 много
    9: 8 /10 - 2 теста мимо 
    10: 8
    """
    # tests_params = [
    #     {"num_dims": 3, "width": 30, "height": 30},
    #     {"num_dims": 4, "width": 15, "height": 15},
    #     {"num_dims": 5, "width": 12, "height": 12},
    #     {"num_dims": 6, "width": 10, "height": 10},
    #     {"num_dims": 7, "width": 9, "height": 9},
    #     {"num_dims": 8, "width": 9, "height": 9},
    #     {"num_dims": 9, "width": 8, "height": 8},
    #     {"num_dims": 10, "width": 8, "height": 8},
    # ]
    #
    # for test in tests_params:
    #     for walls_ratio in [0.0, 0.05, 0.10]:
    #         num_dims = test["num_dims"]
    #         width = test["width"]
    #         height = test["height"]
    #         walls_percent = int(walls_ratio * 100)
    #
    #         tests = simple_map_tests_generator(num_tests=50,
    #                                            start=1,
    #                                            finish=width * height,
    #                                            width=width,
    #                                            height=height,
    #                                            num_dims=num_dims,
    #                                            walls=True if walls_percent > 0 else False,
    #                                            walls_ratio=walls_ratio,
    #                                            map_name_local="simple_map",
    #                                            time_limit=600)
    #
    #         test_results = parallel_run(tests, batch_size=1, n_jobs=4, display_progress=False)
    #         test_results = test_results.sort_values(by=['test_number', 'algorithm'])
    #         test_results.to_csv(f'../data_out/simple_map_{num_dims}_results/simple_map_{num_dims}_{walls_percent}.csv', index=False)
    #         print(test_results)




