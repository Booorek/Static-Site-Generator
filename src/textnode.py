from enum import Enum


class TextType(Enum):
    TEXT = "Normal text"
    BOLD = "**BOLD text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        if self.text_type not in TextType:
            raise Exception("\nUnrecognized text type\n")
        self.url = url

    def __eq__(self, other):
        if self.text_type == other.text_type and self.text == other.text and self.url == other.url:
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
