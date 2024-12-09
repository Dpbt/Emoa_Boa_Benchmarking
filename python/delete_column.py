import pandas as pd


def process_csv_file(input_file, output_file):
    df = pd.read_csv(input_file)

    if 'solutions_labels' in df.columns:
        df = df.drop('solutions_labels', axis=1)

    df.to_csv(output_file, index=False)

    print(f"Обработка завершена. Результат сохранен в {output_file}")


if __name__ == "__main__":
    input_file = '../data_out/simple_map_5_results/simple_map_5_0.csv'
    output_file = '../data_out/simple_map_5_results/simple_map_5_0_wout_labels.csv'
    process_csv_file(input_file, output_file)