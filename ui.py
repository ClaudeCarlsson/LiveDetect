import cv2
import threading
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
from camera import Camera
from chatgpt_api import send_image_to_chatgpt

# Configure these according to your API details
CHATGPT_API_URL = "https://api.openai.com/v1/your-chatgpt-endpoint"
API_KEY = "your_api_key_here"

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Initialize the camera
        self.camera = Camera()

        # Create a canvas that can fit the video frame
        self.canvas = tk.Canvas(window, width=640, height=480)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot = Button(window, text="Capture and Send", width=50, command=self.capture_and_send)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

        self.delay = 15  # ms
        self.update()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def update(self):
        frame = self.camera.get_frame()
        if frame is not None:
            # Convert the image format (BGR -> RGB) for Tkinter
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2image))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(self.delay, self.update)

    def capture_and_send(self):
        frame = self.camera.get_frame()
        if frame is not None:
            # Optionally, perform some image processing or face recognition here.
            # Send the captured frame in a separate thread to avoid blocking the UI.
            threading.Thread(target=self.send_frame, args=(frame,)).start()

    def send_frame(self, frame):
        result = send_image_to_chatgpt(frame, CHATGPT_API_URL, API_KEY)
        print("Response from ChatGPT API:", result)

    def on_closing(self):
        self.camera.release()
        self.window.destroy()

def run_app():
    App(tk.Tk(), "Live Camera AI App")

if __name__ == '__main__':
    run_app()
