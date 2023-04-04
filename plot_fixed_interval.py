import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import os
import json
import csv
import copy


def y_fmt(x, y):
    return f"{int(y)}X"


# set width of bar
barWidth = 0.1

# set height of bar
# TRACES = ["dynamic"]
# MEM = "8g"
# RESULT_DIR = f"dynamic_regular_eval_no_queue_mem_{MEM}"

TECH = [
    "default",
    "regular_reevaluation",
    "action_pressure_trigger",
    "action_pressure_trigger_prediction",
    "oracle",
]
POLICIES = ["all_remote", "all_local", "evaluation"]
APP = [
    "sentence_pairing",
    "discussion_analysis",
    # "flight_chatbot",
    # "restaurant_chatbot",
    # "zeroshot_faq_bot",
    # "flow_analysis",
]
METRIC = ["throughput", "average_latency", "95th_latency"]
AXIS_LABELS = {
    "throughput": "QPS",
    "average_latency": "Avg. Lat.",
    "95th_latency": "95th. Lat.",
}
# MEMS = [4, 6, 8]

# DIRECTORY = "synthetic_apps_results"
FILE = f"synthetic_apps_results.json"
with open(FILE, "r") as fin:
    results = json.load(fin)

for app in APP:
    # get all local and all remote result
    # mem_4_result_file = os.path.join(DIRECTORY, f"{app}-4.json")
    # # A hack some data is missing atm
    # if not os.path.isfile(mem_4_result_file):
    #     mem_4_result_file = os.path.join(DIRECTORY, f"{app}-6.json")
    # with open(mem_4_result_file, "r") as fin:
    #     data = json.load(fin)[app]
    data = results[app]

    fig, axes = plt.subplots(1, 3, figsize=(6, 1.75))
    formatter = tick.FormatStrFormatter("?%1.1f")
    for metric, ax in zip(METRIC, axes.ravel()):
        print(metric)
        # ax.yaxis.set_major_formatter(formatter)
        all_local = data["all_local"]["walker_level"]["walker_run"]["all"][metric]
        all_remote = data["all_remote"]["walker_level"]["walker_run"]["all"][metric]
        jsorc = data["evaluation"]["walker_level"]["walker_run"]["all"][metric]
        print(jsorc)

        # turn this into a list of one so we can have different bar colors
        all_local = [all_local]
        all_remote = [all_remote]

        eval_lats = []
        eval_legends = []

        # normalize to all remote
        if "latency" in metric:
            jsorc = list(np.divide(all_remote, jsorc))
        elif "throughput" in metric:
            jsorc = list(np.divide(jsorc, all_remote))
        eval_lats.append(jsorc)
        eval_legends.append("JSORC")
        print(eval_lats)

        if "latency" in metric:
            all_local = list(np.divide(all_remote, all_local))
        elif "throughput" in metric:
            all_local = list(np.divide(all_local, all_remote))
        all_remote = list(np.divide(all_remote, all_remote))
        # avg_lats = []
        # for policy in POLICIES:
        #     avg_lats.append(
        #         [results[app][policy]["walker_level"]["walker_run"]["all"][metric]]
        #     )
        br_all_remote = np.arange(len(all_remote))  # 1 for all remote
        brs_eval = []
        for i in range(len(eval_lats)):
            brs_eval.append([x + barWidth * (i + 1) for x in br_all_remote])
        br_all_local = [x + barWidth for x in brs_eval[-1]]

        ax.axhline(y=1, ls="--", color="black")

        # Make the plot
        ax.bar(
            br_all_remote,
            all_remote,
            color="dimgray",
            width=barWidth,
            hatch="x",
            edgecolor="grey",
            label="Microservices",
        )
        for i in range(len(brs_eval)):
            ax.bar(
                brs_eval[i],
                eval_lats[i],
                color="darkturquoise",
                width=barWidth,
                hatch="||",
                edgecolor="grey",
                label=eval_legends[i],
            )
        ax.bar(
            br_all_local,
            all_local,
            color="paleturquoise",
            width=barWidth,
            hatch="+",
            edgecolor="grey",
            label="Upper Bound",
        )
        ax.set_ylabel(f"Norm. {AXIS_LABELS[metric]}(X)", fontsize=11)
        # plt.xticks([r + barWidth for r in range(len(avg_lats[0]))], TRACES)
        ax.set_xticks([])
        # plt.title("Dynamic Trace, Different JSORC Tech, with node memory capacity=2GB")

        # Adding Xticks
        # plt.xlabel('Trace', fontweight ='bold', fontsize = 10)

        # plt.legend(fontsize=14, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.24))
    plt.tight_layout()
    if app == "discussion_analysis":
        plt.legend(
            fontsize=12, ncols=3, loc="upper center", bbox_to_anchor=(-1.1, 1.28)
        )

    # plt.savefig(f"{DIRECTORY}/{app}-{metric}.pdf", bbox_inches="tight")
    plt.savefig(f"cal_2023_graphs/{app}-all.pdf", bbox_inches="tight")
