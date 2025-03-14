from textnode import TextType, TextNode
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:

            if node.text.count(delimiter) % 2 != 0:
                raise Exception("Wrong format! Delimiter section not closed")
            temp_text = node.text.split(delimiter)
            i = 0
            for sentence in temp_text:
                if sentence == "":
                    i += 1
                    continue
                if i % 2 != 0:
                    new_nodes.append(TextNode(sentence, text_type))
                    i += 1
                else:
                    new_nodes.append(TextNode(sentence, TextType.TEXT))
                    i += 1
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)]\(([^()]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)]\(([^()]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(TextNode(node.text, node.text_type, node.url or None))
            continue

        segments = []
        last_indx = 0

        for image_alt, image_link in images:
            match = f"![{image_alt}]({image_link})"
            start = node.text.find(match, last_indx)

            if start > last_indx:
                segments.append(node.text[last_indx:start])

            segments.append((image_alt, image_link))

            last_indx = start + len(match)

        if last_indx < len(node.text):
            segments.append(node.text[last_indx:])
        for item in segments:
            if isinstance(item, tuple):
                new_nodes.append(TextNode(item[0], TextType.IMAGE, item[1]))
            else:
                new_nodes.append(TextNode(item, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(TextNode(node.text, node.text_type, node.url or None))
            continue

        segments = []
        last_indx = 0

        for link_alt, link_link in links:
            match = f"[{link_alt}]({link_link})"
            start = node.text.find(match, last_indx)

            if start > last_indx:
                segments.append(node.text[last_indx:start])

            segments.append((link_alt, link_link))

            last_indx = start + len(match)

        if last_indx < len(node.text):
            segments.append(node.text[last_indx:])
        for item in segments:
            if isinstance(item, tuple):
                new_nodes.append(TextNode(item[0], TextType.LINK, item[1]))
            else:
                new_nodes.append(TextNode(item, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    delimiters = [('**', TextType.BOLD), ('_', TextType.ITALIC), ('`', TextType.CODE)]
    new_nodes = [TextNode(text, TextType.TEXT)]
    for delimiter, conversion_type in delimiters:
        new_nodes = split_nodes_delimiter(new_nodes, delimiter, conversion_type)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes
