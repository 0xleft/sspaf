import os
import time
import render

def publish(path: str) -> None:
    if path == ".":
        path = os.getcwd()

    print(f'Publishing project {path}')
    start = time.time()

    render.render(path, dev=False)

    print(f'Published project {path} in {time.time() - start} seconds')
    print(f'Project published to {os.path.join(path, "output")}')