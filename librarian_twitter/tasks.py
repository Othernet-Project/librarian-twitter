from .dirinfo import DirInfo


def check_new_dirinfo(supervisor, fsobj):
    if fsobj.name == DirInfo.FILENAME:
        DirInfo.from_file(supervisor, fsobj.path)
