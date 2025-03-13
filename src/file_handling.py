from os.path import exists,join,isfile,isdir,dirname
from os import listdir,mkdir,makedirs
from shutil import copy,rmtree
import logging
from inline_markdown import extract_title
from markdown_blocks import markdown_to_html_node

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
                logging.info(f"Copying file: {source_path} --> {dest_path}")
                copy(source_path,dest_path)
            except Exception as e:
                logging.error(f"Failed to copy {source_path}: {e}")
        elif isdir(source_path):        
            recursive_copy(source_path,dest_path)
        else:
            logging.warning(f"Skipping {source_path}: Neither a file nor a directory")

def generate_page(from_path, template_path, dest_path, BASEPATH):
    logging.info(f"Generating page: {from_path} --> {dest_path}, using {template_path}")
    # Ensures dest_dir exists
    dir_path = dirname(dest_path)
    if dir_path:
        makedirs(dir_path, exist_ok=True)
    # Read Markdown file
    with open(from_path, 'r') as f_file:
        from_file = f_file.read()
    # Read Template File
    with open(template_path, 'r') as t_file:
        template_file = t_file.read()
    # Extracts title
    title = extract_title(from_file)
    # Convert markdown to HTML
    html_string = markdown_to_html_node(from_file).to_html()
    # Replace Placeholders
    final_html = template_file.replace('{{ Title }}', title).replace('{{ Content }}', html_string).replace('href="/', f'href="{BASEPATH}').replace('src="/', f'src="{BASEPATH}')
    # Writes to content to dest_path file
    with open(dest_path, 'w') as d_file:
        d_file.write(final_html)

def recursive_gen(from_path, template_path, dest_path, BASEPATH):
    logging.info(f"Basepath = {BASEPATH}")
    for item in listdir(from_path):
        source_path = join(from_path,item)
        destination = join(dest_path,item)
        if isfile(source_path):
            if source_path.endswith('.md'):
                try:
                    logging.info(f"Generating HTML: {source_path} --> {destination}")
                    destination = destination.replace('.md', '.html')
                    generate_page(source_path, template_path, destination, BASEPATH)
                except Exception as e:
                    logging.error(f"Failed to generate {source_path}: {e}")
            else:
                logging.info(f"Skipping non-markdown file {source_path}")
        elif isdir(source_path):
            if not exists(destination):
                logging.info(f"Creating Directory {destination}")
                mkdir(destination)
            recursive_gen(source_path, template_path, destination, BASEPATH)
        else:
            logging.warning(f"Skipping {source_path}: neither a file nor directory")