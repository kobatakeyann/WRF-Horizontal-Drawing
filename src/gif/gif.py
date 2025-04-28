from glob import glob

from PIL import Image


def imgs_to_gif(
    imgs_dir_path: str,
    saved_gif_path: str,
    extension: str = "jpg",
    gif_interval_time: int = 150,
) -> None:

    SIZE = (1200, 800)
    img_paths = sorted(glob(f"{imgs_dir_path}/*.{extension}"))

    if not img_paths:
        raise ValueError("No images found in the specified directory.")

    images: list[Image.Image] = []
    for img_filename in img_paths:
        with Image.open(img_filename) as img:
            img.thumbnail(SIZE)
            images.append(img.copy())

    images[0].save(
        saved_gif_path,
        save_all=True,
        append_images=images[1:],
        optimize=True,
        duration=gif_interval_time,
        loop=0,
    )
