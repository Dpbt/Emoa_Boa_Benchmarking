import pandas as pd


if __name__ == "__main__":
    df1 = pd.read_csv('../data_out/NY_test_results_1.csv')
    df2 = pd.read_csv('../data_out/NY_test_results_2.csv')
    df3 = pd.read_csv('../data_out/NY_test_results_3.csv')

    combined_df = pd.concat([df1, df2, df3], ignore_index=True)

    sorted_df = combined_df.sort_values(by=['test_number', 'algorithm'])

    sorted_df.to_csv('../data_out/NY_test_results.csv', index=False)