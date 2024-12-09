import pandas as pd

import sys
sys.path.append('../../python')

from emoa_py_api_for_tests import test_emoa

if __name__ == "__main__":

        pd.set_option('display.max_columns', None)


        # tests = [["emoa", "NY", 600, 1, 5000, "./data_out/NY-result.txt",
        #           ["./data/USA-road-d.NY.gr", "./data/USA-road-t.NY.gr", "./data/USA-road-deg.NY.gr"]]]

        tests = [["emoa", "NY", 600, 3, 100, "C:/Users/denis/PycharmProjects/Emoa_heu_tests/data_out/NY-result.txt",
                  ["C:/Users/denis/PycharmProjects/Emoa_heu_tests/data/USA-road-d.NY.gr",
                   "C:/Users/denis/PycharmProjects/Emoa_heu_tests/data/USA-road-t.NY.gr",
                   "C:/Users/denis/PycharmProjects/Emoa_heu_tests/data/USA-road-deg.NY.gr"]]]

        test_results = test_emoa(tests, display_progress=True)

        test_results.to_csv('../../data_out/NY_test_results.csv', index=False)

        print(test_results)