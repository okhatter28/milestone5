from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "olympics.csv.gz"
OUTPUT = ROOT / "figures" / "olympic_profiles.png"

events = [
    "Swimming Men's 100 metres Freestyle",
    "Swimming Women's 100 metres Freestyle",
    "Swimming Men's 200 metres Breaststroke",
    "Swimming Women's 200 metres Breaststroke",
    "Swimming Men's 100 metres Backstroke",
    "Swimming Women's 100 metres Backstroke",
]

df = pd.read_csv(DATA)
plot_data = df.loc[
    df["sport"].eq("Swimming")
    & df["event"].isin(events)
    & df["height"].notna()
    & df["weight"].notna(),
    ["event", "year", "height", "weight"],
].copy()
plot_data["decade"] = (plot_data["year"] // 10) * 10
decades = sorted(plot_data["decade"].unique())
colors = plt.cm.viridis([i / max(len(decades) - 1, 1) for i in range(len(decades))])
decade_colors = dict(zip(decades, colors))

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
fig, axes = plt.subplots(2, 3, figsize=(14, 8.5), sharex=True, sharey=True)
fig.patch.set_facecolor("#071a2d")

for ax, event in zip(axes.flat, events):
    sample = plot_data.loc[plot_data["event"] == event]
    ax.set_facecolor("#0d253f")

    for decade in decades:
        decade_sample = sample.loc[sample["decade"] == decade]
        ax.scatter(
            decade_sample["height"],
            decade_sample["weight"],
            s=8,
            alpha=0.28,
            color=decade_colors[decade],
            linewidths=0,
            rasterized=True,
            label=str(decade),
        )

    ax.set_title(
        event.replace("Swimming ", "") + f"\n{len(sample):,} observations",
        color="white",
        loc="left",
        fontweight="bold",
        fontsize=11,
        pad=10,
    )
    ax.grid(color="white", alpha=0.08, linewidth=0.7)
    ax.tick_params(colors="#b9cfdf", labelsize=8)
    for spine in ax.spines.values():
        spine.set_visible(False)

fig.supxlabel("HEIGHT (CM)", color="#b9cfdf", fontsize=10, y=0.035)
fig.supylabel("WEIGHT (KG)", color="#b9cfdf", fontsize=10, x=0.035)
fig.suptitle(
    "OLYMPIC SWIMMERS ARE BUILT FOR THE EVENT",
    color="white",
    fontsize=22,
    fontweight="bold",
    x=0.055,
    ha="left",
    y=0.97,
)
fig.text(
    0.055,
    0.925,
    "Each dot is an athlete-event record. Color shows the Olympic decade.",
    color="#b9cfdf",
    fontsize=11,
)
fig.text(
    0.945,
    0.025,
    "Source: TidyTuesday / 120 Years of Olympic History",
    color="#7896aa",
    fontsize=8,
    ha="right",
)

plt.xlim(130, 225)
plt.ylim(25, 165)
handles, labels = axes.flat[0].get_legend_handles_labels()
fig.legend(
    handles,
    labels,
    title="Olympic decade",
    loc="lower center",
    ncol=7,
    frameon=False,
    labelcolor="white",
    title_fontsize=9,
    fontsize=8,
)
plt.tight_layout(rect=[0.045, 0.08, 0.98, 0.895], w_pad=1.2, h_pad=2.0)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUTPUT, dpi=190, facecolor=fig.get_facecolor(), bbox_inches="tight")
print(f"Created {OUTPUT} from {len(df):,} total rows; {len(plot_data):,} swimming observations were plotted.")
