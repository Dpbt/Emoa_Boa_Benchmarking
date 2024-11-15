"""
About: python helper APIs
Author: Zhongqiang (Richard) Ren
"""
from sys import stdout

import numpy as np
import sys
import subprocess
import pandas as pd


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


def getResult_stdout(res_str_stdout):

    num_nodes = int(res_str_stdout.split("num_nodes: ")[1].split()[0])
    num_edges = int(res_str_stdout.split("num_edges: ")[1].split()[0])
    heuristic_time = float(res_str_stdout.split("solutions in ")[1].split("(for heu)")[0])
    search_time = float(res_str_stdout.split("(for heu) + ")[1].split("(for search)")[0])

    result_dict = {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "heuristic_time": heuristic_time,
        "search_time": search_time,
    }

    return result_dict


def runEMOA(cg_list, data_folder, exe_path, res_path, vo, vd, tlimit):
    """
    """
    print("[INFO] runEMOA (python) vo =", vo, ", vd =", vd, ", tlimit =", tlimit, ", M =", len(cg_list) )

    # run EMOA*.
    cmd = [exe_path, str(vo), str(vd), str(tlimit), str(len(cg_list))] + cg_list
    cmd.append(res_path)

    cmd_s = ' '.join(cmd[1:])

    cmd = ["C:\\Program Files\\Git\\bin\\bash.exe",
           "-c",
           "cd /c/Users/denis/CLionProjects/public_emoa_git/cmake-build-debug && ./run_emoa.exe " + cmd_s]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    stdout = process.communicate()
    stdout = stdout[0].decode()
    stdout = getResult_stdout(stdout)

    # Print output and errors
    # print()
    # print("1111111111111111111111111111111111")
    # print(stdout[0].decode(), "1111111111111111111111111111111111")
    # print()

    process.wait() # otherwise, subprocess run concurrently...
    print("[INFO] runEMOA (python) invoke c++ bin finished..." )

    out = getResult(res_path)

    return out, stdout


def test_emoa(tests: list):
    exp_num = 0
    test_results = pd.DataFrame(columns=['map_name', 'num_nodes', 'num_edges', 'num_dims', 'time_limit',
                                         'start', 'goal', 'n_generated', 'n_expanded',
                                         'rt_initHeu', 'rt_search', 'timeout', 'num_nondom_labels_max',
                                         'num_nondom_labels_avg', 'num_solutions',
                                         'solutions_labels', 'heuristic_time', 'search_time'])

    for test in tests:
        exp_num += 1

        map_name, time_limit, start, goal, result_file, maps = test

        out, stdout = runEMOA(cg_list=maps,
                              data_folder="../data/",
                              exe_path="../cmake-build-debug/run_emoa.exe",
                              res_path=result_file,
                              vo=start,
                              vd=goal,
                              tlimit=time_limit)

        new_row = {'map_name': map_name,
                   'num_nodes': stdout["num_nodes"],
                   'num_edges': stdout["num_edges"],
                   'num_dims': len(maps),
                   'time_limit': time_limit,
                   'start': start,
                   'goal': goal,
                   'n_generated': out["n_generated"],
                   'n_expanded': out["n_expanded"],
                   'rt_initHeu': out["rt_initHeu"],
                   'rt_search': out["rt_search"],
                   'timeout': out["timeout"],
                   'num_nondom_labels_max': out["num_nondom_labels_max"],
                   'num_nondom_labels_avg': out["num_nondom_labels_avg"],
                   'num_solutions': out["num_solutions"],
                   'solutions_labels': out["paths"].keys(),
                   'heuristic_time': stdout["heuristic_time"],
                   'search_time': stdout["search_time"]}

        test_results = pd.concat([test_results, pd.DataFrame([new_row])], ignore_index=True)

    return test_results





if __name__ == "__main__":

    grs = ["../data/ex1-c1.gr", "../data/ex1-c2.gr", "../data/ex1-c3.gr"]

    # runEMOA(["../data/ex1-c1.gr", "../data/ex1-c2.gr", "../data/ex1-c3.gr"],
    #         "../data/",
    #         "../cmake-build-debug/run_emoa.exe",
    #         "../data/temp-res.txt",
    #         1, 5, 60)

    # out, stdout = runEMOA(["../data/USA-road-d.NY.gr", "../data/USA-road-t.NY.gr"],
    #         "../data/",
    #         "../cmake-build-debug/run_emoa.exe",
    #         "../data/NY-result.txt",
    #         1, 100, 600)
    #
    # print(out)
    #
    # print(out["paths"].keys())
    #
    # print(stdout)
    #
    # print(stdout["search_time"])

    pd.set_option('display.max_columns', None)

    tests = [["NY", 600, 1, 100, "../data/NY-result.txt", ["../data/USA-road-d.NY.gr", "../data/USA-road-t.NY.gr"]]]

    test_results = test_emoa(tests)

    print(test_results)

