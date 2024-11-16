import os
import subprocess

script_dir = os.path.dirname(os.path.realpath(__file__))
ffmpeg_path = os.path.join(script_dir, 'bin', 'ffmpeg.exe')

input_file = 'E:\\projs\\Python_Apps\\5_Terminal-Youtube\\v\\1 Minute Timer_audio.m4a'
output_file = '.\\v\\audio.mp3'
ffmpeg_command = [ffmpeg_path, '-i', input_file, output_file]

try:
    process = subprocess.Popen(
        ffmpeg_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate(input="y\n")

    if stdout:
        print(stdout)
    if stderr:
        print(stderr)

    if process.returncode == 0:
        print(f"Conversion successful, deleted {input_file}")
    else:
        print(f"Conversion failed with return code: {process.returncode}")

except subprocess.CalledProcessError as e:
    print(f"Error occurred during conversion: {e}")
