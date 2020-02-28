import argparse
import numpy as np
import pandas as pd


def create_table(shape_data, distance_data, out, num_rows):
    """Creates a figure of the ZVV transit network without any grouping.

    Args:
        data: a csv file containing data usable for line plots
        out: the generated imnage is saved here

    Returns:
        None
    """

    shape_data = pd.read_csv(shape_data, low_memory=False)
    distance_data = pd.read_csv(distance_data, low_memory=False)

    table = shape_data \
        .merge(distance_data, on="shape_id") \
        .sort_values('distance', ascending=False) \
        .loc[:, ["route_short_name", "times_taken", "distance"]] \
        .assign(distance=lambda df: np.round(df.distance, 1)) \
        .rename(columns={
            "route_short_name": "Route",
            "times_taken": "No. of trips per year",
            "distance": "Distance per trip (km)"
        }) \
        .head(num_rows)

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
        '-d', '--distance-data',
        help="A csv file containing distance data",
        type=str,
        required=True
    )
    parser.add_argument(
        '-o', '--out',
        help="The path of the output file",
        type=str,
        required=True
    )
    parser.add_argument(
        '-n', '--num-rows',
        help="Number of longest routes to display",
        type=int,
        default=10
    )

    args = parser.parse_args()

    create_table(args.shape_data, args.distance_data, args.out, args.num_rows)


if __name__ == "__main__":
    main()
