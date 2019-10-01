import os

def is_subdir(test_path, root_path):
    path = os.path.realpath(test_path)
    directory = os.path.realpath(root_path)

    relative = os.path.relpath(path, directory)
    return not (relative == os.pardir or relative.startswith(os.pardir + os.sep))

def normalize_path(path_to_normalize):
    if path_to_normalize is None:
        return None

    normalized_path = os.path.normpath(
        os.path.normcase(
            os.path.abspath(
                os.path.expanduser(
                    path_to_normalize
                )
            )
        )
    )

    return normalized_path