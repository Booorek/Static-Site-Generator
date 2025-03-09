class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        s = ""
        for item, value in self.props.items():
            s += f" {item}=\"{value}\""
        return s

    def __repr__(self):
        return f"HTMLNode {self.tag} {self.value} {self.children} {self.props}"

    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        else:
            return False


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf without value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent Node: Empty tag")
        if self.children is None:
            raise ValueError("Parent Node: No children")
        s = ""
        s += f"<{self.tag}{super().props_to_html()}>"
        if self.value is not None:
            s += f"{self.value}"
        if self.children is not None:
            for child in self.children:
                s += child.to_html()
        s += f"</{self.tag}>"
        return s
