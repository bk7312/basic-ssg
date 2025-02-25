
from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):
        if self.value == None:
            raise ValueError("missing value")
        if self.tag == None:
            return self.value
        prop = ""
        if self.props != None:
            prop = self.props_to_html()
        return f"<{self.tag}{prop}>{self.value}</{self.tag}>"
