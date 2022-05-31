import os
from os.path import splitext, exists
from shutil import move
import time

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

source_dir = "C:/Users/Kuba/Downloads"
zips_dir = "C:/Users/Kuba/Downloads/ZIPY"
images_dir = "C:/Users/Kuba/Downloads/IMAGES"
docs_dir = "C:/Users/Kuba/Downloads/PDF"


# ? supported image types
image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

# ? supported Document types
document_extensions = [".doc", ".docx", ".odt", ".xls", ".xlsx", ".txt"]

# ? supported zip/rar types
zip_extensions = ['.rar', ".zip"]



def make_unique(path):
    filename, extension = splitext(path)
    counter = 1
    # IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(path):
        path = f"{filename} ({counter}){extension}"
        counter += 1

    return path

def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(name)
        os.rename(entry, unique_name)
    move(entry, dest)


class ChooseDirectory(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_document_files(entry, name)
                self.check_image_files(entry, name)
                self.check_zip_files(entry, name)
                self.check_document_files(entry, name)

    def check_document_files(self, entry, name):  # * Checks all Document Files
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                move_file(docs_dir, entry, name)
                logging.info(f"Moved document/pdf file: {name}")

    def check_image_files(self, entry, name):
        for img_extension in image_extensions:
            if name.endswith(img_extension) or name.endswith(img_extension.upper()):
                move_file(images_dir, entry, name)
                logging.info(f"Moved zip/rar file: {name}")

    def check_zip_files(self, entry, name):
        for zip_extension in zip_extensions:
            if name.endswith(zip_extension) or name.endswith(zip_extension.upper()):
                move_file(zips_dir, entry, name)
                logging.info(f"Moved zip/rar file: {name}")



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = ChooseDirectory()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()