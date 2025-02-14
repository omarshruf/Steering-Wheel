import tkinter as tk
from PIL import Image, ImageTk
import threading
import math
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os

MyRespone = 0

class RequestHandler_httpd(BaseHTTPRequestHandler):
    def do_GET(self):
        global MyRespone
        MyRequest = self.requestline
        MyRequest = MyRequest[5 : int(len(MyRequest) - 9)].strip()

        if MyRequest.isdigit() or (MyRequest.startswith('-') and MyRequest[1:].isdigit()):
            MyRespone = int(MyRequest)

        messagetosend = bytes('Received', "utf-8")
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', len(messagetosend))
        self.end_headers()
        self.wfile.write(messagetosend)

def run_server():
    """Starts the HTTP server in a separate thread."""
    HOST = '0.0.0.0'
    PORT = 8080
    server_address_httpd = (HOST, PORT)
    httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
    print(f"Starting Server on {HOST}:{PORT}")
    httpd.serve_forever()

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

class SteeringWheelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steering Wheel Control")
        
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        self.smoothed_response = 0.0
        self.smoothing_factor = 5.0

        image_path = "SteerWheel.jpg"
        if os.path.exists(image_path):
            self.original_image = Image.open(image_path)
        else:
            self.original_image = Image.new("RGB", (200, 200), "gray")

        self.original_image = self.original_image.resize((200, 200), Image.Resampling.LANCZOS)
        self.image = ImageTk.PhotoImage(self.original_image)
        self.image_id = self.canvas.create_image(200, 200, image=self.image)

        self.move_mouse_enabled = False
        self.last_update_time = time.time()

        self.update_rotation()

    def update_rotation(self):
        """Updates rotation and mouse movement with smooth transitions."""
        global MyRespone

        # Update rotation display immediately
        if isinstance(MyRespone, (int, float)):
            rotated_image = self.original_image.rotate(-MyRespone)
            self.image = ImageTk.PhotoImage(rotated_image)
            self.canvas.itemconfig(self.image_id, image=self.image)

        self.root.after(10, self.update_rotation)

root = tk.Tk()
app = SteeringWheelApp(root)
root.mainloop()
