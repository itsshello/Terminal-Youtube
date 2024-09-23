import yt_dlp

class YouTubeVideo:
    def __init__(self, video_info):
        self.title = video_info.get('title', 'Unknown Title')
        self.likes = video_info.get('like_count', 'Unknown')
        self.views = video_info.get('view_count', 'Unknown')
        self.author = video_info.get('uploader', 'Unknown')
        self.released_on = video_info.get('upload_date', 'Unknown')
        self.pixel_ratio = f"{video_info['width']}x{video_info['height']}" if 'width' in video_info and 'height' in video_info else "Unknown"
        self.filepath = None

    def __str__(self):
        return f"Title: {self.title}\nLikes: {self.likes}\nViews: {self.views}\nAuthor: {self.author}\nReleased on: {self.released_on}\nPixel Ratio: {self.pixel_ratio}\n"

def download_video_with_audio(youtube_url, save_path='.'):
    ydl_opts = {
        'format': 'bestvideo+bestaudio[ext=m4a]/best',  # Download best video and audio
        'merge_output_format': 'mp4',  # Merge as mp4
        'outtmpl': save_path + '/%(title)s.%(ext)s',  # Output file path template
        'postprocessors': [{  # Automatically merge video and audio
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            video = YouTubeVideo(info)
            video.filepath = f"{save_path}/{info['title']}.mp4"
            return video
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

# Example usage
youtube_link = "https://www.youtube.com/watch?v=RLxumX64HMo"
video = download_video_with_audio(youtube_link)

if video and video.filepath:
    print(f"Video with audio downloaded and saved at: {video.filepath}")
    print(video)  # Display the video details (title, views, etc.)
else:
    print("Failed to download video.")
