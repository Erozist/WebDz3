import os
import sys
import scan
import shutil
import logging
import normalize
from pathlib import Path
from threading import Thread

def handle_file(path, root_folder, dist):
    logging.debug(f'Processing file: {path}')
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder / normalize.normalize(path.name))


def handle_archive(path, root_folder, dist):
    logging.debug(f'Processing file: {path}')
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    del_folder = root_folder / path
    new_name = normalize.normalize(path.name.replace(".zip", '').replace(".tar", '').replace(".gz", ''))

    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))
    except OSError:
        shutil.rmtree(archive_folder)
        os.remove(del_folder)
        logging.error(f'Error occurred while extracting archive: {path}')
        return

    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def process_files(files, root_folder, dist):
    for file_list in files:
        for file in file_list:
            handle_file(file, root_folder, dist)


def process_archives(archives, root_folder, dist):
    for archive_list in archives:
        for archive in archive_list:
            handle_archive(archive, root_folder, dist)


def main(folder_path):
    print(folder_path)
    scan.scan(folder_path)

    # Обробка відеофайлів
    video_thread = Thread(target=process_files, args=(scan.video, folder_path, "video"))
    video_thread.start()

    # Обробка музики
    audio_thread = Thread(target=process_files, args=(scan.audio, folder_path, "audio"))
    audio_thread.start()

    # Обробка зображень
    images_thread = Thread(target=process_files, args=(scan.images, folder_path, "images"))
    images_thread.start()

    # Обробка документів
    documents_thread = Thread(target=process_files, args=(scan.documents, folder_path, "documents"))
    documents_thread.start()

    # Обробка архівів
    archive_thread = Thread(target=process_archives, args=(scan.archives, folder_path, "archives"))
    archive_thread.start()

    # Обробка інших файлів
    others_thread = Thread(target=process_files, args=(scan.others, folder_path, "others"))
    others_thread.start()

    # Очікуємо завершення всіх потоків
    video_thread.join()
    audio_thread.join()
    images_thread.join()
    documents_thread.join()
    archive_thread.join()
    others_thread.join()

    remove_empty_folders(folder_path)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    path = 'temp'  # sys.argv[1]
    print(f'Start in {path}')

    folder = Path(path)
    main(folder.resolve())

    with open(f"{path}/Resume.txt", 'w+', encoding='utf-8') as file:
        file.write("Video: {}\n".format(" *|* ".join(([file.name for files in scan.video for file in files]))))
        file.write("Audio: {}\n".format(" *|* ".join(([file.name for files in scan.audio for file in files]))))
        file.write("Images: {}\n".format(" *|* ".join(([file.name for files in scan.images for file in files]))))
        file.write("Documents: {}\n".format(" *|* ".join(([file.name for files in scan.documents for file in files]))))
        file.write("Archives: {}\n".format(" *|* ".join(([file.name for files in scan.archives for file in files]))))
        file.write("Others: {}\n".format(" *|* ".join(([file.name for file in scan.others]))))
        file.write("Known extensions: {}\n".format(scan.extensions))
        file.write("Unknown extensions: {}\n".format(scan.unknown))
