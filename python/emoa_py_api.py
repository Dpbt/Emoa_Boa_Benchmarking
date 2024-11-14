"""
About: python helper APIs
Author: Zhongqiang (Richard) Ren
"""

import numpy as np
import sys
import subprocess
import time


def costGrid2file(cg, fname, conn=4):
  """
  store the cost matrices to a file in the format required by EMOA* bin.
  cg = a numpy matrix.
  conn = 4 or 8, which means 4-connected or 8-connected.
  """
  (nyt, nxt) = cg.shape
  num_nodes = nyt*nxt
  num_edges = 2*((nyt-1)*(nxt-1)*2 + nyt-1 + nxt-1)

  nghs = []
  if conn == 4:
    nghs = [(0,1),(0,-1),(1,0),(-1,0)]
  elif conn == 8:
    nghs = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
  else:
    sys.exit("[ERROR] costGrid2file, neither 4- nor 8-connected!")

  with open(fname, mode="w+") as f:
    f.write("c This is a cost file for a grid world\n")
    f.write("p sp " + str(num_nodes) + " " + str(num_edges)+"\n")
    for iy in range(nyt):
      for ix in range(nxt):
        u = iy*nxt + ix
        for ngh in nghs:
          jy = iy + ngh[0]
          jx = ix + ngh[1]
          if jy < 0 or jy >= nyt or jx < 0 or jx >= nxt:
          	continue
          v = jy*nxt + jx
          f.write("a "+str(u)+" "+str(v)+" "+str(int(cg[jy,jx]))+"\n" ) # only support integer, floor the cost number.
    f.close()
  return

def getResult(res_file):
  """
  """
  res_dict = dict()
  with open(res_file, mode="r") as fres:
    lines = fres.readlines()
    # print(lines)
    # temp = lines[0].split(':')
    # res_dict["graph_load_time"] = float(temp[1])
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


# def runEMOA(cg_list, data_folder, exe_path, res_path, vo, vd, tlimit):
#   """
#   """
#   print("[INFO] runEMOA (python) vo =", vo, ", vd =", vd, ", tlimit =", tlimit, ", M =", len(cg_list) )
#
#   # generate cost files.
#   fnames = list()
#   for i,cg in enumerate(cg_list):
#     fname = data_folder+"temp-c" + str(i+1) + ".gr"
#     costGrid2file(cg, fname)
#     fnames.append(fname)
#   print("[INFO] runEMOA (python) cost file generated..." )
#
#   # run EMOA*.
#   cmd = [exe_path, str(vo), str(vd), str(tlimit), str(len(cg_list))] + fnames
#   cmd.append(res_path)
#
#   cmd_s = ' '.join(cmd[1:])
#
#   # command = ["C:\\Program Files\\Git\\bin\\bash.exe",
#   #            "-c",
#   #            f"cd /c/Users/denis/CLionProjects/public_emoa2/cmake-build-debug && ./run_emoa.exe {str(vo)} {str(vd)} "
#   #            f"{str(tlimit)} {str(len(cg_list))} ../data/ex1-c1.gr ../data/ex1-c2.gr ../data/ex1-c3.gr ../data/result.txt"]
#
#   cmd = ["C:\\Program Files\\Git\\bin\\bash.exe",
#              "-c",
#              "cd /c/Users/denis/CLionProjects/public_emoa2/cmake-build-debug && ./run_emoa.exe " + cmd_s]
#
#   # print(cmd)
#   # print(command)
#
#   process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
#
#   stdout, stderr = process.communicate()
#
#   # Print output and errors
#   print(stdout.decode())
#   print(stderr.decode())
#
#   process.wait() # otherwise, subprocess run concurrently...
#   print("[INFO] runEMOA (python) invoke c++ bin finished..." )
#
#   out = getResult(res_path)
#   print("[INFO] runEMOA (python) get result from file done..." )
#
#   return out


def runEMOA(cg_list, data_folder, exe_path, res_path, vo, vd, tlimit):
  """
  """
  print("[INFO] runEMOA (python) vo =", vo, ", vd =", vd, ", tlimit =", tlimit, ", M =", len(cg_list) )

  # generate cost files.
  # fnames = list()
  # for i,cg in enumerate(cg_list):
  #   fname = data_folder+"temp-c" + str(i+1) + ".gr"
  #   costGrid2file(cg, fname)
  #   fnames.append(fname)
  # print("[INFO] runEMOA (python) cost file generated..." )

  # run EMOA*.
  cmd = [exe_path, str(vo), str(vd), str(tlimit), str(len(cg_list))] + cg_list
  cmd.append(res_path)

  cmd_s = ' '.join(cmd[1:])

  cmd = ["C:\\Program Files\\Git\\bin\\bash.exe",
         "-c",
         "cd /c/Users/denis/CLionProjects/public_emoa2/cmake-build-debug && ./run_emoa.exe " + cmd_s]

  process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

  stdout = process.communicate()

  # Print output and errors
  print("1111111111111111111111111111111111")
  print(stdout[0].decode())
  print("1111111111111111111111111111111111")
  # print(stderr.decode())

  process.wait() # otherwise, subprocess run concurrently...
  print("[INFO] runEMOA (python) invoke c++ bin finished..." )

  out = getResult(res_path)
  print("[INFO] runEMOA (python) get result from file done..." )

  return out


if __name__ == "__main__":

  # cost grid 1
  c1 = np.ones([3,3])*3
  c1[0,2] = 1

  # cost grid 2
  c2 = np.ones([3,3])*3
  c2[1,1] = 1

  # cost grid 3
  c3 = np.ones([3,3])*3
  c3[2,0] = 1

  grs = ["../data/ex1-c1.gr", "../data/ex1-c2.gr", "../data/ex1-c3.gr"]

  # run EMOA
  # res_dict = runEMOA([c1,c2,c3], "../data/", "../build/run_emoa",
  #                    "../data/temp-res.txt", 0, 8, 60)
  # res_dict = runEMOA([c1,c2,c3], "../data/", "../cmake-build-debug/run_emoa.exe",
  #                    "../data/temp-res.txt", 1, 5, 60)
  res_dict = runEMOA(["../data/ex1-c1.gr", "../data/ex1-c2.gr", "../data/ex1-c3.gr"], "../data/", "../cmake-build-debug/run_emoa.exe",
                     "../data/temp-res.txt", 1, 5, 60)
  print(res_dict)


