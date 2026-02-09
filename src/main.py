from textnode import TextNode, TextType
from markdown import markdown_to_html_node, extract_title
import os
import sys
import shutil


def generation(src, dest):
    for item in os.listdir(src):
        src_path =  os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            os.mkdir(dest_path)
            generation(src_path,dest_path)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")    
    with open(from_path, "r") as file:
        content = file.read()
        with open(template_path, "r") as file2:
            content2 = file2.read()
            html = markdown_to_html_node(content)
            html = html.to_html()
            title = extract_title(content)

            page = content2.replace("{{ Title }}", title)
            page = page.replace("{{ Content }}", html)

            page = page.replace('href="/', f'href="{basepath}')
            page = page.replace('src="/', f'src="{basepath}')

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path, "w") as f:
                f.write(page)

def generate_pages_recursive(dir_path_content, template_path, des_dir_path, basepath):
    paths = os.listdir(dir_path_content)

    for item in paths:
        src_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(des_dir_path, item)


        if os.path.isfile(src_path):
            if src_path.endswith(".md"):
                dest_path = os.path.join(des_dir_path, item.replace(".md", ".html"))
                generate_page(src_path, template_path, dest_path, basepath)

        else:
            os.mkdir(dest_path)
            generate_pages_recursive(src_path, template_path, dest_path, basepath)




def main():
    node = TextNode("this is some anchor text", TextType.BOLD)
    print(node.__repr__())

    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.mkdir("docs")

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    generation("static", "docs")

    generate_pages_recursive("content", "template.html", "docs", basepath)

    
    

if __name__ == "__main__":
    main()
