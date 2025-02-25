
from textnode import *
from utils import replace_public_with_static, generate_pages_recursive


def main():
    # print("hello world")
    # text_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    # print(text_node)
    replace_public_with_static()

    generate_pages_recursive("content", "template.html", "public")

main()