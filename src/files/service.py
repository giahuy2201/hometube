import os
import shutil


def move_media(src_path: str, dst_path: str, media_id: str):
    """
    Move files whose name contain media_id from src to dst
    """
    os.makedirs(dst_path, exist_ok=True)
    files = os.listdir(src_path)
    matching_files = [file for file in files if media_id in file]
    for file in matching_files:
        source_path = os.path.join(src_path, file)
        target_path = os.path.join(dst_path, file)
        shutil.move(source_path, target_path)
    return len(matching_files) > 0
