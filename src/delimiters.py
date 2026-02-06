def split_nodes_delimiter(old_nodes, delimiter, text_type):
    from textnode import TextNode, TextType
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        if delimiter not in old_node.text:
            new_nodes.append(old_node)
            continue

        sections = old_node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")

        is_text = True  # start in TEXT mode

        for section in sections:
            if section == "":
                is_text = not is_text
                continue

            if is_text:
                new_nodes.append(TextNode(section, TextType.TEXT))
            else:
                new_nodes.append(TextNode(section, text_type))

            is_text = not is_text

    return new_nodes

