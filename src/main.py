from textnode import TextType, TextNode

print("hello world")
def main():
    text = "This is a text node"
    text_type = TextType.BOLD
    url = "https://www.boot.dev"
    print(TextNode(text, text_type, url))

    
if __name__ == "__main__":
    main()
