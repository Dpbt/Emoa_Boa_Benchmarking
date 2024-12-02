"""
About: python helper APIs
Author: Zhongqiang (Richard) Ren and Denis Derkach
"""

from sys import stdout
import numpy as np
import sys
import subprocess
import pandas as pd
from IPython.display import Image as Img, display
from ipywidgets import IntProgress
from tqdm import tqdm
from joblib import Parallel, delayed
import time


def getResult(res_file):
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


def runEMOA(cg_list, data_folder, exe_path, res_path, vo, vd, tlimit):
    """
    """
    # print("[INFO] runEMOA (python) vo =", vo, ", vd =", vd, ", tlimit =", tlimit, ", M =", len(cg_list))

    cmd = [exe_path, str(vo), str(vd), str(tlimit), str(len(cg_list))] + cg_list
    cmd.append(res_path)

    cmd_s = ' '.join(cmd[1:])

    # cmd = ["C:\\Program Files\\Git\\bin\\bash.exe",
    #        "-c",
    #        "cd /c/Users/denis/CLionProjects/public_emoa_git/cmake-build-debug && ./run_emoa.exe " + cmd_s]

    # cmd = ["C:\\Program Files\\Git\\bin\\bash.exe",
    #        "-c",
    #        "../cmake-build-debug/run_emoa.exe " + cmd_s]

    cmd = ["C:\\Program Files\\Git\\bin\\bash.exe",
           "-c",
           "C:/Users/denis/CLionProjects/Emoa_heu/cmake-build-debug/run_emoa.exe " + cmd_s]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    process.wait()
    # print("[INFO] runEMOA (python) invoke c++ bin finished..." )

    out = getResult(res_path)

    return out

def runBOA(cg_list, data_folder, exe_path, res_path, vo, vd, tlimit):
    """
    """
    cmd = [exe_path, str(vo), str(vd), str(tlimit), str(len(cg_list))] + cg_list
    cmd.append(res_path)

    cmd_s = ' '.join(cmd[1:])

    # cmd = ["C:\\Program Files\\Git\\bin\\bash.exe",
    #        "-c",
    #        "cd /c/Users/denis/CLionProjects/public_emoa_git/cmake-build-debug && ./run_emoa.exe " + cmd_s]

    # cmd = ["C:\\Program Files\\Git\\bin\\bash.exe",
    #        "-c",
    #        "../cmake-build-debug/run_emoa.exe " + cmd_s]

    cmd = ["C:\\Program Files\\Git\\bin\\bash.exe",
           "-c",
           "C:/Users/denis/CLionProjects/Emoa_heu/cmake-build-debug/run_boa.exe " + cmd_s]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    process.wait()
    # print("[INFO] runEMOA (python) invoke c++ bin finished..." )

    out = getResult(res_path)

    return out


def test_emoa(tests: list, display_progress: bool = False):
    exp_num = 0
    test_results = pd.DataFrame(columns=['algorithm', 'map_name', 'num_dims', 'time_limit',
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

        algorithm, map_name, time_limit, start, goal, result_file, maps = test

        if algorithm == "emoa":
            out = runEMOA(cg_list=maps,
                          data_folder="../data/",
                          exe_path="../cmake-build-debug/run_emoa.exe",
                          res_path=result_file,
                          vo=start,
                          vd=goal,
                          tlimit=time_limit)
        elif algorithm == "boa":
            out = runBOA(cg_list=maps,
                          data_folder="../data/",
                          exe_path="../cmake-build-debug/run_boa.exe",
                          res_path=result_file,
                          vo=start,
                          vd=goal,
                          tlimit=time_limit)
        else:
            print("Error: no such algorithm")

        new_row = {'algorithm': algorithm,
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

    num_batch = int(len(tests)/batch_size) if len(tests) % batch_size == 0 else int(len(tests)/batch_size) + 1
    tests_with_batch = [tests[i * batch_size : (i + 1) * batch_size] for i in range(num_batch)]

    with Parallel(n_jobs=n_jobs, verbose=10, backend='threading') as parallel:
        results = parallel(delayed(test_emoa)(test_batch, display_progress=display_progress) for test_batch in tests_with_batch)

    test_results = pd.concat(results, ignore_index=True)

    return test_results



if __name__ == "__main__":
    pd.set_option('display.max_columns', None)

    tests = [["emoa", "NY", 600, 1, 5000, "../data_out/NY-result.txt",
               ["../data/USA-road-d.NY.gr", "../data/USA-road-t.NY.gr", "../data/USA-road-deg.NY.gr"]],
             ["emoa", "NY", 600, 2, 6000, "../data_out/NY-result.txt",
               ["../data/USA-road-d.NY.gr", "../data/USA-road-t.NY.gr", "../data/USA-road-deg.NY.gr"]],
             ["emoa", "NY", 600, 1, 3000, "../data_out/NY-result.txt",
               ["../data/USA-road-d.NY.gr", "../data/USA-road-t.NY.gr", "../data/USA-road-deg.NY.gr"]],
             ["emoa", "NY", 600, 100, 6500, "../data_out/NY-result.txt",
               ["../data/USA-road-d.NY.gr", "../data/USA-road-t.NY.gr", "../data/USA-road-deg.NY.gr"]],
             ["emoa", "NY", 600, 4, 5500, "../data_out/NY-result.txt",
               ["../data/USA-road-d.NY.gr", "../data/USA-road-t.NY.gr", "../data/USA-road-deg.NY.gr"]],]

    tests = [["emoa", "NY", 600, 1, 5000, "../data_out/NY-result.txt",
              ["../data/USA-road-d.NY.gr", "../data/USA-road-t.NY.gr", "../data/USA-road-deg.NY.gr"]],
             ["boa", "NY", 600, 1, 5000, "../data_out/NY-result.txt",
              ["../data/USA-road-d.NY.gr", "../data/USA-road-t.NY.gr", "../data/USA-road-deg.NY.gr"]]]

    start_time = time.time()

    test_results = parallel_run(tests, batch_size=1, n_jobs=5, display_progress=False)

    end_time = time.time()

    print()
    print("Runtime:", end_time - start_time)

    test_results.to_csv('../data_out/NY_test_results.csv', index=False)

    print(test_results)

