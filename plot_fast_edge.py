import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import os


def y_fmt(x, y):
    return f"{int(y)}X"


# set width of bar
barWidth = 0.1


fast_edge_on = {
    "gen_rand_life": {
        "lat": 5.989,
        "mem": 16087,
        "redis": 4,
        "db": 66,
        "object_saved": 8009,
    },
    "get_latest_day": {
        "lat": 5.84,
        "mem": 16101,
        "redis": 8077,
        "db": 0,
        "object_saved": 8024,
    },
}

fast_edge_off = {
    "gen_rand_life": {
        "lat": 6.271,
        "mem": 16087,
        "redis": 4,
        "db": 66,
        "object_saved": 15817,
    },
    "get_latest_day": {
        "lat": 6.581,
        "mem": 16133,
        "redis": 16132,
        "db": 0,
        "object_saved": 0,
    },
}

fig, axes = plt.subplots(1, 2, figsize=(6, 1.75))

baseline = [1, 1]

# plot latency for gen_rand_life and get_latest_day
ax = axes[0]
xs = [1, 1 + barWidth * 3]
ax.bar(
    xs,
    baseline,
    color="lightgray",
    width=barWidth,
    hatch="//",
    edgecolor="grey",
    label="Baseline",
)
xs = [x + barWidth for x in xs]
ax.bar(
    xs,
    [
        fast_edge_off["gen_rand_life"]["lat"] / fast_edge_on["gen_rand_life"]["lat"],
        fast_edge_off["get_latest_day"]["lat"] / fast_edge_on["get_latest_day"]["lat"],
    ],
    color="aquamarine",
    width=barWidth,
    hatch=".",
    edgecolor="grey",
    label="Fast Edge",
)
ax.set_ylabel(f"Lat. Speedup(X)", fontsize=10)
xticks = [x - barWidth / 2 for x in xs]
ax.set_xticks(xticks)
ax.set_xticklabels(["create", "walk"])
ax.set_ylim(0.9, 1.2)

# plot # of objects touched
ax = axes[1]
xs = [1, 1 + barWidth * 3]
baseline = [100, 100]
ax.bar(
    xs,
    baseline,
    color="lightgray",
    width=barWidth,
    hatch="//",
    edgecolor="grey",
    label="Baseline",
)
xs = [x + barWidth for x in xs]
ax.bar(
    xs,
    [
        int(
            # 100
            # / (
            #     fast_edge_off["gen_rand_life"]["redis"]
            #     / fast_edge_on["gen_rand_life"]["redis"]
            # )
            50  # This should be 50. the redis number reported from the logs does not repersent number of objects touched.
        ),
        int(
            100
            / (
                fast_edge_off["get_latest_day"]["redis"]
                / fast_edge_on["get_latest_day"]["redis"]
            )
        ),
    ],
    color="aquamarine",
    width=barWidth,
    hatch=".",
    edgecolor="grey",
    label="Fast Edge",
)
ax.set_ylabel(f"# Objects (Norm.)", fontsize=8)
ax.yaxis.set_major_formatter(tick.PercentFormatter())
xticks = [x - barWidth / 2 for x in xs]
ax.set_xticks(xticks)
ax.set_xticklabels(["create", "walk"])
ax.set_ylim(0, 110)


plt.tight_layout()
plt.legend(fontsize=10, ncols=1, loc="upper center", bbox_to_anchor=(-1, 1))
plt.savefig("cal_2023_graphs/fast_edge_result.pdf", bbox_inches="tight")
