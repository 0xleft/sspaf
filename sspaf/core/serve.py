import os
import time
import flask
import threading
from sspaf.core import render
import waitress

class ChangeDetector():
    def __init__(self, path: str):
        self.path = path
        self.last_modified = {}
        self.stop = False

    def run(self):
        previous_contents = set(os.listdir(self.path))
        while True:
            if self.stop:
                break
            current_contents = set(os.listdir(self.path))
            if current_contents != previous_contents:
                render.render(self.path)
                previous_contents = current_contents
            
            for filename in current_contents:
                file_path = os.path.join(self.path, filename)
                if os.path.isfile(file_path):
                    modification_time = os.path.getmtime(file_path)
                    if modification_time > self.last_modified.get(file_path, 0):
                        render.render(self.path)
                        self.last_modified[file_path] = modification_time
            
            time.sleep(1)

def serve(output_path: str) -> None:
    if output_path == ".":
        output_path = os.getcwd()

    print(f'Serving project {output_path}')

    app = flask.Flask(__name__, static_folder=os.path.join(output_path, 'output'))

    @app.route('/<path:path>')
    def send_file(path):
        try:
            return flask.send_file(output_path + '/output/' + path)
        except:
            return flask.send_file(output_path + '/output/index.html'), 404

    @app.route('/')
    def send_index():
        return flask.send_file(output_path + '/output/index.html')


    detector = ChangeDetector(output_path)
    thread = threading.Thread(target=detector.run)
    thread.start()

    render.render(output_path)
    print(f"Starting server on http://localhost:8080/")
    os.system("start http://localhost:8080/")
    waitress.serve(app, host='127.0.0.1', port=8080)
    detector.stop = True
    thread.join()