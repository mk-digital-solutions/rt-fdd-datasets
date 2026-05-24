"""
Minimal example: plot one normal cycle from each dataset.

Demonstrates how to:
  1. Load a dataset
  2. Convert epoch-ms timestamps to seconds relative to cycle start
  3. Filter a representative cycle and plot the main analog signal

Run:
    python plot_cycle.py
"""
import matplotlib.pyplot as plt

from load_datasets import (
    load_picknplace_od,
    load_picknplace_asd,
    load_furnace_od,
    load_furnace_asd,
)


def relative_seconds(ts_ms):
    """Convert epoch-ms timestamps to seconds relative to the first sample."""
    return (ts_ms - ts_ms.iloc[0]) / 1000.0


def plot_pnp_normal_cycle(ax, df, label):
    """Plot the X-axis position trace of a representative normal cycle."""
    normal = df[(df["fault_class"] == 0) & (df["axis"] == 0)]
    cycle_id = sorted(normal["cycle"].unique())[5]
    cycle = normal[normal["cycle"] == cycle_id].sort_values("timestamp")
    ax.plot(relative_seconds(cycle["timestamp"]), cycle["x_pos_AI"], label=label)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("x_pos_AI")
    ax.set_title("Pick-and-Place: normal cycle (X-axis trajectory)")


def plot_furnace_normal_cycle(ax, df, label):
    """Plot the temperature trace of a representative normal cycle."""
    normal = df[df["class"].str.lower() == "normal"]
    cycle_id = sorted(normal["cycle_count"].unique())[5]
    cycle = normal[normal["cycle_count"] == cycle_id].sort_values("timestamp")
    ax.plot(relative_seconds(cycle["timestamp"]), cycle["temperature"], label=label)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Furnace: normal cycle (temperature profile)")


def main():
    pnp_od = load_picknplace_od()
    pnp_asd = load_picknplace_asd()
    furn_od = load_furnace_od()
    furn_asd = load_furnace_asd()

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    plot_pnp_normal_cycle(axes[0], pnp_od, "OD (real)")
    plot_pnp_normal_cycle(axes[0], pnp_asd, "ASD (simulated)")
    axes[0].legend()

    plot_furnace_normal_cycle(axes[1], furn_od, "OD (real)")
    plot_furnace_normal_cycle(axes[1], furn_asd, "ASD (simulated)")
    axes[1].legend()

    fig.tight_layout()
    fig.savefig("cycle_examples.png", dpi=120)
    print("Saved cycle_examples.png")


if __name__ == "__main__":
    main()
