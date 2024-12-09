import pandas as pd


if __name__ == "__main__":
    num = 5
    walls = 0
    df = pd.read_csv(f'../data_out/simple_map_{num}_results/simple_map_{num}_{walls}.csv')
    # df2 = pd.read_csv('../data_out/NY_test_results_2.csv')
    # df3 = pd.read_csv('../data_out/NY_test_results_3.csv')

    # combined_df = pd.concat([df1, df2, df3], ignore_index=True)

    sorted_df = df.sort_values(by=['test_number', 'algorithm'])

    sorted_df.to_csv(f'../data_out/simple_map_{num}_results/simple_map_{num}_{walls}.csv', index=False)