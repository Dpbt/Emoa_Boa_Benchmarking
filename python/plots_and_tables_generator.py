"""
About: Python script for generating tables and plots from NY city map test results.
Author: Denis Derkach
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def ny_table_generator(input_file: str = "../data_out/NY_results/NY_test_results_final.csv",
                       output_file: str = "../data_out/plots_and_tables/NY_successful_runs_table.csv") -> pd.DataFrame:
    """
    Generates a comparison table of successful runs for EMOA and BOA algorithms.

    The table includes the number of successful runs and average search times.

    :param input_file: Path to the input CSV file containing test results.
    :param output_file: Path to the output CSV file where the comparison table will be saved.
    :return: A DataFrame containing the comparison data.
    """
    test_results = pd.read_csv(input_file)
    comparison_data = []
    algorithms = ["emoa", "boa"]

    num_tests = test_results["test_number"].nunique()

    for algorithm in algorithms:
        algorithm_data = test_results[test_results["algorithm"] == algorithm]
        successful_runs = algorithm_data[algorithm_data["timeout"] == 0]

        comparison_data.append({
            "Algorithm": "EMOA*" if algorithm == "emoa" else "ext-BOA*-lex",
            "Successful Runs": f"{len(successful_runs)}/{num_tests}",
            "Avg Search Time": round(successful_runs["search_time"].mean(), 2),
            "Median Search Time": round(successful_runs["search_time"].median(), 2),
            "Max Search Time": round(successful_runs["search_time"].max(), 2)
        })

    comparison_table = pd.DataFrame(comparison_data)
    comparison_table.to_csv(output_file, index=False)

    return comparison_table


def ny_table_generator_2(input_file: str, output_file: str) -> None:
    """
    Generates a table of solution ratios for tests that timed out.

    The ratio is calculated between the number of solutions found by EMOA and BOA.

    :param input_file: Path to the input CSV file containing test results.
    :param output_file: Path to the output CSV file where the statistics will be saved.
    :return: None
    """
    test_results = pd.read_csv(input_file)

    filtered_results = test_results[test_results["timeout"] == 1]
    valid_tests = filtered_results.groupby("test_number").filter(lambda x: set(x["algorithm"]) == {"emoa", "boa"})

    ratios = []

    for test_number in valid_tests["test_number"].unique():
        emoa_solutions = \
            valid_tests[(valid_tests["test_number"] == test_number) & (valid_tests["algorithm"] == "emoa")][
                "num_solutions"].values[0]
        boa_solutions = valid_tests[(valid_tests["test_number"] == test_number) & (valid_tests["algorithm"] == "boa")][
            "num_solutions"].values[0]

        ratio = emoa_solutions / boa_solutions
        ratios.append({"test_number": test_number, "solution_ratio": ratio})

    ratios_df = pd.DataFrame(ratios)

    statistics = {
        "min": round(ratios_df["solution_ratio"].min(), 2),
        "average": round(ratios_df["solution_ratio"].mean(), 2),
        "median": round(ratios_df["solution_ratio"].median(), 2),
        "max": round(ratios_df["solution_ratio"].max(), 2)
    }

    stats_df = pd.DataFrame(statistics, index=[0])
    stats_df.to_csv(output_file, index=False)


def plot_search_time_vs_solutions(min_dim: int = 3, max_dim: int = 10,
                                  walls_percentage_list: tuple = (0, 5, 10),
                                  output_file: str = "../data_out/plots_and_tables/st_num_sol_all_dims.png") -> None:
    """
    Plots search time against the number of solutions for different dimensions and wall percentages.

    :param min_dim: Minimum dimension to consider.
    :param max_dim: Maximum dimension to consider.
    :param walls_percentage_list: Tuple of wall percentages to consider in the plots.
    :param output_file: Path to the output image file where the plot will be saved.
    :return: None
    """

    all_data = []

    for num_dims in range(min_dim, max_dim + 1):
        for walls_percentage in walls_percentage_list:
            file_name = f"../data_out/simple_map_{num_dims}_results/simple_map_{num_dims}_{walls_percentage}.csv"

            if os.path.exists(file_name):
                df = pd.read_csv(file_name)
                df["num_dims"] = num_dims
                df["walls_percentage"] = walls_percentage
                all_data.append(df)

    if not all_data:
        print("No data files found.")
        return

    combined_data = pd.concat(all_data, ignore_index=True)

    fig = plt.figure(figsize=(22, 12))
    gs = fig.add_gridspec(2, 5)

    colors = {
        ("emoa", 0): "red",
        ("emoa", 5): "darkred",
        ("emoa", 10): "salmon",
        ("boa", 0): "blue",
        ("boa", 5): "darkblue",
        ("boa", 10): "skyblue"
    }

    markers = {0: "x", 5: "o", 10: "s"}

    for idx, num_dims in enumerate(range(3, 11)):
        ax = fig.add_subplot(gs[idx // 4, idx % 4])
        data = combined_data[combined_data["num_dims"] == num_dims]

        for algorithm in ["emoa", "boa"]:
            for walls in [0, 5, 10]:
                subset = data[(data["algorithm"] == algorithm) & (data["walls_percentage"] == walls)]
                if not subset.empty:
                    ax.scatter(subset["num_solutions"], subset["search_time"],
                               c=colors[(algorithm, walls)], marker=markers[walls],
                               label=f"{algorithm}, {walls}% walls", alpha=0.7, s=15)

        ax.set_title(f"Dimensions: {num_dims}", fontsize=24)
        ax.set_xlabel("Number of Solutions", fontsize=24)
        ax.set_ylabel("Search Time", fontsize=24)
        ax.set_yscale("log")

        ax.set_xlim(0, 5000)
        ax.set_xticks([0, 1000, 2000, 3000, 4000, 5000])
        ax.set_xticklabels(["0", "1000", "2000", "3000", "4000", "5000"])
        ax.tick_params(axis="both", labelsize=14)

        ax.grid(True, which="both", ls="-", alpha=0.2)

    legend_ax = fig.add_subplot(gs[:, -1])
    legend_ax.axis("off")

    legend_elements = [plt.Line2D([0], [0], marker=markers[walls], color=colors[(alg, walls)],
                                  label=f"{alg}, {walls}% walls", markersize=10, linestyle="None")
                       for alg in ["emoa", "boa"] for walls in [0, 5, 10]]

    legend_ax.legend(handles=legend_elements, loc="center", title="Algorithm and Wall Percentage", fontsize=18,
                     title_fontsize=20)

    plt.tight_layout()

    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.15,
                        top=0.85, hspace=0.4, wspace=0.38)

    plt.suptitle("Search Time vs Number of Solutions for Different Dimensions",
                 fontsize=40,
                 y=0.95)

    plt.savefig(output_file,
                dpi=400,
                bbox_inches="tight")


def simple_map_table_generator(min_dim: int = 3,
                               max_dim: int = 10,
                               walls_percentage_list: tuple = (0, 5, 10),
                               output_file: str = "../data_out/plots_and_tables/simple_map_stats_table.csv") -> pd.DataFrame:
    """
    Generates a statistics table for simple maps based on dimensions and wall percentages.

    The table includes mean and min/max ratios of BOA to EMOA runtimes.

    :param min_dim: Minimum dimension to consider.
    :param max_dim: Maximum dimension to consider.
    :param walls_percentage_list: Tuple of wall percentages to consider.
    :param output_file: Path to the output CSV file where the statistics will be saved.
    :return: A DataFrame containing the statistics.
    """

    results = []

    for num_dims in range(min_dim, max_dim + 1):
        for walls_percentage in walls_percentage_list:
            file_name = f"../data_out/simple_map_{num_dims}_results/simple_map_{num_dims}_{walls_percentage}.csv"

            if os.path.exists(file_name):
                df = pd.read_csv(file_name)
                df["num_dims"] = num_dims
                df["walls_percentage"] = walls_percentage

                grouped = df.groupby(["test_number", "algorithm"])["search_time"].first().unstack("algorithm")
                ratio = grouped["boa"] / grouped["emoa"]

                stats = {
                    "num_dims": num_dims,
                    "walls_percentage": walls_percentage,
                    "mean_ratio": round(ratio.mean(), 2),
                    "median_ratio": round(ratio.median(), 2),
                    # Uncomment if needed
                    # "std_ratio": round(ratio.std(), 2),
                    "min_ratio": round(ratio.min(), 2),
                    "max_ratio": round(ratio.max(), 2),
                    # Uncomment if needed
                    # "q1_ratio": round(ratio.quantile(0.25), 2),
                    # "q3_ratio": round(ratio.quantile(0.75), 2)
                }

                results.append(stats)

    final_table = pd.DataFrame(results)
    final_table.sort_values(["num_dims", "walls_percentage"], inplace=True)
    final_table.to_csv(output_file, index=False)

    return final_table


def simple_map_plot_mean_ratio(input_file: str,
                               output_file: str) -> None:
    """
    Plots the mean ratio of BOA runtime to EMOA runtime based on map dimensionality.

    :param input_file: Path to the input CSV file containing mean ratios.
    :param output_file: Path to the output image file where the plot will be saved.
    :return: None
    """

    df = pd.read_csv(input_file)

    plt.style.use("seaborn")
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = sns.color_palette("viridis", n_colors=len(df["walls_percentage"].unique()))

    for i, percentage in enumerate(df["walls_percentage"].unique()):
        data = df[df["walls_percentage"] == percentage]
        ax.plot(data["num_dims"], data["mean_ratio"],
                label=f"{percentage}%",
                marker="o",
                color=colors[i],
                linewidth=2.5,
                alpha=0.7)

    ax.set_xlabel("Map dimension", fontsize=20)
    ax.set_ylabel("Average ratio of BOA runtime to EMOA", fontsize=16)
    ax.set_title("Dependence of average BOA to EMOA runtime ratio on map dimensionality",
                 fontsize=20,
                 pad=20)

    ax.legend(title="Walls percentage", fontsize=15,
              title_fontsize="17")

    ax.tick_params(axis="both", labelsize=16)

    plt.savefig(output_file,
                dpi=500,
                bbox_inches="tight")


if __name__ == "__main__":
    # NY successful runs table
    comparison_table = ny_table_generator(input_file="../data_out/NY_results/NY_test_results_final.csv",
                                          output_file="../data_out/plots_and_tables/NY_successful_runs_table.csv")

    # NY table generation: can be uncommented if needed
    # ny_table_generator_2(input_file="../data_out/NY_results/NY_test_results_final.csv",
    #                      output_file="../data_out/plots_and_tables/NY_table_2.csv")

    # Plotting search time vs solutions: can be uncommented if needed
    # plot_search_time_vs_solutions(min_dim=3,
    #                               max_dim=10,
    #                               walls_percentage_list=(0, 5, 10),
    #                               output_file="../data_out/plots_and_tables/st_num_sol_all_dims.png")

    # Table with some statistics for simple maps: can be uncommented if needed
    # simple_map_table_generator(min_dim=3,
    #                            max_dim=10,
    #                            walls_percentage_list=(0, 5, 10),
    #                            output_file="../data_out/plots_and_tables/simple_map_stats_table.csv")

    # Plotting mean ratio: can be uncommented if needed
    # simple_map_plot_mean_ratio(input_file="../data_out/plots_and_tables/simple_map_stats_table.csv",
    #                            output_file="../data_out/plots_and_tables/simple_map_mean_ratio_plot.png")
