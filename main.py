import yt_dlp

def download_video(youtube_url, save_path='.'):
    # Options to download the best video and audio available
    ydl_opts = {
        'format': 'bestvideo',  # Get the best video and audio available
        'outtmpl': save_path + '/%(title)s.%(ext)s',  # Set the output file name format
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading video from: {youtube_url}")
            ydl.download([youtube_url])
            print("Download completed!")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
youtube_link = input("Enter the YouTube video URL: ")
download_video(youtube_link)

# from pytube import YouTube
# YouTube('https://www.youtube.com/watch?v=RLxumX64HMo').streams.first().download()
# yt = YouTube('http://youtube.com/watch?v=2lAe1cqCOXo')
# yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()