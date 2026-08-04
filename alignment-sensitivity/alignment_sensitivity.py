#!/usr/bin/env python3
"""Calculate and plot gauge-volume alignment sensitivity."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from scipy.interpolate import griddata


HERE = Path(__file__).resolve().parent
RECTANGLE_HALF_WIDTH_MM = 0.15


def load_rows() -> list[dict[str, object]]:
    with (HERE / "fitted_values.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    # Fit uncertainties are retained in the CSV but are not used in this
    # deterministic alignment-sensitivity visualization.
    numeric_fields = (
        "measurement_position_mm",
        "relative_y_mm",
        "relative_z_mm",
        "shift_mm",
        "d_spacing_angstrom",
    )
    for row in rows:
        for field in numeric_fields:
            row[field] = float(row[field])
    return rows


def calculate_location(rows: list[dict[str, object]]) -> dict[str, object]:
    reference = next(row for row in rows if row["shift_direction"] == "reference")
    reference_spacing = float(reference["d_spacing_angstrom"])
    spacing = np.array([float(row["d_spacing_angstrom"]) for row in rows])
    strain = (spacing - reference_spacing) / reference_spacing * 1e6
    return {
        "x": float(reference["measurement_position_mm"]),
        "y": np.array([float(row["relative_y_mm"]) for row in rows]),
        "z": np.array([float(row["relative_z_mm"]) for row in rows]),
        "strain": strain,
    }


def create_figure(rows: list[dict[str, object]]) -> plt.Figure:
    locations = []
    for location_number in range(1, 5):
        label = f"Location {location_number}"
        location_rows = [row for row in rows if row["location"] == label]
        if len(location_rows) != 5:
            raise ValueError(f"{label} must contain five shift measurements.")
        locations.append(calculate_location(location_rows))

    grid = np.arange(-1.0, 1.05, 0.05)
    y_grid, z_grid = np.meshgrid(grid, grid)
    interpolated_locations = [
        griddata(
            np.column_stack((location["z"], location["y"])),
            location["strain"],
            (z_grid, y_grid),
            method="linear",
        )
        for location in locations
    ]
    color_minimum = min(np.nanmin(values) for values in interpolated_locations)
    color_maximum = max(np.nanmax(values) for values in interpolated_locations)
    figure, axes = plt.subplots(2, 2, figsize=(7.2, 6.69))

    for axis, location, interpolated in zip(
        axes.flat, locations, interpolated_locations
    ):
        contour = axis.contourf(
            z_grid,
            y_grid,
            interpolated,
            levels=100,
            cmap="viridis",
            vmin=color_minimum,
            vmax=color_maximum,
        )
        colorbar = figure.colorbar(contour, ax=axis)
        colorbar.set_label("Microstrain", fontsize=7)
        colorbar.ax.tick_params(labelsize=7)

        axis.scatter(
            location["z"],
            location["y"],
            c="red",
            s=20,
            edgecolors="black",
            linewidths=1,
        )
        for z_value, y_value, strain_value in zip(
            location["z"], location["y"], location["strain"]
        ):
            axis.text(
                z_value - 0.05,
                y_value + 0.07,
                f"{strain_value:.0f}",
                fontsize=7,
                color="red",
            )

        axis.add_patch(
            Rectangle(
                (-RECTANGLE_HALF_WIDTH_MM, -RECTANGLE_HALF_WIDTH_MM),
                2 * RECTANGLE_HALF_WIDTH_MM,
                2 * RECTANGLE_HALF_WIDTH_MM,
                edgecolor="red",
                facecolor="none",
                linewidth=1,
            )
        )
        rectangle_mask = (
            (z_grid >= -RECTANGLE_HALF_WIDTH_MM)
            & (z_grid <= RECTANGLE_HALF_WIDTH_MM)
            & (y_grid >= -RECTANGLE_HALF_WIDTH_MM)
            & (y_grid <= RECTANGLE_HALF_WIDTH_MM)
        )
        rectangle_values = interpolated[rectangle_mask]
        maximum_index = np.nanargmax(np.abs(rectangle_values))
        maximum_z = z_grid[rectangle_mask][maximum_index]
        maximum_y = y_grid[rectangle_mask][maximum_index]
        maximum_strain = rectangle_values[maximum_index]
        axis.scatter(
            maximum_z,
            maximum_y,
            c="lightblue",
            s=20,
            edgecolors="black",
            zorder=10,
        )
        axis.text(
            maximum_z + 0.07,
            maximum_y + 0.025,
            f"{abs(maximum_strain):.0f}",
            fontsize=7,
            color="lightblue",
        )

        axis.set_xlabel("Relative Z position (mm)", fontsize=7)
        axis.set_ylabel("Relative Y position (mm)", fontsize=7)
        axis.set_title(f"x = {location['x']:.0f} mm", fontsize=7)
        axis.tick_params(labelsize=7)
        axis.set_xlim(-1.2, 1.2)
        axis.set_ylim(-1.2, 1.2)
        axis.set_aspect("equal")

    figure.tight_layout()
    return figure


def main() -> None:
    create_figure(load_rows())
    plt.show()


if __name__ == "__main__":
    main()
