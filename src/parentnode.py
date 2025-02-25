
from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag == None:
            raise ValueError("missing tag")
        if self.children == None or not isinstance(self.children, list) or len(self.children) < 1:
            raise ValueError("missing children")
        prop = ""
        if self.props != None:
            prop = self.props_to_html()
        children = ""
        for child in self.children:
            children += child.to_html()
        return f"<{self.tag}{prop}>{children}</{self.tag}>"
