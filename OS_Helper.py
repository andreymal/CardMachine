'''
OS Helpers
'''
import os
import glob
import PIL_Helper


def Delete(filename):
    filelist = glob.glob(filename)
    for f in filelist:
        os.remove(f)


def CleanDirectory(path=".", mkdir="workspace", rmstring="*.*"):
    dir_path = os.path.join(path, mkdir)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    else:
        Delete(os.path.join(dir_path, rmstring))
    return dir_path


def BuildPage(card_list, page_num, workspace_path, extension, *args, **kwargs):
    kwargs['filename'] = os.path.join(workspace_path, "page_{0:>03}.{1}".format(page_num, extension))
    PIL_Helper.BuildPage(card_list, *args, **kwargs)


def BuildBack(card_list, page_num, workspace_path, extension, *args, **kwargs):
    kwargs['filename'] = os.path.join(workspace_path, "backs_{0:>03}.{1}".format(page_num, extension))
    kwargs['reverse'] = True
    PIL_Helper.BuildPage(card_list, *args, **kwargs)
