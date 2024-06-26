from matplotlib.axes import Axes
from pandas import Series


class AdditionToAxes:
    def __init__(self, target_ax: Axes) -> None:
        # ax = fig.add_axes((0.11, 0.09, 0.79, 0.83))
        self.ax = target_ax

    def plot_data(
        self,
        x_data: Series,
        y_data: Series,
        color: str,
        linewidth: float,
        ticks_size: float,
    ) -> None:
        self.ax.plot(x_data, y_data, linewidth=linewidth, color=color)
        self.ax.tick_params(labelsize=ticks_size)

    def set_label(
        self, x_name: str, y_name: str, labelsize: float, interval: float
    ) -> None:
        self.ax.set_xlabel(x_name, fontsize=labelsize, labelpad=interval)
        self.ax.set_ylabel(y_name, fontsize=labelsize, labelpad=interval)

    def set_range(
        self, x_start: float, x_end: float, y_start: float, y_end: float
    ) -> None:
        self.ax.set_xlim(left=x_start, right=x_end)
        self.ax.set_ylim(bottom=y_start, top=y_end)

    def draw_baseline_v(self, x: float, color: str, width: float) -> None:
        self.ax.axvline(x=x, color=color, linewidth=width)

    def draw_baseline_h(self, y: float, color: str, width: float) -> None:
        self.ax.axhline(y=y, color=color, linewidth=width)

    def set_title(self, title_name: str, size: float) -> None:
        self.ax.set_title(title_name, fontsize=size)

    def draw_gridlines(self, color: str, width: float):
        self.ax.grid(True, color=color, linewidth=width)
