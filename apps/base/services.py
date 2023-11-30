import os


def delete_of_file(path_file):
    """Deleting an old file
    """
    if os.path.exists(path_file):
        os.remove(path_file)
