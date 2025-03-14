import string


def markdown_to_blocks(markdown):
    texts = markdown.split("\n\n")
    texts = list(filter(lambda x: x != "", texts))
    stripped_texts = []
    for text in texts:
        stripped_texts.append(text.strip(string.whitespace))
    return stripped_texts
