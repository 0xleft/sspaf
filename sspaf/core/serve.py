import os
import time
import flask
import threading
from sspaf.core import render
import waitress

class ChangeDetector():
    def __init__(self, path: str):
        super().__init__()
        self.path = path
        self.stop = False

    def get_directory_snapshot(self, path):
        snapshot = {}
        for root, dirs, files in os.walk(path):
            # ignore output folder
            if "output" in root:
                continue
            for file in files:
                path = os.path.join(root, file)
                with open(path, 'rb') as f:
                    snapshot[path] = hash(f.read())
        return snapshot

    def detect_changes(self):
        while True:
            if self.stop:
                return
            snapshot = self.get_directory_snapshot(self.path)
            if snapshot != self.snapshot:
                self.snapshot = snapshot
                render.render(self.path)
            time.sleep(1)

    @staticmethod
    def run(path: str):
        detector = ChangeDetector(path)
        detector.snapshot = detector.get_directory_snapshot(path)
        thread = threading.Thread(target=detector.detect_changes)
        thread.start()

        return detector

def serve(output_path: str) -> None:
    if output_path == ".":
        output_path = os.getcwd()

    print(f'Serving project {output_path}')

    app = flask.Flask(__name__, static_folder=os.path.join(output_path, 'output'))

    @app.route('/sspaf.js')
    def send_sspaf():
        return flask.send_file(output_path + '/output/sspaf.js')
    
    # jsons
    @app.route('/<path:path>.json')
    def send_json(path):
        return flask.send_file(output_path + '/output/' + path + '.json')

    @app.route('/')
    def send_index():
        return flask.send_file(output_path + '/output/index.html')

    @app.route('/<path:path>')
    def send_page(path):
        return flask.send_file(output_path + '/output/' + path)

    detector = ChangeDetector.run(output_path)
    render.render(output_path)
    print(f"Starting server on http://localhost:8080/")
    os.system("start http://localhost:8080/")
    waitress.serve(app, host='127.0.0.1', port=8080)
    detector.stop = True
    print(f'Stopped server on http://localhost:8080/')