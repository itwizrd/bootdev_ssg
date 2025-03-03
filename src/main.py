from textnode import TextType, TextNode
from file_handling import recursive_copy,clear_directory


dir_static = "./static"
dir_public = "./public"


def main():
    clear_directory(dir_public)
    recursive_copy(dir_static,dir_public)



    
if __name__ == "__main__":
    main()
