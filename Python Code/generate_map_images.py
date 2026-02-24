"""
Generate static map images for Dundee Traffic Monitor.

This script generates PNG map images using OpenStreetMap tiles via contextily.
Images are saved to Data/MapImages/ directory.

Generated images:
- dundee_overview.png: Overview of entire Dundee city center
- 8 camera-specific maps (zoomed in on each camera location)
"""

import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Non-interactive backend
import contextily as ctx
import matplotlib.pyplot as plt
import numpy as np


def lat_lon_to_mercator(lat, lon):
    """Convert lat/lon to Web Mercator (EPSG:3857) coordinates."""
    x = lon * 20037508.34 / 180
    y = np.log(np.tan((90 + lat) * np.pi / 360)) / (np.pi / 180)
    y = y * 20037508.34 / 180
    return x, y


# Camera locations (lat, lon) – updated with actual coordinates from Google Maps
CAMERA_LOCATIONS = {
    "308_murraygate": (56.462759929526975, -2.9688074424282256),
    "310_seagate": (56.46343861706323, -2.9663773611621784),
    "317_reform_st": (56.46068274831757, -2.9704451667318845),
    "320_westport": (56.459786207166744, -2.9774909068460174),
    "323_union_street": (56.45872266066467, -2.970528642428207),
    "328_south_marketgate": (56.45839028141656, -2.970105232545838),
    "332_waterfront": (56.45832117376106, -2.964379542428206),
    "500_hilltown": (56.465815269827665, -2.9719523645172363),
}

# Dundee city center bounds
DUNDEE_BOUNDS = {
    "west": -2.9850,
    "east": -2.9550,
    "south": 56.4550,
    "north": 56.4720,
}

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent / "Data" / "MapImages"


def generate_overview_map(output_path: Path, figsize: tuple = (12, 8), dpi: int = 150):
    """
    Generate overview map of Dundee city center.

    Args:
        output_path: Path to save the PNG file
        figsize: Figure size in inches (width, height)
        dpi: Dots per inch for resolution
    """
    print(f"Generating overview map: {output_path.name}")

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    # Convert bounds to Web Mercator
    west, east = DUNDEE_BOUNDS["west"], DUNDEE_BOUNDS["east"]
    south, north = DUNDEE_BOUNDS["south"], DUNDEE_BOUNDS["north"]

    x_min, y_min = lat_lon_to_mercator(south, west)
    x_max, y_max = lat_lon_to_mercator(north, east)

    # Set bounds in Web Mercator
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    # Add OpenStreetMap basemap (top-down view)
    try:
        ctx.add_basemap(
            ax,
            source=ctx.providers.OpenStreetMap.Mapnik,
            crs="EPSG:3857",
            alpha=1.0,
            attribution=False,
        )
    except Exception as e:
        print(f"  Warning: Could not fetch tiles: {e}")
        ax.set_facecolor("#e5e5e5")

    # Add camera markers (convert to Mercator)
    for camera_name, (lat, lon) in CAMERA_LOCATIONS.items():
        x, y = lat_lon_to_mercator(lat, lon)
        ax.scatter(
            [x],
            [y],
            s=150,
            c="red",
            edgecolors="white",
            linewidths=2,
            zorder=3,
        )
        ax.annotate(
            camera_name.replace("_", " ").title(),
            (x, y),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=9,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
            zorder=4,
        )

    # Title
    ax.set_title(
        "Dundee City Center - CCTV Camera Locations",
        fontsize=14,
        fontweight="bold",
        pad=10,
    )

    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis("off")

    # Save
    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(f"  ✓ Saved: {output_path}")


def generate_camera_map(
    camera_name: str,
    lat: float,
    lon: float,
    output_path: Path,
    zoom_meters: int = 500,  # Half-width in meters (total view is 2x this)
    figsize: tuple = (6, 6),
    dpi: int = 150,
):
    """
    Generate zoomed-in map for a specific camera location.

    Args:
        camera_name: Name of the camera (for title and filename)
        lat: Latitude of camera
        lon: Longitude of camera
        output_path: Path to save the PNG file
        zoom_meters: Half-width of view in meters (smaller = more zoomed in)
        figsize: Figure size in inches (width, height)
        dpi: Dots per inch for resolution
    """
    print(f"Generating camera map: {camera_name}")

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    # Convert center to Web Mercator
    x_center, y_center = lat_lon_to_mercator(lat, lon)

    # Set bounds in Web Mercator (centered on camera)
    ax.set_xlim(x_center - zoom_meters, x_center + zoom_meters)
    ax.set_ylim(y_center - zoom_meters, y_center + zoom_meters)

    # Add OpenStreetMap basemap (top-down view)
    try:
        ctx.add_basemap(
            ax,
            source=ctx.providers.OpenStreetMap.Mapnik,
            crs="EPSG:3857",
            alpha=1.0,
            attribution=False,
        )
    except Exception as e:
        print(f"  Warning: Could not fetch tiles: {e}")
        ax.set_facecolor("#e5e5e5")

    # Mark camera location
    ax.scatter(
        [x_center],
        [y_center],
        s=300,
        c="red",
        edgecolors="white",
        linewidths=3,
        zorder=3,
        marker="o",
    )

    # Add crosshair
    ax.axhline(
        y=y_center, color="red", linestyle="--", linewidth=1, alpha=0.5, zorder=2
    )
    ax.axvline(
        x=x_center, color="red", linestyle="--", linewidth=1, alpha=0.5, zorder=2
    )

    # Title
    display_name = camera_name.replace("_", " ").title()
    ax.set_title(f"Camera: {display_name}", fontsize=12, fontweight="bold", pad=10)

    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis("off")

    # Save
    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(f"  ✓ Saved: {output_path}")


def main():
    """Generate all map images."""
    print("=" * 60)
    print("Generating Static Map Images for Dundee Traffic Monitor")
    print("=" * 60)

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\nOutput directory: {OUTPUT_DIR}\n")

    # Generate overview map
    generate_overview_map(OUTPUT_DIR / "dundee_overview.png")
    print()

    # Generate camera-specific maps
    for camera_name, (lat, lon) in CAMERA_LOCATIONS.items():
        output_path = OUTPUT_DIR / f"{camera_name}.png"
        generate_camera_map(camera_name, lat, lon, output_path)
        print()

    print("=" * 60)
    print("✓ All map images generated successfully!")
    print(f"  Total images: {len(CAMERA_LOCATIONS) + 1}")
    print(f"  Location: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
