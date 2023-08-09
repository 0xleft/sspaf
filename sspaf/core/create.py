import os
import time

def create(path: str) -> None:
    if path == ".":
        path = os.getcwd()

    print(f'Creating project {path}')
    start = time.time()

    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, 'index.html'), 'w+') as f:
        f.write(
"""
<h1>Hello, World!</h1>
""")
    
    with open(os.path.join(path, 'header.html'), 'w+') as f:
        f.write(
"""
<header>
    <a href="#index">Home</a>
</header>
""")
        
    with open(os.path.join(path, 'footer.html'), 'w+') as f:
        f.write(
"""
<footer>
    <p>Footer</p>
</footer>
""")