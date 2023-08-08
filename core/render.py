import os
import time

def render(path: str, dev=True) -> None:
    if path == ".":
        path = os.getcwd()

    print(f'Rendering project {path}')
    start = time.time()

    try:
        os.makedirs(os.path.join(path, 'output'))
    except:
        for root, dirs, files in os.walk(os.path.join(path, 'output'), topdown=False):
            for name in files:
                try:
                    os.remove(os.path.join(root, name))
                except:
                    pass
            for name in dirs:
                try:
                    os.rmdir(os.path.join(root, name))
                except:
                    pass

    # copy all non html files to the output folder
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".html"):
                continue

            source = os.path.join(root, file)
            destination = os.path.join(root.replace(path, os.path.join(path, 'output')), file)

            os.makedirs(os.path.dirname(destination), exist_ok=True)
            with open(source, 'r') as f:
                content = f.read()

            with open(destination, 'w+') as f:
                f.write(content)

    pages = []

    # render all html files
    for file in os.listdir(path):
        if file.endswith(".html"):
            if file.endswith("header.html") or file.endswith("footer.html"):
                continue
            source = os.path.join(path, file)
            
            with open(source, 'r') as f:
                content = f.read().replace("\n", "").replace('"', '\\"').replace("'", "\\'")

            with open(os.path.join(path, 'output', file.replace(".html", ".json")), 'w+') as f:
                f.write(f'{{"title": "{file.replace(".html", "")}", "content": "{content}"}}')

            pages.append(file.replace(".html", ".json"))

            # copy assets/init.html from the spf folder
            source = os.path.join(os.path.dirname(__file__), 'assets', 'init.html')
            destination = os.path.join(path, 'output', file)

            with open(source, 'r') as f:
                content = f.read()

            try:
                with open(os.path.join(path, file), 'r') as index:
                    index_content = index.read()
            except:
                index_content = ""
            content = content.replace("SPF_INDEX", index_content)

            try:
                with open(os.path.join(path, 'header.html'), 'r') as header:
                    header_content = header.read()
            except:
                header_content = ""
            content = content.replace("SPF_HEADER", header_content)

            try:
                with open(os.path.join(path, 'footer.html'), 'r') as footer:
                    footer_content = footer.read()
            except:
                footer_content = ""
            content = content.replace("SPF_FOOTER", footer_content)


            with open(destination, 'w+') as f:
                f.write(content.replace("SPF_TITLE", "index"))


    source = os.path.join(os.path.dirname(__file__), 'assets', 'spf.js')
    destination = os.path.join(path, 'output', 'spf.js')

    with open(source, 'r') as f:
        content = f.read()

    content = content.replace("SPF_PAGES", pages.__str__())

    if dev:
        content = content.replace("SPF_DEV",
"""
""")
    else:
        content = content.replace("SPF_DEV", "")

    with open(destination, 'w+') as f:
        f.write(content)

    end = time.time()
    print(f"The project was rendered in {end - start} seconds")