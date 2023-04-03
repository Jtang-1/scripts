import os
import mimetypes
from enum import Enum
import shutil

mimetypes.init()

root = "/Users/Josephtang/"
dir_to_analyze = "Downloads"

class Directories(Enum): 
    directory = os.path.join(root, dir_to_analyze)
    new_media_dir = os.path.join(root, dir_to_analyze+"_media")
    new_not_media_dir = os.path.join(root, dir_to_analyze+ "_not_media")

for dir in [key.value for key in Directories]:
    if not os.path.exists(dir):
        os.makedirs(dir)


def is_media(filename:str):
    mimestart = mimetypes.guess_type(filename)[0]
    if mimestart != None:
        mimestart = mimestart.split('/')[0]
        if mimestart in ['audio', 'video','image']:
            return True
    return False

def copy_src_to_dst(src:str, dst:str):
    if os.path.isfile(src):
        pass
        shutil.copy2(src, dst)
    elif os.path.isdir(src):
        suffix = os.path.relpath(src, Directories.directory.value)
        dir = os.path.basename(os.path.normpath(src))
        dst = os.path.join(dst, suffix)
        print("dst is", dst)
        shutil.copytree(src,dst)

def copy_to_not_media(src):
    copy_src_to_dst(src, Directories.new_not_media_dir.value)

def copy_to_media(src):
    copy_src_to_dst(src, Directories.new_media_dir.value)

visited_dir_with_media = set()

for root,dirs,files in os.walk(Directories.directory.value):
    if root in visited_dir_with_media:
        for dir in dirs:
            visited_dir_with_media.add(os.path.join(root,dir))
        continue
    for filename in files:
        file = os.path.join(root, filename)
        is_media_files = set()
        if is_media(filename):
            has_not_found_media_in_dir = root not in visited_dir_with_media and root!=Directories.directory.value
            is_media_files.add(file)
            if has_not_found_media_in_dir:
                visited_dir_with_media.add(root)
                for dir in dirs:
                    visited_dir_with_media.add(os.path.join(root,dir))
                copy_to_media(root)
                break
        for file in is_media_files:
            copy_to_media(file)

