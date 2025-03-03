from os.path import exists,join,isfile,isdir
from os import listdir,mkdir
from shutil import copy,rmtree
import logging

logging.basicConfig(level=logging.INFO,format='%(message)s')

def clear_directory(dir):
    if exists(dir):
        logging.info(f"Clearing directory: {dir}")
        rmtree(dir)
    logging.info(f"Creating directory: {dir}")
    mkdir(dir)

def recursive_copy(static_dir, public_dir):
    if not exists(public_dir):
        logging.info(f"Creating directory: {public_dir}")
        mkdir(public_dir)
    if not exists(static_dir):
        raise FileNotFoundError("FileNotFound: Static directory not found")

    for item in listdir(static_dir):
        source_path = join(static_dir,item)
        dest_path = join(public_dir,item)

        if isfile(source_path):
            try:
                logging.info(f"Copying file: {source_path} -> {dest_path}")
                copy(source_path,dest_path)
            except Exception as e:
                logging.error(f"Failed to copy {source_path}: {e}")
        elif isdir(source_path):        
            recursive_copy(source_path,dest_path)
        else:
            logging.warning(f"Skipping {source_path}: Neither a file nor a directory")