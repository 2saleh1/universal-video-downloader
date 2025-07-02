# Universal Video Downloader

A sleek, easy-to-use desktop application for downloading videos from YouTube and hundreds of other platforms with automatic quality selection and progress tracking.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🎥 **Multi-platform support** - Download from YouTube, Vimeo, Facebook, Instagram, TikTok, and 1000+ sites
- 🎯 **Smart quality detection** - Automatically finds and displays available video qualities
- 📊 **Real-time progress** - Visual progress bar with percentage tracking
- 🌙 **Dark theme UI** - Modern, eye-friendly interface
- 🔄 **Auto-merging** - Seamlessly combines video and audio streams
- 📁 **Organized downloads** - Saves videos to a dedicated "Videos" folder
- ⚡ **Dependency management** - Automatically installs required components

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Internet connection

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/universal-video-downloader.git
   cd universal-video-downloader
   ```

2. **Run the application**
   ```bash
   python downloader.py
   ```

The app will automatically install `yt-dlp` if not present. For optimal performance, install FFmpeg:
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/)
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

## 🎮 Usage

1. **Enter URL** - Paste any video URL from supported platforms
2. **Get Qualities** - Click to fetch available download options
3. **Select Quality** - Choose your preferred resolution
4. **Download** - Hit the download button and track progress

### Supported Platforms
YouTube, Vimeo, Facebook, Instagram, Twitter/X, TikTok, Twitch, Reddit, Dailymotion, and many more!

## 📱 Screenshots

![App Screenshot](screenshot.png)

*Add your own screenshot of the application interface*

## 🛠️ Technical Details

- **Built with**: Python, Tkinter, yt-dlp
- **Dependencies**: Automatically managed
- **Output format**: MP4 (optimized for compatibility)
- **Threading**: Non-blocking UI with background downloads

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for personal use only. Please respect copyright laws and platform terms of service. Only download content you have permission to download.

## 🙏 Acknowledgments

- Built on top of the excellent [yt-dlp](https://github.com/yt-dlp/yt-dlp) project
- Inspired by the need for a simple, cross-platform video downloader
