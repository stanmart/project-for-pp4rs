import os
import pathlib2
import argparse
import datetime
import numpy as np
import pandas as pd


def collect_shape_data(gtfs_dir):
    """Calculate the number of times a shape (line on a map) is travelled.
    Appends some additional information about the route that the shape belongs to.

    Args:
        gtfs_dir: the directory where the GTFS file is extracted

    Returns:
        pandas.DataFrame: contains shape data
    """

    gtfs_dir = pathlib2.Path(gtfs_dir)

    service_days = calculate_service_days(gtfs_dir)
    trips = pd.read_csv(gtfs_dir / 'trips.txt', index_col=2)
    routes = pd.read_csv(gtfs_dir / 'routes.txt', index_col=0)

    route_id_diffs = trips \
        .groupby('shape_id') \
        .aggregate({'route_id': [min, max]})
    if any(route_id_diffs[('route_id', 'min')] != route_id_diffs[('route_id', 'max')]):
        raise ValueError("Shape ids must uniquely identify route_ids")

    route_info = trips \
        .join(service_days, on="service_id", how="left") \
        .groupby(["shape_id"]) \
        .aggregate({'days': sum, 'route_id': 'first'}) \
        .rename(columns={'days': 'times_taken'}) \
        .join(
            routes[['route_short_name', 'route_type', 'route_color']],
            on="route_id", how="left"
        ) \
        .reset_index()

    return route_info


def calculate_service_days(gtfs_dir):
    """Calculate the number of active days for each service.

    Args:
        gtfs_dir: the directory where the GTFS file is extracted

    Returns:
        pandas.DataFrame: contains day counts by service_id
    """

    gtfs_dir = pathlib2.Path(gtfs_dir)

    calendar = pd.read_csv(gtfs_dir / 'calendar.txt', index_col=0)
    calendar_dates = pd.read_csv(gtfs_dir / 'calendar_dates.txt')

    validity_weeks = calculate_validity_weeks(calendar)
    regular_number_of_days = calendar \
        .loc[:, ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']] \
        .sum(axis=1) \
        * validity_weeks

    exception_key = pd.DataFrame({
        "exception_type": [1, 2],
        "day_diff": [1, -1]
    })
    irregular_number_of_days = calendar_dates \
        .merge(exception_key, on="exception_type", how="left") \
        .groupby("service_id") \
        .sum()

    number_of_days = regular_number_of_days \
        .to_frame(name="regular_days") \
        .join(irregular_number_of_days[["day_diff"]], how="outer") \
        .fillna(value=0) \
        .assign(days=lambda df: df.regular_days + df.day_diff)

    if number_of_days.days.min() < 0:
        raise ValueError("Number of days a service operates on cannot be negative.")

    return number_of_days


def calculate_validity_weeks(calendar):
    """Calculate the validity of the calendar in weeks.

    Args:
        calendar: a pandas.DataFrame containing the contents of calendar.txt

    Returns:
        int: the validity of the timetable in weeks
    """

    if calendar.start_date.min() != calendar.start_date.max() or \
            calendar.end_date.min() != calendar.end_date.max():
        raise ValueError("Non-uniform timetable validities are not handled yet.")
    start_date = datetime.datetime.strptime(
        str(calendar.start_date[0]),
        '%Y%m%d'
    )
    end_date = datetime.datetime.strptime(
        str(calendar.end_date[0]),
        '%Y%m%d'
    )

    validity_days = (end_date - start_date).days + 1
    if validity_days % 7 != 0:
        raise ValueError("Non-integer weeks are not handled yet.")

    return validity_days // 7


def generate_plot_data(gtfs_dir, shape_data):
    """Generates a dataset suitable for line plots using datashader.

    Args:
        gtfs_dir: the directory where the GTFS file is extracted
        shape_data: additional shape data that is needed for the plotting

    Returns:
        pandas.DataFrame: a DataFrame that is used for line plots
    """

    gtfs_dir = pathlib2.Path(gtfs_dir)
    shapes = pd.read_csv(gtfs_dir / 'shapes.txt')

    plotting_data = insert_empty_rows(shapes, 'shape_id') \
        .merge(shape_data, on='shape_id', how='left')

    return plotting_data


def insert_empty_rows(df, by):
    """ Inserts a row filled with NaNs between each chunk of the dataframe
    separated by a variable. The resulting dataset is suitable for line plots.

    Args:
        df: a pandas.DataFrame
        by: a column of `df` that will be used for the grouping

    Returns:
        pandas.DataFrame: the same as the input `df` with empty lines inserted
        between groups
    """

    df_parts = []

    for level, df_part in df.groupby(by):
        empty = pd.DataFrame(
            [[level if colname == by else np.NaN for colname in df.columns]],
            columns=df.columns
        )
        df_parts.append(df_part.append(empty))

    return pd.concat(df_parts)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-g', '--gtfs-dir',
        help="The diractory where the GTFS files are located",
        type=str,
        required=True
    )
    parser.add_argument(
        '-o', '--out-dir',
        help="The diractory where the new data files are created. \
              Default is the same as the data directory.",
        type=str
    )

    args = parser.parse_args()
    if not args.out_dir:
        args.out_dir = args.gtfs_dir

    shape_data = collect_shape_data(args.gtfs_dir)
    plot_data = generate_plot_data(args.gtfs_dir, shape_data)

    out_dir = pathlib2.Path(args.out_dir)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    elif not os.path.isdir(out_dir):
        raise NotADirectoryError("The object at out_dir exists but is not a directory")

    shape_data.to_csv(out_dir / 'shape_data.csv', index=False)
    plot_data.to_csv(out_dir / 'plot_data.csv', index=False)


if __name__ == "__main__":
    main()
