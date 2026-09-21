from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

# File locations
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "olympics.csv.gz"
OUTPUT = ROOT / "figures" / "olympic_profiles.png"

# Read the Olympic dataset
df = pd.read_csv(DATA)

# Confirm that the dataset contains thousands of observations
assert len(df) >= 1000, "The assignment requires thousands of observations."

# Sports included in the visualization
sports = [
    "Basketball",
    "Volleyball",
    "Swimming",
    "Rowing",
    "Athletics",
    "Cycling",
    "Gymnastics",
    "Weightlifting",
]

# Keep observations with valid height and weight measurements
plot_data = df.loc[
    df["sport"].isin(sports)
    & df["height"].notna()
    & df["weight"].notna(),
    ["sport", "height", "weight"],
]

# Set up the graphic
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10
})

fig, axes = plt.subplots(
    2,
    4,
    figsize=(15, 8.6),
    sharex=True,
    sharey=True
)

fig.patch.set_facecolor("#071a2d")

# Create one scatterplot for each sport
for ax, sport in zip(axes.flat, sports):
    sample = plot_data.loc[plot_data["sport"] == sport]

    ax.set_facecolor("#0d253f")

    ax.scatter(
        sample["height"],
        sample["weight"],
        s=7,
        alpha=0.10,
        color="#4de2d0",
        linewidths=0,
        rasterized=True
    )

    # Calculate the median height and weight
    median_height = sample["height"].median()
    median_weight = sample["weight"].median()

    # Add a marker for the median athlete
    ax.scatter(
        median_height,
        median_weight,
        marker="P",
        s=115,
        color="#ffd166",
        edgecolor="white",
        linewidth=1.2,
        zorder=5
    )

    ax.set_title(
        f"{sport}\n{len(sample):,} observations",
        color="white",
        loc="left",
        fontweight="bold",
        fontsize=11,
        pad=10
    )

    ax.grid(
        color="white",
        alpha=0.08,
        linewidth=0.7
    )

    ax.tick_params(
        colors="#b9cfdf",
        labelsize=8
    )

    for spine in ax.spines.values():
        spine.set_visible(False)

# Add labels and titles
fig.supxlabel(
    "HEIGHT (CM)",
    color="#b9cfdf",
    fontsize=10,
    y=0.035
)

fig.supylabel(
    "WEIGHT (KG)",
    color="#b9cfdf",
    fontsize=10,
    x=0.035
)

fig.suptitle(
    "OLYMPIC BODIES ARE BUILT FOR THE EVENT",
    color="white",
    fontsize=22,
    fontweight="bold",
    x=0.055,
    ha="left",
    y=0.97
)

fig.text(
    0.055,
    0.925,
    "Each dot is one athlete-event record. "
    "The gold marker shows the median athlete in each sport.",
    color="#b9cfdf",
    fontsize=11
)

fig.text(
    0.945,
    0.025,
    "Source: TidyTuesday / 120 Years of Olympic History",
    color="#7896aa",
    fontsize=8,
    ha="right"
)

# Set consistent axes for comparison
plt.xlim(130, 225)
plt.ylim(25, 165)

plt.tight_layout(
    rect=[0.045, 0.055, 0.98, 0.895],
    w_pad=1.2,
    h_pad=2.0
)

# Save the completed graphic
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

fig.savefig(
    OUTPUT,
    dpi=190,
    facecolor=fig.get_facecolor(),
    bbox_inches="tight"
)

print(
    f"Created {OUTPUT} from {len(df):,} total rows; "
    f"{len(plot_data):,} observations were plotted."
)
