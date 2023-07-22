import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Replace this with your actual download directory path
DOWNLOADS_DIR = "C:/Users/gargb/OneDrive/Desktop/sample" #change this to your directory

# Dictionary to map file extensions to folder names
file_extensions = {
    '.pdf': 'Documents',
    '.doc': 'Documents',
    '.txt': 'Documents',
    '.jpg': 'Images',
    '.png': 'Images',
    '.mp4': 'Videos',
    # Add more file extensions and corresponding folder names as needed
}

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        _, file_extension = os.path.splitext(file_path)

        if file_extension.lower() in file_extensions:
            target_folder = file_extensions[file_extension.lower()]
            target_dir = os.path.join(DOWNLOADS_DIR, target_folder)

            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            # Add a delay of 2 seconds after the file creation event
            time.sleep(2)

            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                new_file_path = os.path.join(target_dir, os.path.basename(file_path))
                shutil.move(file_path, new_file_path)
                print(f"Moved {file_path} to {new_file_path}")
            else:
                print(f"Failed to move {file_path} (file not found or empty)")

def main():
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, DOWNLOADS_DIR, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
