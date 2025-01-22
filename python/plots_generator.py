import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def ny_table_generator(input_file: str = "../data_out/NY_results/NY_test_results_final.csv",
                       output_file: str = "../data_out/plots_and_tables/NY_successful_runs_table.csv"):
    test_results = pd.read_csv(input_file)
    comparison_data = []
    algorithms = ['emoa', 'boa']

    num_tests = test_results['test_number'].nunique()

    for algorithm in algorithms:
        algorithm_data = test_results[test_results['algorithm'] == algorithm]
        successful_runs = algorithm_data[algorithm_data['timeout'] == 0]

        comparison_data.append({
            'Algorithm': "EMOA*" if algorithm == "emoa" else "ext-BOA*-lex",
            'Successful Runs': str(len(successful_runs)) + "/" + str(num_tests),
            'Avg Search Time': successful_runs['search_time'].mean(),
            'Median Search Time': successful_runs['search_time'].median(),
            'Max Search Time': successful_runs['search_time'].max()
        })

    comparison_table = pd.DataFrame(comparison_data)
    comparison_table.to_csv(output_file, index=False)

    return comparison_table


def plot_search_time_vs_solutions(min_dim: int = 3, max_dim: int = 10, walls_percentage_list: tuple = (0, 5, 10)):
    all_data = []

    for num_dims in range(min_dim, max_dim + 1):
        for walls_percentage in walls_percentage_list:
            file_name = f"../data_out/simple_map_{num_dims}_results/simple_map_{num_dims}_{walls_percentage}.csv"

            if os.path.exists(file_name):
                df = pd.read_csv(file_name)
                df['num_dims'] = num_dims
                df['walls_percentage'] = walls_percentage
                all_data.append(df)

    if not all_data:
        print("No data files found.")
        return

    combined_data = pd.concat(all_data, ignore_index=True)

    fig = plt.figure(figsize=(22, 12))
    gs = fig.add_gridspec(2, 5)

    colors = {
        ('emoa', 0): 'red',
        ('emoa', 5): 'darkred',
        ('emoa', 10): 'salmon',
        ('boa', 0): 'blue',
        ('boa', 5): 'darkblue',
        ('boa', 10): 'skyblue'
    }
    markers = {0: 'x', 5: 'o', 10: 's'}

    for idx, num_dims in enumerate(range(3, 11)):
        ax = fig.add_subplot(gs[idx // 4, idx % 4])
        data = combined_data[combined_data['num_dims'] == num_dims]

        for algorithm in ['emoa', 'boa']:
            for walls in [0, 5, 10]:
                subset = data[(data['algorithm'] == algorithm) & (data['walls_percentage'] == walls)]
                if not subset.empty:
                    ax.scatter(subset['num_solutions'], subset['search_time'],
                               c=colors[(algorithm, walls)], marker=markers[walls],
                               label=f"{algorithm}, {walls}% walls", alpha=0.7, s=15)

        ax.set_title(f'Dimensions: {num_dims}', fontsize=12)
        ax.set_xlabel('Number of Solutions', fontsize=10)
        ax.set_ylabel('Search Time', fontsize=10)
        ax.set_yscale('log')

        ax.set_xlim(0, 5000)
        ax.set_xticks([0, 1000, 2000, 3000, 4000, 5000])
        ax.set_xticklabels(['0', '1000', '2000', '3000', '4000', '5000'])

        ax.grid(True, which="both", ls="-", alpha=0.2)

    legend_ax = fig.add_subplot(gs[:, -1])
    legend_ax.axis('off')

    legend_elements = [plt.Line2D([0], [0], marker=markers[walls], color=colors[(alg, walls)],
                                  label=f'{alg}, {walls}% walls', markersize=10, linestyle='None')
                       for alg in ['emoa', 'boa'] for walls in [0, 5, 10]]
    legend_ax.legend(handles=legend_elements, loc='center', title='Algorithm and Wall Percentage')

    plt.tight_layout()
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.15, top=0.85, hspace=0.5, wspace=0.35)
    plt.suptitle('Search Time vs Number of Solutions for Different Dimensions', fontsize=16, y=0.95)

    # plt.show()
    plt.savefig('../data_out/plots_and_tables/st_num_sol_all_dims.png', dpi=500, bbox_inches='tight')


def simple_map_table_generator(min_dim: int = 3, max_dim: int = 10, walls_percentage_list: tuple = (0, 5, 10),
                               output_file: str = "../data_out/plots_and_tables/simple_map_stats_table.csv"):
    results = []

    for num_dims in range(min_dim, max_dim + 1):
        for walls_percentage in walls_percentage_list:
            file_name = f"../data_out/simple_map_{num_dims}_results/simple_map_{num_dims}_{walls_percentage}.csv"

            if os.path.exists(file_name):
                df = pd.read_csv(file_name)
                df['num_dims'] = num_dims
                df['walls_percentage'] = walls_percentage

                grouped = df.groupby(['test_number', 'algorithm'])['search_time'].first().unstack('algorithm')
                ratio = grouped['boa'] / grouped['emoa']

                stats = {
                    'num_dims': num_dims,
                    'walls_percentage': walls_percentage,
                    'mean_ratio': round(ratio.mean(), 2),
                    'median_ratio': round(ratio.median(), 2),
                    # 'std_ratio': round(ratio.std(), 2),
                    'min_ratio': round(ratio.min(), 2),
                    'max_ratio': round(ratio.max(), 2),
                    # 'q1_ratio': round(ratio.quantile(0.25), 2),
                    # 'q3_ratio': round(ratio.quantile(0.75), 2)
                }

                results.append(stats)

    final_table = pd.DataFrame(results)
    final_table = final_table.sort_values(['num_dims', 'walls_percentage'])
    final_table.to_csv(output_file, index=False)

    return final_table


def simple_map_plot_mean_ratio(input_file: str, output_file: str):
    df = pd.read_csv(input_file)

    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = sns.color_palette("viridis", n_colors=len(df['walls_percentage'].unique()))

    for i, percentage in enumerate(df['walls_percentage'].unique()):
        data = df[df['walls_percentage'] == percentage]
        ax.plot(data['num_dims'], data['mean_ratio'],
            label=f'{percentage}%',
            marker='o',
            color=colors[i],
            linewidth=2.5,
            alpha=0.7)

    ax.set_xlabel('Map dimension')
    ax.set_ylabel('Average ratio of BOA runtime to EMOA')
    ax.set_title('Dependence of average BOA to EMOA runtime ratio on map dimensionality')
    ax.legend(title='Walls percentage')

    # plt.show()
    plt.savefig(output_file, dpi=500, bbox_inches='tight')


if __name__ == "__main__":
    # NY successful runs table
    # comparison_table = ny_table_generator(input_file="../data_out/NY_results/NY_test_results_final.csv",
    #                                       output_file="../data_out/plots_and_tables/NY_successful_runs_table.csv")

    # Plot for simple maps of different dims and walls percentages
    # plot_search_time_vs_solutions(min_dim=3, max_dim=10, walls_percentage_list=(0, 5, 10))

    # Table with some statistics for simple maps of different dims and walls percentages
    # simple_map_table_generator(min_dim=3, max_dim=10, walls_percentage_list=(0, 5, 10),
    #                            output_file = "../data_out/plots_and_tables/simple_map_stats_table.csv")

    # PLot with some statistics for simple maps of different dims and walls percentages
    simple_map_plot_mean_ratio(input_file = "../data_out/plots_and_tables/simple_map_stats_table.csv",
                               output_file = "../data_out/plots_and_tables/simple_map_mean_ratio_plot.png")
