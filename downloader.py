import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import sys
import os
import json
import threading
from pathlib import Path
import re

class UniversalVideoDownloader:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Universal Video Downloader")
        self.root.geometry("800x600")
        self.root.configure(bg='#1e1e1e')
        
        # Create Videos folder if it doesn't exist
        self.videos_folder = Path("Videos")
        self.videos_folder.mkdir(exist_ok=True)
        
        # Variables
        self.url_var = tk.StringVar()
        self.quality_var = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Ready")
        
        self.formats_data = {}
        self.download_thread = None
        
        # Check dependencies on startup
        self.check_dependencies()
        self.setup_ui()
        
    def check_dependencies(self):
        """Check and install required dependencies"""
        try:
            # Check yt-dlp
            subprocess.run(['yt-dlp', '--version'], 
                        capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.install_ytdlp()
            
        try:
            # Check ffmpeg
            subprocess.run(['ffmpeg', '-version'], 
                        capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Instead of just showing a warning, try to install ffmpeg
            self.install_ffmpeg()
    
    def install_ytdlp(self):
        """Install yt-dlp automatically"""
        try:
            self.status_var.set("Installing yt-dlp...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'yt-dlp'])
            messagebox.showinfo("Success", "yt-dlp installed successfully!")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to install yt-dlp. Please install manually:\npip install yt-dlp")
            
            
    def install_ffmpeg(self):
        """Install ffmpeg automatically based on the platform"""
        platform = sys.platform
        self.status_var.set("Installing FFmpeg...")
        
        try:
            if platform == "win32":  # Windows
                # For Windows, we'll use the pip package ffmpeg-python which includes binaries
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'ffmpeg-python'])
                messagebox.showinfo("Success", "FFmpeg installed successfully!")
                
            elif platform == "darwin":  # macOS
                # Check if homebrew is installed
                try:
                    subprocess.run(['brew', '--version'], capture_output=True, check=True)
                    # Install ffmpeg with homebrew
                    subprocess.check_call(['brew', 'install', 'ffmpeg'])
                    messagebox.showinfo("Success", "FFmpeg installed successfully via Homebrew!")
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # Homebrew not found
                    messagebox.showwarning("Homebrew Not Found", 
                                        "Homebrew is needed to install FFmpeg on macOS.\n"
                                        "Please install Homebrew first: https://brew.sh/")
                    
            elif platform.startswith("linux"):  # Linux
                # Try apt (Debian/Ubuntu)
                try:
                    subprocess.check_call(['sudo', 'apt', 'update'])
                    subprocess.check_call(['sudo', 'apt', 'install', '-y', 'ffmpeg'])
                    messagebox.showinfo("Success", "FFmpeg installed successfully via apt!")
                except subprocess.CalledProcessError:
                    # Try yum (Fedora/CentOS/RHEL)
                    try:
                        subprocess.check_call(['sudo', 'yum', 'install', '-y', 'ffmpeg'])
                        messagebox.showinfo("Success", "FFmpeg installed successfully via yum!")
                    except subprocess.CalledProcessError:
                        # Try pacman (Arch Linux)
                        try:
                            subprocess.check_call(['sudo', 'pacman', '-S', '--noconfirm', 'ffmpeg'])
                            messagebox.showinfo("Success", "FFmpeg installed successfully via pacman!")
                        except subprocess.CalledProcessError:
                            # If all package managers fail
                            messagebox.showwarning("Installation Failed", 
                                                "Failed to install FFmpeg automatically.\n"
                                                "Please install FFmpeg manually for your Linux distribution.")
            else:
                # Unsupported platform
                messagebox.showwarning("Unsupported Platform", 
                                    "Automatic FFmpeg installation not supported on this platform.\n"
                                    "Please install FFmpeg manually: https://ffmpeg.org/")
                
        except Exception as e:
            messagebox.showwarning("FFmpeg Installation", 
                                f"Could not install FFmpeg automatically: {str(e)}.\n"
                                "Please install FFmpeg manually: https://ffmpeg.org/")
        
            
    def setup_ui(self):
        """Setup the user interface"""
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure dark theme colors
        style.configure('Dark.TFrame', background='#1e1e1e')
        style.configure('Dark.TLabel', background='#1e1e1e', foreground='#ffffff')
        style.configure('Dark.TButton', background='#404040', foreground='#ffffff')
        style.configure('Dark.TEntry', fieldbackground='#404040', foreground='#ffffff')
        style.configure('Dark.TCombobox', fieldbackground='#404040', foreground='#ffffff')
        style.configure('Dark.Horizontal.TProgressbar', background='#667eea')
        
        # Main container
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="🎥 Universal Video Downloader", 
                              font=('Arial', 24, 'bold'), 
                              bg='#1e1e1e', fg='#667eea')
        title_label.pack(pady=(0, 30))
        
        # URL Input Section
        url_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        url_frame.pack(fill='x', pady=(0, 20))
        
        url_label = ttk.Label(url_frame, text="📎 Video URL:", 
                             font=('Arial', 12), style='Dark.TLabel')
        url_label.pack(anchor='w', pady=(0, 5))
        
        url_entry_frame = ttk.Frame(url_frame, style='Dark.TFrame')
        url_entry_frame.pack(fill='x')
        
        self.url_entry = tk.Entry(url_entry_frame, textvariable=self.url_var,
                                 font=('Arial', 11), bg='#404040', fg='#ffffff',
                                 insertbackground='#ffffff', relief='flat', bd=5)
        self.url_entry.pack(side='left', fill='x', expand=True, ipady=8)
        
        fetch_btn = tk.Button(url_entry_frame, text="Get Qualities", 
                             command=self.fetch_qualities,
                             bg='#667eea', fg='white', font=('Arial', 10, 'bold'),
                             relief='flat', bd=0, padx=20)
        fetch_btn.pack(side='right', padx=(10, 0))
        
        # Quality Selection Section
        quality_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        quality_frame.pack(fill='x', pady=(0, 20))
        
        quality_label = ttk.Label(quality_frame, text="📊 Select Quality:", 
                                 font=('Arial', 12), style='Dark.TLabel')
        quality_label.pack(anchor='w', pady=(0, 5))
        
        self.quality_combo = ttk.Combobox(quality_frame, textvariable=self.quality_var,
                                         font=('Arial', 11), state='readonly')
        self.quality_combo.pack(fill='x', ipady=5)
        
        # Download Section
        download_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        download_frame.pack(fill='x', pady=(0, 20))
        
        self.download_btn = tk.Button(download_frame, text="⬇️ Download Video", 
                                     command=self.download_video,
                                     bg='#28a745', fg='white', font=('Arial', 14, 'bold'),
                                     relief='flat', bd=0, pady=10, state='disabled')
        self.download_btn.pack(fill='x')
        
        # Progress Section
        progress_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        progress_frame.pack(fill='x', pady=(0, 20))
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                           style='Dark.Horizontal.TProgressbar')
        self.progress_bar.pack(fill='x', pady=(0, 10))
        
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var,
                                     font=('Arial', 10), style='Dark.TLabel')
        self.status_label.pack(anchor='w')
        
        # Footer
        footer_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        footer_frame.pack(fill='x', side='bottom')
        
        footer_label = tk.Label(footer_frame, 
                               text="💾 Downloads will be saved to 'Videos' folder",
                               font=('Arial', 9), bg='#1e1e1e', fg='#888888')
        footer_label.pack(pady=(20, 0))
        
        # Bind Enter key to fetch qualities
        self.url_entry.bind('<Return>', lambda e: self.fetch_qualities())
        
    def fetch_qualities(self):
        """Fetch available video qualities"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a video URL!")
            return
            
        # Validate URL
        if not re.match(r'^https?://', url):
            messagebox.showwarning("Warning", "Please enter a valid URL (starting with http:// or https://)")
            return
            
        def fetch_thread():
            try:
                self.status_var.set("Fetching available qualities...")
                self.progress_var.set(0)
                self.root.update()
                
                # Get video formats
                cmd = ['yt-dlp', '-J', url]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                
                data = json.loads(result.stdout)
                title = data.get('title', 'Unknown')
                formats = data.get('formats', [])
                
                # Process formats to get unique qualities with best audio
                quality_map = {}
                
                for fmt in formats:
                    if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none':
                        # Video with audio (best option)
                        height = fmt.get('height')
                        if height:
                            quality_key = f"{height}p"
                            current_tbr = fmt.get('tbr', 0) or 0
                            existing_tbr = quality_map.get(quality_key, {}).get('tbr', 0) or 0
                            if quality_key not in quality_map or current_tbr > existing_tbr:
                                quality_map[quality_key] = fmt
                    elif fmt.get('vcodec') != 'none' and fmt.get('acodec') == 'none':
                        # Video only - pair with best audio
                        height = fmt.get('height')
                        if height:
                            quality_key = f"{height}p"
                            
                            # Find best audio format
                            best_audio = None
                            for audio_fmt in formats:
                                if audio_fmt.get('acodec') != 'none' and audio_fmt.get('vcodec') == 'none':
                                    current_abr = audio_fmt.get('abr', 0) or 0
                                    best_abr = best_audio.get('abr', 0) or 0 if best_audio else 0
                                    if not best_audio or current_abr > best_abr:
                                        best_audio = audio_fmt
                            
                            if best_audio:
                                current_video_tbr = fmt.get('tbr', 0) or 0
                                existing_video_tbr = quality_map.get(quality_key, {}).get('video_tbr', 0) or 0
                                if (quality_key not in quality_map or 
                                    current_video_tbr > existing_video_tbr):
                                    quality_map[quality_key] = {
                                        'video_format_id': fmt['format_id'],
                                        'audio_format_id': best_audio['format_id'],
                                        'height': height,
                                        'video_tbr': current_video_tbr,
                                        'combined': True
                                    }
                
                # Sort qualities by resolution
                sorted_qualities = sorted(quality_map.items(), 
                                        key=lambda x: x[1].get('height', 0) or 0, reverse=True)
                
                self.formats_data = {k: v for k, v in sorted_qualities}
                
                # Update UI
                self.root.after(0, self.update_quality_combo, list(self.formats_data.keys()), title)
                
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr or "Failed to fetch video information"
                self.root.after(0, lambda: messagebox.showerror("Error", f"Error: {error_msg}"))
                self.root.after(0, lambda: self.status_var.set("Error fetching qualities"))
            except json.JSONDecodeError:
                self.root.after(0, lambda: messagebox.showerror("Error", "Failed to parse video information"))
                self.root.after(0, lambda: self.status_var.set("Error parsing data"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Unexpected error: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("Error occurred"))
        
        # Run in separate thread to prevent UI freezing
        threading.Thread(target=fetch_thread, daemon=True).start()
        
    def update_quality_combo(self, qualities, title):
        """Update the quality combobox with fetched qualities"""
        if qualities:
            self.quality_combo['values'] = qualities
            self.quality_combo.set(qualities[0])  # Select best quality by default
            self.download_btn.config(state='normal')
            self.status_var.set(f"✅ Found {len(qualities)} qualities for: {title[:50]}...")
        else:
            messagebox.showwarning("Warning", "No compatible video qualities found!")
            self.status_var.set("No qualities found")
            
    def download_video(self):
        """Download the selected video"""
        if not self.quality_var.get() or not self.url_var.get():
            messagebox.showwarning("Warning", "Please select a quality and enter URL!")
            return
            
        if self.download_thread and self.download_thread.is_alive():
            messagebox.showinfo("Info", "Download already in progress!")
            return
            
        def download_thread():
            try:
                self.root.after(0, lambda: self.download_btn.config(state='disabled'))
                self.root.after(0, lambda: self.status_var.set("Starting download..."))
                self.root.after(0, lambda: self.progress_var.set(0))
                
                url = self.url_var.get().strip()
                quality = self.quality_var.get()
                format_info = self.formats_data[quality]
                
                # Prepare download command
                output_path = self.videos_folder / "%(title)s.%(ext)s"
                
                if format_info.get('combined'):
                    # Separate video and audio formats
                    format_selector = f"{format_info['video_format_id']}+{format_info['audio_format_id']}"
                else:
                    # Single format with video and audio
                    format_selector = format_info['format_id']
                
                cmd = [
                    'yt-dlp',
                    '-f', format_selector,
                    '--merge-output-format', 'mp4',
                    '-o', str(output_path),
                    url
                ]
                
                # Run download with progress tracking
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                         text=True, universal_newlines=True)
                
                for line in process.stdout:
                    line = line.strip()
                    if '[download]' in line and '%' in line:
                        # Extract progress percentage
                        try:
                            percent_match = re.search(r'(\d+\.?\d*)%', line)
                            if percent_match:
                                percent = float(percent_match.group(1))
                                self.root.after(0, lambda p=percent: self.progress_var.set(p))
                                self.root.after(0, lambda: self.status_var.set(f"Downloading... {percent:.1f}%"))
                        except:
                            pass
                    elif 'Merging formats' in line:
                        self.root.after(0, lambda: self.status_var.set("Merging video and audio..."))
                
                process.wait()
                
                if process.returncode == 0:
                    self.root.after(0, lambda: self.progress_var.set(100))
                    self.root.after(0, lambda: self.status_var.set("✅ Download completed successfully!"))
                    self.root.after(0, lambda: messagebox.showinfo("Success", 
                        f"Video downloaded successfully!\nSaved to: {self.videos_folder.absolute()}"))
                else:
                    self.root.after(0, lambda: self.status_var.set("❌ Download failed"))
                    self.root.after(0, lambda: messagebox.showerror("Error", "Download failed. Please try again."))
                    
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Download error: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("❌ Download error"))
            finally:
                self.root.after(0, lambda: self.download_btn.config(state='normal'))
        
        self.download_thread = threading.Thread(target=download_thread, daemon=True)
        self.download_thread.start()
        
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = UniversalVideoDownloader()
    app.run()