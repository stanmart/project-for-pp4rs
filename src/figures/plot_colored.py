import argparse
import pandas as pd
import datashader as ds
import datashader.transfer_functions as tf
from datashader.utils import export_image


def create_plot(data, out, width):
    """Creates a figure of the ZVV transit network using ZVV's color scheme.

    Args:
        data: a csv file containing data usable for line plots
        out: the generated imnage is saved here

    Returns:
        None
    """

    plot_data = pd.read_csv(data, low_memory=False)

    x_range = (plot_data.shape_pt_lon.min(), plot_data.shape_pt_lon.max())
    y_range = (plot_data.shape_pt_lat.min(), plot_data.shape_pt_lat.max())

    height = round(width * (y_range[1] - y_range[0]) / (x_range[1] - x_range[0]))

    cvs = ds.Canvas(
        plot_width=width,
        plot_height=height,
        x_range=x_range,
        y_range=y_range
    )

    layers = []
    for color, data_part in plot_data.groupby('route_color'):
        agg = cvs.line(
            data_part, 'shape_pt_lon', 'shape_pt_lat',
            agg=ds.sum('times_taken')
        )
        image_part = tf.shade(agg, cmap=['#000000', '#' + color], how='eq_hist')
        layers.append(image_part)

    image = tf.stack(*layers, how='add')

    if out.endswith('.png'):
        out = out[:-4]
    export_image(image, filename=out, background='black')


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-d', '--data',
        help="A line-plot-compatible data file",
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
        '-w', '--width',
        help="The width of the image in pixels",
        type=int,
        default=1600
    )

    args = parser.parse_args()

    create_plot(args.data, args.out, args.width)


if __name__ == "__main__":
    main()
