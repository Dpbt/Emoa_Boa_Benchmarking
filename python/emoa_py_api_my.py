"""
About: python helper APIs
Author: Zhongqiang (Richard) Ren
"""

import numpy as np
import sys
import subprocess


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
        temp = lines[6].split(":")
        res_dict['n_sol'] = int(temp[1])
        # print("-- n_sol = ", res_dict['n_sol'] )
        start_idx = 7
        res_dict["paths"] = dict()
        res_dict["costs"] = dict()
        for i in range(res_dict['n_sol']):
            # sol ID
            temp = lines[start_idx+3*i].split(":")
            solID = int(temp[1])
            # cost vector
            temp = lines[start_idx+3*i+1].split(",")
            cvec = list()
            cvec.append( int(temp[0][1:]) )
            for j in range(1,len(temp)-1):
                cvec.append(int(temp[j]))
            res_dict["costs"][solID] = np.array(cvec)
            # path
            temp = lines[start_idx+3*i+2].split(' ')
            res_dict["paths"][solID] = list(map(int, list(temp[:-1])))
    return res_dict

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

    # Print output and errors
    print()
    print("1111111111111111111111111111111111")
    print(stdout[0].decode(), "1111111111111111111111111111111111")
    # print()

    process.wait() # otherwise, subprocess run concurrently...
    print("[INFO] runEMOA (python) invoke c++ bin finished..." )


if __name__ == "__main__":

    grs = ["../data/ex1-c1.gr", "../data/ex1-c2.gr", "../data/ex1-c3.gr"]

    # runEMOA(["../data/ex1-c1.gr", "../data/ex1-c2.gr", "../data/ex1-c3.gr"],
    #         "../data/",
    #         "../cmake-build-debug/run_emoa.exe",
    #         "../data/temp-res.txt",
    #         1, 5, 60)

    runEMOA(["../data/USA-road-d.NY.gr", "../data/USA-road-t.NY.gr"],
            "../data/",
            "../cmake-build-debug/run_emoa.exe",
            "../data/NY-result.txt",
            1, 100, 600)


