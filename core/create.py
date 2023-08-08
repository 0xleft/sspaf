import os
import time

def create(path: str) -> None:
    if path == ".":
        path = os.getcwd()

    print(f'Creating project {path}')
    start = time.time()

    os.makedirs(path, exist_ok=True)
    os.makedirs(os.path.join(path, 'src'), exist_ok=True)


