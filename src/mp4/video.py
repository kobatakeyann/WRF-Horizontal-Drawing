from glob import glob

import cv2

from constant import MP4_FPS


def make_mp4_from_imgs(img_dir_path: str, saved_mp4_path: str) -> None:
    img_array = []
    for img_filename in sorted(glob(f"{img_dir_path}/*.jpg")):
        img = cv2.imread(img_filename)
        height, width, _ = img.shape
        size = (width, height)
        img_array.append(img)
    out = cv2.VideoWriter(
        filename=saved_mp4_path,
        apiPreference=cv2.CAP_FFMPEG,
        fourcc=cv2.VideoWriter_fourcc(*"avc1"),
        fps=MP4_FPS,
        frameSize=size,
    )
    for img in img_array:
        out.write(img)
    out.release()
