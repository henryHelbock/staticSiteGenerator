from textnode import TextNode, TextType

def split_nodes_delimiter(oldNodes, delimiter, textType):
    newNodes = []

    for node in oldNodes:
        # Pass through non-TEXT nodes unchanged
        if node.text_type != TextType.TEXT:
            newNodes.append(node)
            continue

        parts = node.text.split(delimiter)

        # Unmatched delimiter check
        if (len(parts) - 1) % 2 != 0:
            raise Exception("missing matching delimiter")

        # Determine starting type
        current_type = textType if parts[0] == "" else TextType.TEXT

        for part in parts:
            if part == "":
                continue

            newNodes.append(TextNode(part, current_type))

            # Alternate type after each real segment
            current_type = (
                textType if current_type == TextType.TEXT else TextType.TEXT
            )

    return newNodes
