import argparse
import numpy as np
import pandas as pd


def create_table(shape_data, out):
    """Creates a table of the n longest routes (shapes) and saves it as a tex file.

    Args:
        shape_data: a csv file containing shape data
        distance_data: a csv file containing distance data
        out: the generated table is saved here

    Returns:
        None
    """

    shape_data = pd.read_csv(shape_data, low_memory=False)
    vehicle_key = pd.DataFrame({
        "route_type": [0, 2, 3, 7],
        "vehicle_type": ["Tram", "S-Bahn", "Bus", "Other"]
    })

    table = shape_data \
        .merge(vehicle_key, on="route_type") \
        .loc[:, ["vehicle_type", "times_taken"]] \
        .groupby("vehicle_type") \
        .aggregate(sum) \
        .sort_values("times_taken", ascending=False) \
        .reset_index() \
        .rename(columns={
            "vehicle_type": "Vehicle type",
            "times_taken": "Number of trips per year"
        })

    with open(out, 'w') as file:
        table.to_latex(buf=file, index=False)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-s', '--shape-data',
        help="A csv file containing shape data",
        type=str,
        required=True
    )
    parser.add_argument(
        '-o', '--out',
        help="The path of the output file",
        type=str,
        required=True
    )

    args = parser.parse_args()

    create_table(args.shape_data, args.out)


if __name__ == "__main__":
    main()
