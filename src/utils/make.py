import re
import os


def find_input_files(tex_file):
    """Find all of the files that are included, inputted or includegraphics'd
    in a tex file.

    Args:
        tex_file: The path of the tex file.

    Returns:
        List[str]: the list of included files
    """

    with open(tex_file, 'r') as file:
        tex_contents = file.read()

    patterns = [
        re.compile(r"\\input\{(.*)\}"),
        re.compile(r"\\include\{(.*)\}"),
        re.compile(r"\\includegraphics(?:\[.*\])?\{(.*)\}")
    ]

    paths = sum((pattern.findall(tex_contents) for pattern in patterns), [])

    return [os.path.normpath(path) for path in paths]


def join(path1, path2):
    """Join and normalize two paths.

    Args:
        path1: a path string
        path2: a path string

    Returns:
        str: a path string
    """

    return os.path.normpath(os.path.join(path1, path2))
