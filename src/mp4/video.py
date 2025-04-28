from glob import glob

import cv2


def imgs_to_mp4(
    imgs_dir_path: str,
    saved_mp4_path: str,
    extension: str = "jpg",
    fps: float = 5.0,
) -> None:

    img_paths = sorted(glob(f"{imgs_dir_path}/*.{extension}"))
    if not img_paths:
        raise ValueError("No images found in the specified directory.")

    first_frame = cv2.imread(img_paths[0])
    height, width, _ = first_frame.shape
    SIZE = (width, height)

    writer = cv2.VideoWriter(
        filename=saved_mp4_path,
        apiPreference=cv2.CAP_FFMPEG,
        fourcc=cv2.VideoWriter_fourcc(*"avc1"),
        fps=fps,
        frameSize=SIZE,
    )

    for img_path in img_paths:
        img = cv2.imread(img_path)
        writer.write(img)
    writer.release()
