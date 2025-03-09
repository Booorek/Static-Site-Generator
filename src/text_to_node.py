from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:

            if node.text.count(delimiter) == 0:
                raise Exception("Delimiter not found")
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
