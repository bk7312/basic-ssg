import sys
# from textnode import *
from utils import replace_folder_with_static, generate_pages_recursive


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    # print("hello world")
    # text_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    # print(text_node)
    replace_folder_with_static("docs")

    # generate_pages_recursive("content", "template.html", "public", basepath)
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()