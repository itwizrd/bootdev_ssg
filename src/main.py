import sys
from file_handling import recursive_copy,clear_directory,recursive_gen
import inline_markdown

basepath = sys.argv[1] if len(sys.argv) > 1 else '/'
dir_static = "./static"
dir_public = "./docs"
dir_content = "./content"
file_template = "./src/template.html"


def main():
    clear_directory(dir_public)
    recursive_copy(dir_static,dir_public)
    recursive_gen(dir_content, file_template, dir_public, basepath)



    
if __name__ == "__main__":
    main()
