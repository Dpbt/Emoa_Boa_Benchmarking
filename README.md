# Benchmarking of EMOA\* and ext-BOA\*-lex algorithms

In this project, we make a detailed comparison of two algorithms that solve the multi-objective shortest path problem (
MO-SPP) on a graph where the goal is to find a set of Pareto-optimal solutions from the initial vertex to the final
vertex in the graph. This repository contains a C++ implementation of the Enhanced Multi-Objective A\* algorithm (
EMOA\*) and the Extended Bi-Objective Search Algorithm (ext-BOA\*-lex), as well as their benchmarking and the code used
for it. More technical information about the algorithms can be found in [[1](https://arxiv.org/pdf/2202.08992.pdf)]
and [[2](https://icaps20.icaps-conference.org/paper199.html)].

The original implementation of the EMOA algorithm\* was obtained from
the [repository](https://github.com/rap-lab-org/public_emoa) of the authors of the original paper.

<img src="https://github.com/wonderren/wonderren.github.io/blob/master/images/fig_emoa_NY17.png" alt="" align="middle" hspace="20" style=" border: #FFFFFF 2px none;">

(Fig 1: Some Pareto-optimal solution paths in a New York City roadmap that optimize path length, arrival time and path
risk.)

## Requirements

* We use CMake (3.16.3) and Make (4.2.1) to compile the code. Lower or higher version may also work.

## Project Structure

* `README.md` - This file
* `data/` - Map (New-York road map, generated maps and example map) files
* `dataout/` - Tables containing benchmarking results, generated plots and some technical files
* `source/` - Contains the path planning source code
* `test/` - Contains example code for path planning algorithms
* `include/` - Contains header files
* `python/` - Our python api for benchmarking algorithms, plots, maps and tests generators

## Our work

* The code of the ext-BOA\*-lex algorithm implemented in C++ (`source/search_boalex.cpp` and `test/run_boalex.cpp`
  files)
* A parallel test system that runs tests for both algorithms (`python/py_parallel_api.py` file)
* A map generator of a given size, dimensionality, with the ability to add random walls (`python/map_generator.py` file)
* Third metric generator for New York's expensive maps (`python/3_dimension_generator_for_ny_map.py` file)
* Test list generator based on our map generators (`python/tests_generator.py` file)
* Code that generates plots showing our results (`python/plots_generator.py` file)

## Instructions:

### Installation

* Clone this repo
* Compile this repo
    * `mkdir build`
    * `cd build`
    * `cmake ..` (You can specify the build type you like by adding additional args)
    * `make`
* Run example in `./test_emoa `

### Command-Line Interface (CLI)

* Run example via command-line interface (CLI)
    * `./run_emoa 1 5 60 3 ../data/ex1-c1.gr ../data/ex1-c2.gr ../data/ex1-c3.gr ../data/result.txt` or
    * `./run_boalex 1 5 60 3 ../data/ex1-c1.gr ../data/ex1-c2.gr ../data/ex1-c3.gr ../data/result.txt`
    * Runs EMOA\* on 3-cost graph (edge weights detailed in `../data/ex1-c1.gr`, `../data/ex1-c2.gr`,
      `../data/ex1-c3.gr`) to find solutions from node 1 to node 5 with a 60 second time limit, and saves results into
      `data/result.txt`
* General usage of the command-line interface
    *
    `./run_emoa (arg1 v_start) (arg2 v_dest) (arg3 time_limit) (arg4 M) (arg5 graph1_path) (arg6 graph2_path) ... ((arg(M+4) graphM_path)) (arg(M+5) result_path)`
    *
    `./run_boalex (arg1 v_start) (arg2 v_dest) (arg3 time_limit) (arg4 M) (arg5 graph1_path) (arg6 graph2_path) ... ((arg(M+4) graphM_path)) (arg(M+5) result_path)`
    * arg1 v_start = the starting node
    * arg2 v_dest = the destination node
    * arg3 time_limit = the time limit for EMOA\*
    * arg4 M = the number of objectives for the input instance
    * arg5~arg(M+4) = the paths to M files that describe the graph, where each file contains the edge weights for one
      type of edge cost in the graph (details about file structure are specified below)
    * arg(M+5) = the path of the result file
* For help info `./run_emoa -h` or `./run_emoa --help`

### Preliminary Python API

* We have also developed a Python wrapper based on the aforementioned CLI (by writing and reading files and call the
  CLI), which can be found in `python/py_parallel_api.py`
* The main function in the API is `parallel_run`, which takes as input the list of tests, the size of batches for each
  process and the number of processes to parallelize testing and returns a pandas DataFrame, containing results for all
  tests in the list
* each test in the list must be presented in the following format: [experiment number, algorithm name (“boa” or “emoa”),
  map name, timelimit, start vertex, end vertex, file path to record the results of the experiment (.txt, intermediate
  file), [list of paths to map files]].
* The current Python wrapper is only applicable to grid-like map. For general usage, please use the CLI.
* More APIs may be developed in the future.

### Tests List Structure

The `tests` list is a collection of test cases that will be executed for different algorithms and configurations. Each
test case is represented as a list containing the following elements:

- **Test Number (`exp_number`)**: An integer representing the unique identifier for the test case.
- **Algorithm (`"boa"` or `"emoa"`)**: A string indicating which algorithm will be used for the test.
- **Map Name (`f"example map 3 dims"`)**: A formatted string describing the map being used.
- **Time Limit (`time_limit`)**: An integer specifying the maximum time allowed for the algorithm to run (in seconds).
- **Start Vertex (`start`)**: An integer representing the starting vertex index for the search algorithm.
- **Finish Vertex (`finish`)**: An integer representing the destination vertex index for the search algorithm.
- **Map Names List (`map_names_list`)**: A list of strings containing paths to the map files that will be used in this
  test.

#### Example of a Test Case

```python
tests = [[1, "emoa", "example map 3 dims", 600, 1, 5,
          ["../data/ex1-c1.gr", "../data/ex1-c2.gr", "../data/ex1-c3.gr"]],
         [1, "boa", "example map 3 dims", 600, 1, 5,
          ["../data/ex1-c1.gr", "../data/ex1-c2.gr", "../data/ex1-c3.gr"]]
         ]
```

### Graph file specification

* The input graph is directed.
* The node ID are within range 1~*n*, where *n* is the number of nodes in the graph.
* Parallel edges are not allowed.
* Graph files must follow the same format described
  by [DIMACS](http://www.diag.uniroma1.it//~challenge9/format.shtml#graph).
* Graph files used in the same run must correspond to each other line-by-line.
* In other words, it requires all cost files to have the same set of edges in the same order.

```
For example:
In c1 file, let’s say we have edges:
a 0 1 26
a 2 4 26
a 3 5 114
Then in c2 file, we also need to have edges:
a 0 1 x
a 2 4 y
a 3 5 z
Here, x,y,z are non-negative integer cost values. If, for example, edge (3,5) has cost zero, this edge also need to appear in the third place (i.e., the same place as in the c1 file) in c2 file, and has a value 0.
Same rule applies to all cost files.
```

### Result file specifiction

Result file contains 7 lines of metadata (graph_load_time, n_generated, n_expanded, n_domCheck, rt_initHeu, rt_search,
N). N is the number of solutions found.

Each of the N solutions are then listed in sets of three lines:

1. The first line contains `Label: {label_id}`, where the label_id identifies the solution
2. The second line contains the (space-separated) cost vector of the solution
3. The third line contains the (space-separated) path of vertices for the solution

### Notes for Performance

* The implementation of EMOA* (as well as the baselines as mentioned in the paper [1]) relies heavily on std::
  unordered_map from C++ STL for the purpose of easy implementation. Using other data structure such as std::vector (or
  simply arrays) can lead to improvement in performance than using std::unordered_map.

### References

* [1] Enhanced Multi-Objective A* Using Balanced Binary Search Trees.\
  Zhongqiang Ren, Richard Zhan, Sivakumar Rathinam, Maxim Likhachev and Howie Choset.\
  [[Bibtex](https://wonderren.github.io/files/bibtex_ren22emoa.txt)][[Paper](https://wonderren.github.io/files/ren22_emoa_socs.pdf)]
* [2] A Simple and Fast Bi-Objective Search Algorithm.\
  Carlos Hernandez Ulloa, William Yeoh, Jorge A. Baier, Han Zhang, Luis Suazo, Sven Koenig.\
  [[Paper](https://icaps20.icaps-conference.org/paper199.html)]

### Development Team

Contributors: [Denis Derkach](https://github.com/Dpbt), [Denis Kolesnikov](https://github.com/Hexpth).

Advisors: Konstantin Yakovlev (SPBU).