import requests
import argparse
import zipfile
import tempfile


def download_file(url, file):
    """Downloads the file located at `url` and saves it to the
    open file `file`.

    Args:
        url: the URL of the file to download
        file: an open file object in binary write mode

    Returns:
        None
    """
    ...


def extract_file(file, out_dir):
    """Extract the contents of a zip file to a directory

    Args:
        file: an open file object in binary mode
        out_dir: a path to the directory where the file will be extracted. Will
            be created if it does not exist.
    """
    ...


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-u', '--url',
        help="The URL to the GTFS file",
        type=str
    )
    parser.add_argument(
        '-o', '--out-dir',
        help="The diractory where the GTFS file is extracted",
        type=str
    )

    args = parser.parse_args()

    with tempfile.TemporaryFile('wb') as file:
        download_file(args.u, file)
        extract_file(file, args.o)


if __name__ == "__main__":
    main()
