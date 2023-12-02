import pandas as pd
import statistics
import csv
import os

def calculate_mean_stdev():
    with open('results.csv', mode='w', newline='') as csvfile:
        fieldnames = ['Metric', 'Mean', 'Standard Deviation']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

    df = pd.read_csv('extracted_data.csv')
    grouped_data = df.groupby('Metric')['Value']
    mean = grouped_data.mean()
    stdev = grouped_data.apply(statistics.stdev)

    for metric, mean, stdev in zip(mean.index, mean, stdev):
        with open('results.csv', mode='a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'Metric': metric, 'Mean': mean, 'Standard Deviation': stdev})

        print(f'Mean {metric}: {mean} milliseconds')
        print(f'Standard Deviation {metric}: {stdev} milliseconds')

if __name__ == "__main__":
    calculate_mean_stdev()