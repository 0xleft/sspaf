import os
import time
from core.assets import init, js
import shutil

def render(path: str, dev=True) -> None:
    if path == ".":
        path = os.getcwd()

    start = time.time()

    # remove output folder
    shutil.rmtree(os.path.join(path, 'output'), ignore_errors=True)

    # create output folder
    os.makedirs(os.path.join(path, 'output'), exist_ok=True)

    # create the expected folder structure using os.walk
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if dir == 'output':
                continue
            os.makedirs(os.path.join(path, 'output', dir), exist_ok=True)

    # copy all the fiels from the main folder
    for file in os.listdir(path):
        if file.endswith('.html'):
            continue
        if shutil.os.path.isdir(os.path.join(path, file)):
            continue
        # TODO no
        try:
            shutil.copy(os.path.join(path, file), os.path.join(path, 'output', file))
        except shutil.SameFileError:
            pass

    # copy all non html files to the output folder and the expected folders
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if "output" in dir:
                continue
            for file in os.listdir(os.path.join(root, dir)):
                if file.endswith('.html'):
                    continue
                # TODO no
                try:
                    shutil.copy(os.path.join(root, dir, file), os.path.join(path, 'output', dir, file))
                except shutil.SameFileError:
                    pass

    # create the acording json files for all html files in the expected folders
    # main folder
    init_path(path, "")

    # subfolders
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if "output" in dir:
                continue
            init_path(root, dir)

    end = time.time()
    print(f"The project was rendered in {end - start} seconds")


def init_path(root: str, path: str) -> None:
    # TODO no
    if "output" in root:
        return

    pages = []

    # create all the json files
    for file in os.listdir(os.path.join(root, path)):
        if file.endswith("header.html") or file.endswith("footer.html") or not file.endswith('.html'):
            continue

        pages.append(file.replace(".html", ".json"))

        html_handle = open(os.path.join(root, path, file), "r")
        page_content = html_handle.read().replace("\n", "").replace('"', '\\"').replace("'", "\\'")
        html_handle.close()

        json_handle = open(os.path.join(root, 'output', path, file.replace(".html", ".json")), "w+")
        json_handle.write(f'{{"title": "{file.replace(".html", "")}", "content": "{page_content}"}}')
        json_handle.close()


        # create the index page for all the files
        init_page_content = init.page
        init_page_content = init_page_content.replace("SSPAF_TITLE", file.replace(".html", ""))
        init_page_content = init_page_content.replace("SSPAF_INDEX", page_content)

        try:
            header_handle = open(os.path.join(root, path, "header.html"), "r")
            header_content = header_handle.read()
            header_handle.close()
        except FileNotFoundError:
            header_content = ""

        try:
            footer_handle = open(os.path.join(root, path, "footer.html"), "r")
            footer_content = footer_handle.read()
            footer_handle.close()
        except FileNotFoundError:
            footer_content = ""

        init_page_content = init_page_content.replace("SSPAF_HEADER", header_content)
        init_page_content = init_page_content.replace("SSPAF_FOOTER", footer_content)

        init_page_handle = open(os.path.join(root, 'output', path, file), "w+")
        init_page_handle.write(init_page_content)
        init_page_handle.close()

    # create the sspaf.js file
    js_content = js.page
    js_content = js_content.replace("SSPAF_PAGES", str(pages))
    
    js_handle = open(os.path.join(root, 'output', path, 'sspaf.js'), "w+")
    js_handle.write(js_content)
    js_handle.close()