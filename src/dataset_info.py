from pathlib import Path

from arangement.replacement import DimensionArrayReplacement


def output_dataset_information(wrfout_path: str) -> None:
    target_wrfout = DimensionArrayReplacement(wrfout_path)
    dataset = target_wrfout.dataset
    parent_dir = Path(wrfout_path).parent
    filename = Path(wrfout_path).stem
    output_path = f"{parent_dir}/info_{filename}.txt"
    with open(output_path, mode="w") as f:
        f.write("################### Overview ###################\n")
        f.write(f"<< dimension infomation >>\n{dataset.dims} \n")
        f.write(f"\n<< coordinate infomation >>\n{dataset.coords} \n")
        f.write(f"\n<< variables infomation >>\n{dataset.data_vars} \n")
        f.write("\n\n################### Detail ###################\n")
        f.write(f"<< dimension infomation >>\n")
        for dim in dataset.dims:
            f.write(f"\n{dataset[dim]} \n")
        f.write(f"\n\n<< coordinate infomation >>\n")
        for coord in dataset.coords:
            f.write(f"\n{dataset[coord]} \n")
        f.write(f"\n\n<< variables infomation >>\n")
        for var in dataset.data_vars:
            f.write(f"\n{dataset[var]} \n")
