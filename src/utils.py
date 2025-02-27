from enum import Enum
import re
import os
import shutil
from textnode import TextNode, TextType
from parentnode import ParentNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    if not isinstance(old_nodes, list):
        raise Exception("not a list")
    for n in old_nodes:
        if not isinstance(n, TextNode):
            raise Exception("non text node found in list")
        if n.text_type == TextType.TEXT:
            parts = n.text.split(delimiter)
            if len(parts) % 2 != 1:
                # print("invalid parts\n\n", parts)
                raise Exception("invalid markdown syntax")
            for i, p in enumerate(parts):
                if i % 2 == 0:
                    if p != "":
                        new_list.append(TextNode(p, TextType.TEXT))
                else:
                    new_list.append(TextNode(p, text_type))
        else:
            new_list.append(n)
    return new_list

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]):
    list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            list.append(node)
            continue
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            list.append(node)
            continue
        for image in images:
            before, node.text = node.text.split(f"![{image[0]}]({image[1]})", 1)
            list.extend([
                TextNode(before, TextType.TEXT), 
                TextNode(image[0], TextType.IMAGE, image[1]), 
            ])
        if node.text != "":
            list.append(TextNode(node.text, TextType.TEXT))
    return list

def split_nodes_link(old_nodes: list[TextNode]):
    list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            list.append(node)
            continue
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            list.append(node)
            continue
        for link in links:
            before, node.text = node.text.split(f"[{link[0]}]({link[1]})", 1)
            list.extend([
                TextNode(before, TextType.TEXT), 
                TextNode(link[0], TextType.LINK, link[1]), 
            ])
        if node.text != "":
            list.append(TextNode(node.text, TextType.TEXT))
    return list

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes


def markdown_to_blocks(markdown):
    lines = [stripped for line in markdown.split("\n\n") if (stripped := line.strip())]
    # lines = markdown.split("\n\n")
    # lines = list(map(lambda x: x.strip(), lines))
    # lines = list(filter(lambda x: x != "", lines))
    return lines


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown) -> BlockType:
    if len(re.findall(r"^#{1,6} ", markdown)) == 1:
        return BlockType.HEADING

    if markdown[:3] + markdown[-3:] == "``````":
        return BlockType.CODE
    
    lines = markdown.split("\n")
    
    is_quote = True
    is_ordered_list = True
    is_unordered_list = True
    for i, line in enumerate(lines):
        if not line.startswith(">"):
            is_quote = False
        if not line.startswith("* ") and not line.startswith("- "):
            is_unordered_list = False
        if not line.startswith(f"{i+1}. "):
            is_ordered_list = False
    
    if is_quote:
        return BlockType.QUOTE
    
    if is_unordered_list:
        return BlockType.UNORDERED_LIST
    
    if is_ordered_list:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH



def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children_list = []
    for block in blocks:
        type = block_to_block_type(block)
        # print("troubleshoot create html block\n\n", block, type)
        html_node = create_html_node(block, type)
        if html_node != None:
            children_list.append(html_node)

    return ParentNode("div", children_list)


