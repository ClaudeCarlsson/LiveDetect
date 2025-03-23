import cv2
import requests
import base64
from io import BytesIO
from PIL import Image

def image_to_base64(frame):
    # Convert an OpenCV image (BGR) to base64 (assume JPEG)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(frame_rgb)
    buffer = BytesIO()
    pil_img.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def send_image_to_chatgpt(frame, api_url, api_key):
    img_base64 = image_to_base64(frame)
    # Construct the payload. Adjust the prompt or field names as needed.
    payload = {
        "prompt": "Analyze the image data provided.",
        "image": img_base64,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()
