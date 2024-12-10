import pandas as pd


if __name__ == "__main__":
    num = 5
    walls = 10
    df1 = pd.read_csv('../data_out/NY_results/NY_test_results_wout_labels.csv')
    df2 = pd.read_csv('../data_out/NY_results/NY_test_results_2_1.csv')
    df3 = pd.read_csv('../data_out/NY_results/NY_test_results_2_2.csv')

    combined_df = pd.concat([df1, df2, df3], ignore_index=True)

    sorted_df = combined_df.sort_values(by=['test_number', 'algorithm'])

    sorted_df.to_csv('../data_out/NY_results/NY_test_results_final.csv', index=False)