def create_html_node(block, type):
    match type:
        case BlockType.QUOTE:
            # note: bootdev didn't wrap quote with p tag, I prefer with p tag
            quote = block.split("\n")
            text_nodes = [text_to_textnodes(q[1].strip()) for x in quote if (q := x.split(" ", 1)) and len(q) > 1]
            # text_nodes = list(map(lambda x: text_to_textnodes(x.split(" ", 1)[1].strip()), quote))
            leaf_nodes = [for_each_text_node_to_html_node(x) for x in text_nodes]
            # leaf_nodes = list(map(lambda x: for_each_text_node_to_html_node(x), text_nodes))
            children = [ParentNode("p", x) for x in leaf_nodes]
            # children = list(map(lambda x: ParentNode("p", x), leaf_nodes))
            return ParentNode("blockquote", children)
        
        case BlockType.UNORDERED_LIST:
            li = block.split("\n")
            text_nodes = [text_to_textnodes(l[1].strip()) for x in li if (l := x.split(" ", 1)) and len(l) > 1]
            # text_nodes = list(map(lambda x: text_to_textnodes(x.split(" ", 1)[1]), li))
            leaf_nodes = [for_each_text_node_to_html_node(x) for x in text_nodes]
            # leaf_nodes = list(map(lambda x: for_each_text_node_to_html_node(x), text_nodes))
            children = [ParentNode("li", x) for x in leaf_nodes]
            # children = list(map(lambda x: ParentNode("li", x), leaf_nodes))
            return ParentNode("ul", children)
        
        case BlockType.ORDERED_LIST:
            li = block.split("\n")
            text_nodes = [text_to_textnodes(l[1].strip()) for x in li if (l := x.split(". ", 1)) and len(l) > 1]
            # text_nodes = list(map(lambda x: text_to_textnodes(x.split(". ", 1)[1]), li))
            leaf_nodes = [for_each_text_node_to_html_node(x) for x in text_nodes]
            # leaf_nodes = list(map(lambda x: for_each_text_node_to_html_node(x), text_nodes))
            children = [ParentNode("li", x) for x in leaf_nodes]
            # children = list(map(lambda x: ParentNode("li", x), leaf_nodes))
            return ParentNode("ol", children)
        
        case BlockType.CODE:
            code = block[3:-3]#.split("\n")
            if len(code) == 0:
                return None
            # processes the text inside the code block, undesirable
            # text_nodes = text_to_textnodes(code)
            # print("code text", text_nodes)
            # leaf_nodes = list(map(lambda x: x.text_node_to_html_node(), text_nodes))
            # print("code leaf", leaf_nodes)
            # children = ParentNode("code", leaf_nodes)

            children = ParentNode("code", [TextNode(code.lstrip("\n"), TextType.TEXT).text_node_to_html_node()])
            # print("code children", children)
            return ParentNode("pre", [children])
        
        case BlockType.HEADING:
            heading, text = block.split(" ", 1)
            level = len(heading)
            text_nodes = text_to_textnodes(text)
            children = [x.text_node_to_html_node() for x in text_nodes]
            # children = list(map(lambda x: x.text_node_to_html_node(), text_nodes))
            return ParentNode(f"h{level}", children)
        
        case BlockType.PARAGRAPH:
            block = " ".join(block.split("\n")) # combines line break into single paragraph
            children = [x.text_node_to_html_node() for x in text_to_textnodes(block)]
            # children = list(map(lambda x: x.text_node_to_html_node(), text_to_textnodes(block)))
            return ParentNode("p", children)

def for_each_text_node_to_html_node(text_nodes):
    return [node.text_node_to_html_node() for node in text_nodes]

def replace_folder_with_static(folder):        
    if os.path.exists(folder):
        shutil.rmtree(folder)
    if not os.path.exists("static"):
        return
    copy_folder("static", folder)

    

def copy_folder(src, dest):
    if os.path.isfile(src):
        if src == ".DS_Store":
            return
        shutil.copy(src, dest)
        return
    os.mkdir(dest)
    files = os.listdir(src)
    for file in files:
        copy_folder(os.path.join(src, file), os.path.join(dest, file))
    


def extract_title(markdown):
    first_line = markdown.split("\n")[0].strip()
    if not first_line.startswith("# "):
        raise Exception("not valid h1")
    splitted = first_line.split(" ", 1)
    if len(splitted) < 2:
        raise Exception("invalid h1")
    return splitted[1]


def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    f = open(from_path)
    content = f.read()
    f.close()
    t = open(template_path)
    template = t.read()
    t.close()

    nodes = markdown_to_html_node(content)
    # html = list(map(lambda x: x.to_html(), nodes))
    # print("nodes\n\n", nodes)
    html = nodes.to_html()
    # print("htmlnodes\n\n", html)
    title = extract_title(content)
    with_title = template.replace("{{ Title }}", title)
    with_content = with_title.replace("{{ Content }}", html)
    update_href = with_content.replace('href="/', f'href="{basepath}')
    update_src = update_href.replace('src="/', f'src="{basepath}')
    o = open(dest_path, "w")
    o.write(update_src)
    o.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    files = os.listdir(dir_path_content)
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    for file in files:
        content_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(content_path):
            if file.endswith(".md"):
                print("generating file", content_path)
                html_filename = file[:-3] + ".html"
                generate_page(content_path, template_path, os.path.join(dest_dir_path, html_filename), basepath)
        else:
            generate_pages_recursive(content_path, template_path, dest_path, basepath)

