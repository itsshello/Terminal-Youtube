import yt_dlp

class YouTubeVideo:
    def __init__(self, url):
        self.url = url
        self.title = ""
        self.description = ""
        self.like_count = 0
        self.view_count = 0
        self.author = ""
        self.release_time = ""
        self.pixel_ratio = ""
        self.video_path = ""
        self.audio_path = ""
    
    def fetch_metadata(self):
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'noplaylist': True,
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.url, download=False)
            self.title = info.get('title', '')
            self.description = info.get('description', '')
            self.like_count = info.get('like_count', 0)
            self.view_count = info.get('view_count', 0)
            self.author = info.get('uploader', '')
            self.release_time = info.get('upload_date', '')
            self.pixel_ratio = f"{info.get('width', 0)}x{info.get('height', 0)}"
    
    def HighQualityDualDownload(self, save_path='.'):
        ydl_opts_video = {
            'format': 'bestvideo',  # Only video
            'outtmpl': save_path + '/%(title)s.%(ext)s',
        }
        
        ydl_opts_audio = {
            'format': 'bestaudio',  # Only audio
            'outtmpl': save_path + '/%(title)s_audio.%(ext)s',
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
                print(f"Downloading video: {self.title}")
                info_video = ydl.extract_info(self.url, download=True)
                self.video_path = f"{save_path}/{info_video['title']}.{info_video['ext']}"
            
            with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
                print(f"Downloading audio: {self.title}")
                info_audio = ydl.extract_info(self.url, download=True)
                self.audio_path = f"{save_path}/{info_audio['title']}_audio.{info_audio['ext']}"
            
            print("Download completed!")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def download(self, save_path='.'):
        ydl_opts = {
            'format': 'bestvideo',  # Get the best video only
            'outtmpl': save_path + '/%(title)s.%(ext)s',
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Downloading video from: {youtube_url}")

                info_video = ydl.extract_info(self.url, download=True)
                self.video_path = f"{save_path}/{info_video['title']}.{info_video['ext']}"

                print("Download completed!")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def videoPath(self):
        return self.video_path;
    

# Example usage
youtube_link = input("Enter the YouTube video URL: ")
video = YouTubeVideo(youtube_link)

# Fetch metadata
video.fetch_metadata()

# Display video information
print(f"Title: {video.title}")
print(f"Description: {video.description}")
print(f"Likes: {video.like_count}")
print(f"Views: {video.view_count}")
print(f"Author: {video.author}")
print(f"Released on: {video.release_time}")
print(f"Pixel Ratio: {video.pixel_ratio}")

# Optionally download the video and audio
download_option = input("Do you want to download this video and audio? (yes/no): ")
if download_option.lower() == 'yes':
    video.download()
