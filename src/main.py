from textnode import TextNode, TextType

def main():
    node = TextNode("this is some anchor text", TextType.BOLD)
    print(node.__repr__())
    # print("test")

if __name__ == "__main__":
    main()
