

import cv2
import os
from PIL import Image

ASCII_CHARS = "@%#*+=-:. "

def scale_image(image, new_width=100):
    (original_width, original_height) = image.size
    aspect_ratio = original_height / original_width
    new_height = int(aspect_ratio * new_width * 0.55)  # Adjust for terminal aspect ratio
    return image.resize((new_width, new_height))

def convert_grayscale(image):
    return image.convert("L")

def map_pixels_to_ascii(image, range_width=25):
    pixels = image.getdata()
    ascii_str = ""
    for pixel_value in pixels:
        ascii_str += ASCII_CHARS[pixel_value // range_width]
    return ascii_str

def image_to_ascii(image, new_width=100):
    image = scale_image(image, new_width)
    image = convert_grayscale(image)
    ascii_str = map_pixels_to_ascii(image)
    img_width = image.width
    ascii_str_len = len(ascii_str)
    ascii_img = ""
    # Split the ASCII string based on the image width
    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i:i + img_width] + "\n"
    return ascii_img

def play_video_in_ascii(video_path, new_width=100):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return
    
    try:
        os.system("cls" if os.name == "nt" else "clear")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert frame (numpy array) to PIL Image
            pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            # Convert image to ASCII
            ascii_frame = image_to_ascii(pil_image, new_width)
            
            # Print the ASCII art frame
            os.system("cls" if os.name == "nt" else "clear")
            print(ascii_frame)
            
            # Optional: Slow down frame rate (adjust for different frame rates)
            cv2.waitKey(50)  # Adjust to control frame rate (1000ms / 50 = 20 FPS)
    
    finally:
        cap.release()
        cv2.destroyAllWindows()

# Example usage
# video_path = input("Enter the path to the video file: ")
play_video_in_ascii("E:\\projs\\Python_Apps\\5_Terminal-Youtube\\Kita Ikuyo dances to doodle song (Bocchi The Rock!).webm", new_width=100)
