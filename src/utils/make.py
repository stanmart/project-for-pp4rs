import re


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

    return sum((pattern.findall(tex_contents) for pattern in patterns), [])
