import os
import flask
import numpy
import cv2
import time
import json

DEFAULT_APP_NAME = __name__

class FlirNodeMData:

    def __init__(self, ns, ns_event):
        self.ns = ns
        self.ns_event = ns_event
        setattr(self.ns, FlirNodeMData.__name__, [None, None, None])

    def update(self, frame_id, frame_timestamp, cv_frame):
        setattr(self.ns, FlirNodeMData.__name__, [frame_id, frame_timestamp, cv_frame])
        self.ns_event.set()

    def read(self):
        return getattr(self.ns, FlirNodeMData.__name__)

    def read_cv_frame(self):
        return self.read_data()[1]
    
    def wait_for_data(self):
        return self.wait_for_frame_change(None)

    def wait_for_frame_change(self, frame_id):
        curr_data = self.read()
        while curr_data[0] == frame_id:
            self.ns_event.wait()
            curr_data = self.read()
        return curr_data

def create_app(flir_mdata,
               name=DEFAULT_APP_NAME, 
               default_log_level="INFO"):

    app = flask.Flask(name)

    log_level = os.environ.get(f"{app.name.upper()}_LOG_LEVEL", default_log_level)
    app.logger.setLevel(log_level)

    app.logger.info(f"Creating App {name}...")

    @app.route("/")
    def root():
        return send_static("index.html")


    @app.route("/<path:path>")
    def send_static(path):
        print(path)
        return flask.send_from_directory(os.path.join(os.path.dirname(__file__), "nodepageV2"), path)

    @app.route("/get_frame_data")
    def get_frame_data():
        _, _, data = flir_mdata.wait_for_data()
     
        return json.dumps(data)


    @app.route('/get_node_name')
    def get_node_name():

        return json.dumps([flir_mdata.ns.node_name])
 
    

    return app

def app_mworker(ns, ns_event, port):
    
    app = create_app(FlirNodeMData(ns, ns_event))
    app.run(host="0.0.0.0", port=port)
