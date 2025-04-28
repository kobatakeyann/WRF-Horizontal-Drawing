from pathlib import Path

from wrfout.information.collector import WrfoutInformationCollector
from wrfout.loader.xarray_dataset import WrfoutXarrayDataset


class WrfoutInformationOutputter:
    def __init__(self, wrfout_path: str) -> None:
        self._wrfout_path = wrfout_path
        self._wrfout = WrfoutXarrayDataset(wrfout_path)

    def _build_output_path(self) -> str:
        parent_dir = str(Path(self._wrfout_path).parents[1])
        wrfout_name = Path(self._wrfout_path).stem
        return f"{parent_dir}/information/{wrfout_name}_info.txt"

    def output_to_file(self) -> None:
        output_path = self._build_output_path()
        collector = WrfoutInformationCollector(self._wrfout)
        content = collector.collect_summary() + collector.collect_details()
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, mode="w") as f:
            f.write(content)
