"""Small, reusable output and axis-formatting helpers."""

from pathlib import Path

import matplotlib.ticker as mticker


def save_figure(fig, output_path, dpi=300):
    """Save a Matplotlib figure and create its parent directory if required."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight", facecolor="white")
    print(f"Saved figure: {output_path}")


def save_table(dataframe, output_path, index=False):
    """Save a dataframe and create its parent directory if required."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_path, index=index)
    print(f"Saved table: {output_path}")


def format_currency_axis(axis):
    """Format an axis using whole-dollar labels."""
    axis.set_major_formatter(
        mticker.FuncFormatter(lambda value, position: f"${value:,.0f}")
    )


def format_percent_axis(axis):
    """Format an axis using percentage labels."""
    axis.set_major_formatter(
        mticker.FuncFormatter(lambda value, position: f"{value:.0f}%")
    )
