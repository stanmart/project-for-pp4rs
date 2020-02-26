import os
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

    with requests.get(url, stream=True) as req:
        req.raise_for_status()
        for chunk in req.iter_content(chunk_size=8192):
            if chunk:  # filter out keep-alive new chunks
                file.write(chunk)

    print(f"Succesfully downloaded file from {url}")


def extract_file(file, out_dir):
    """Extract the contents of a zip file to a directory

    Args:
        file: an open file object in binary mode
        out_dir: a path to the directory where the file will be extracted. Will
            be created if it does not exist.
    """
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    elif not os.path.isdir():
        raise NotADirectoryError("The object at out_dir exists but is not a directory")

    with zipfile.ZipFile(file) as temp_zip:
        temp_zip.extractall(out_dir)

    print(f"Contents unpacked succesfully to {out_dir}")


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
