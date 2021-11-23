"""
    Heuristic to figure out fixes in files based on diff analysis.
    For now, supports only single-file diffs. Will add support for multi-file filtering out later
"""

def is_file_relevant(filename):
    valid_exts = [".c", ".cpp"]
    for ext in valid_exts:
        if filename.endswith(ext):
            return True
    return False


def get_relevant_files(diff_lines):
    