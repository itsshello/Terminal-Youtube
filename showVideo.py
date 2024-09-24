import os
import cv2
import time
from PIL import Image

# Use a more detailed set of ASCII characters
ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,'\"^`'."

def map_pixels_to_ascii(image, ascii_chars=ASCII_CHARS):
    grayscale_image = image.convert("L")
    pixels = grayscale_image.getdata()

    # Map pixel values to ASCII characters
    ascii_str = ""
    range_width = 256 // len(ascii_chars)
    
    for pixel_value in pixels:
        ascii_str += ascii_chars[min(pixel_value // range_width, len(ascii_chars) - 1)]
    
    return ascii_str

def image_to_ascii(image, new_width):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)  # Adjust height to maintain aspect ratio

    resized_image = image.resize((new_width, new_height))

    ascii_str = map_pixels_to_ascii(resized_image)
    ascii_lines = [ascii_str[i:i + new_width] for i in range(0, len(ascii_str), new_width)]
    return "\n".join(ascii_lines)

def get_terminal_size():
    return os.get_terminal_size().columns, os.get_terminal_size().lines

def play_video_in_ascii(video_path, default_fps=10):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Dynamically get the terminal size and adjust the width accordingly
        terminal_width, _ = get_terminal_size()

        # Convert the frame to PIL image format
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Measure start time to calculate the rendering time
        start_time = time.time()

        # Convert the image to ASCII
        ascii_frame = image_to_ascii(pil_image, new_width=terminal_width)

        # Clear the terminal screen
        os.system('cls' if os.name == 'nt' else 'clear')

        # Print the ASCII frame
        print(ascii_frame)

        # Calculate rendering time and adjust sleep for FPS
        render_time = time.time() - start_time
        frame_delay = 1.0 / default_fps

        # If rendering time is greater than frame delay, skip sleep to maintain timing
        if render_time < frame_delay:
            time.sleep(frame_delay - render_time)

    cap.release()

# Example usage
video_path = "E:\\projs\\Python_Apps\\5_Terminal-Youtube\\Kita Ikuyo dances to doodle song (Bocchi The Rock!).mp4"
play_video_in_ascii(video_path)
