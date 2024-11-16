import os
import cv2
import time
import threading
import pygame
from PIL import Image

ASCII_CHARS = "@%#*+=-:. "

def map_pixels_to_ascii(image, ascii_chars=ASCII_CHARS):
    grayscale_image = image.convert("L")
    pixels = grayscale_image.getdata()

    ascii_str = ""
    range_width = 256 // len(ascii_chars)
    
    for pixel_value in pixels:
        ascii_str += ascii_chars[min(pixel_value // range_width, len(ascii_chars) - 1)]
    
    return ascii_str

def image_to_ascii(image, new_width):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)

    resized_image = image.resize((new_width, new_height))
    ascii_str = map_pixels_to_ascii(resized_image)
    ascii_lines = [ascii_str[i:i + new_width] for i in range(0, len(ascii_str), new_width)]
    return "\n".join(ascii_lines)

def get_terminal_size():
    return os.get_terminal_size().columns, os.get_terminal_size().lines - 5

def play_audio(audio_path):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

def get_audio_length(audio_path):
    pygame.mixer.init()
    audio = pygame.mixer.Sound(audio_path)
    return audio.get_length()

def get_audio_time():
    return pygame.mixer.music.get_pos() / 1000.0

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"

def display_progress(audio_time, video_time, audio_duration, video_duration, terminal_width, current_fps):
    audio_str = f"{format_time(audio_time)} / {format_time(audio_duration)}"
    video_str = f"{format_time(video_time)} / {format_time(video_duration)}"

    bar_width = terminal_width - max(len(audio_str), len(video_str)) - 10 - 8  # Adjust for FPS display
    audio_progress = min(audio_time / audio_duration, 1.0)
    video_progress = min(video_time / video_duration, 1.0)

    audio_bar = int(audio_progress * bar_width)
    video_bar = int(video_progress * bar_width)

    audio_bar_str = "[" + "#" * audio_bar + "-" * (bar_width - audio_bar) + "]"
    video_bar_str = "[" + "#" * video_bar + "-" * (bar_width - video_bar) + "]"

    # Add FPS display on the left side of the progress bar
    fps_display = f"FPS: {current_fps:.2f}  "

    print(f"{fps_display}Audio: {audio_bar_str} {audio_str}")
    print(f"{fps_display}Video: {video_bar_str} {video_str}")

def play_video_in_ascii(video_path, audio_path, initial_fps=10, fps_adjust_rate=0.5, max_fps=60, min_fps=1):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_duration = total_frames / fps
    audio_duration = get_audio_length(audio_path)

    audio_thread = threading.Thread(target=play_audio, args=(audio_path,))
    audio_thread.start()

    start_time = time.time()
    frame_idx = 0
    last_frame_time = 0
    target_fps = initial_fps
    fps_counter_start_time = time.time()

    while frame_idx < total_frames:
        try:
            ret, frame = cap.read()
            if not ret:
                break

            terminal_width, _ = get_terminal_size()

            video_time = frame_idx / fps
            real_time = time.time() - start_time
            audio_time = get_audio_time()

            # Skip frames if the video is way ahead of the audio
            if video_time < audio_time:
                frame_idx += 1
                continue

            # Calculate FPS for this frame
            frame_render_time = time.time() - fps_counter_start_time
            current_fps = 1.0 / frame_render_time if frame_render_time > 0 else 0
            fps_counter_start_time = time.time()

            # Convert frame to ASCII every target_fps interval
            if real_time - last_frame_time > 1.0 / target_fps:
                pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                ascii_frame = image_to_ascii(pil_image, new_width=terminal_width)

                os.system('cls' if os.name == 'nt' else 'clear')
                print(ascii_frame)

                last_frame_time = real_time

            # Display progress bar along with the current FPS
            display_progress(audio_time, video_time, audio_duration, video_duration, terminal_width, current_fps)

            # Sync adjustment logic
            sync_diff = audio_time - video_time

            # More aggressive FPS adjustments based on sync difference
            if sync_diff > 0.02:  # Video is behind audio, speed up more aggressively
                target_fps = min(target_fps + (fps_adjust_rate * abs(sync_diff) * 5), max_fps)
            elif sync_diff < -0.02:  # Video is ahead of audio, slow down more aggressively
                target_fps = max(target_fps - (fps_adjust_rate * abs(sync_diff) * 5), min_fps)

            time.sleep(max(1.0 / target_fps, 0))
            frame_idx += 1

        except KeyboardInterrupt:
            print("\nPlayback interrupted. Exiting...")
            break

    cap.release()
    audio_thread.join()

# Example usage
video_path = "E:/projs/Python_Apps/5_Terminal-Youtube/Rick Astley - Never Gonna Give You Up (Official Music Video).mp4"
audio_path = "E:/projs/Python_Apps/5_Terminal-Youtube/audio.mp3"

play_video_in_ascii(video_path, audio_path)
