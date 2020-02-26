import pathlib2
import argparse
import datetime
import pandas as pd


def collect_shape_data(data_dir):
    """Calculate the number of times a shape (line on a map) is travelled.
    Appends some additional information about the route that the shape belongs to.

    Args:
        data_dir: the directory where the GTFS file is extracted

    Returns:
        pandas.DataFrame: contains shape data
    """

    data_dir = pathlib2.Path(data_dir)

    service_days = calculate_service_days(data_dir)
    trips = pd.read_csv(data_dir / 'trips.txt', index_col=2)
    routes = pd.read_csv(data_dir / 'routes.txt', index_col=0)

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


def calculate_service_days(data_dir):
    """Calculate the number of active days for each service.

    Args:
        data_dir: the directory where the GTFS file is extracted

    Returns:
        pandas.DataFrame: contains day counts by service_id
    """

    data_dir = pathlib2.Path(data_dir)

    calendar = pd.read_csv(data_dir / 'calendar.txt', index_col=0)
    calendar_dates = pd.read_csv(data_dir / 'calendar_dates.txt')

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


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-d', '--data-dir',
        help="The diractory where the GTFS file is located",
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
        args.out_dir = args.data_dir

    shape_data = collect_shape_data(args.data_dir)


if __name__ == "__main__":
    main()
