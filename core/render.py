import os
import time

def render(path: str) -> None:
    if path == ".":
        path = os.getcwd()

    print(f'Rendering project {path}')
    start = time.time()

    try:
        os.makedirs(os.path.join(path, 'output'))
    except:
        for root, dirs, files in os.walk(os.path.join(path, 'output'), topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

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
            source = os.path.join(path, file)
            
            with open(source, 'r') as f:
                content = f.read().replace("\n", "").replace('"', '\\"').replace("'", "\\'")

            with open(os.path.join(path, 'output', file.replace(".html", ".json")), 'w+') as f:
                f.write(f'{{"title": "{file.replace(".html", "")}", "content": "{content}"}}')

            pages.append(file.replace(".html", ".json"))

    # copy assets/init.html from the spf folder
    source = os.path.join(os.path.dirname(__file__), 'assets', 'init.html')
    destination = os.path.join(path, 'output', 'index.html')

    with open(source, 'r') as f:
        content = f.read()

    with open(destination, 'w+') as f:
        f.write(content.replace("SPF_TITLE", "index"))
    
    source = os.path.join(os.path.dirname(__file__), 'assets', 'spf.js')
    destination = os.path.join(path, 'output', 'spf.js')

    with open(source, 'r') as f:
        content = f.read()

    content = content.replace("SPF_PAGES", pages.__str__())

    with open(destination, 'w') as f:
        f.write(content)

    end = time.time()
    print(f"The project was rendered in {end - start} seconds")