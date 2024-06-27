from glob import glob

from PIL import Image


def make_gif_from_imgs(img_dir_path: str, saved_gif_path: str) -> None:
    img_array = []
    for img_filename in sorted(glob(f"{img_dir_path}/*.jpg")):
        img = Image.open(img_filename)
        img.thumbnail((1200, 800))
        img_array.append(img)
    img_array[0].save(
        saved_gif_path,
        save_all=True,
        append_images=img_array[1:],
        optimize=True,
        duration=90,
        loop=0,
    )


make_gif_from_imgs(
    "/work1/kobatake_yusuke/WRF/analysis/drawing/img/wrfout_nestingtest_d03_2023-08-21_00:00:00/horizontal/_RAINNC__HGT__U10_",
    "/work1/kobatake_yusuke/WRF/analysis/drawing/img/wrfout_nestingtest_d03_2023-08-21_00:00:00/horizontal/_RAINNC__HGT__U10_/rainfall.gif",
)
