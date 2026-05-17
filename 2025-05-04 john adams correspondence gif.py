"""Generated from Jupyter notebook: 2025-05-04 john adams correspondence gif

Magics and shell lines are commented out. Run with a normal Python interpreter."""

from collections import Counter

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


def draw_frame(i):
    ax.clear()
    date = dates[i]
    ax.set_title(f"Correspondence: {date}", fontsize=14)
    ax.axis("off")
    nx.draw_networkx_nodes(G, layout, ax=ax, node_size=800, node_color="lightblue")
    nx.draw_networkx_labels(G, layout, ax=ax, font_size=10)
    day_msgs = msgs_by_date[date]
    for row in day_msgs.itertuples(index=False):
        src = layout[row.authors]
        tgt = layout[row.recipients]
        steps = 10
        for j in range(steps):
            interp = src + (tgt - src) * (j / steps)
            ax.plot([src[0], interp[0]], [src[1], interp[1]], color="red", alpha=0.3)


def main():
    ani = animation.FuncAnimation(
        fig, draw_frame, frames=len(dates), interval=300, repeat=False
    )
    gif_path = "john_adams_correspondence_animation.gif"
    ani.save(gif_path, writer="pillow", fps=3)
    gif_path
    post_madison_df.index.min()
    post_madison_df.head()
    post_madison_df["date_from"].min()
    post_madison_df["date_from"].max()


def main() -> None:
    post_madison_df = pd.read_csv("post-madison.csv")

    valid_edges = post_madison_df.dropna(subset=["authors", "recipients"])

    G = nx.DiGraph()

    for row in valid_edges.itertuples(index=False):
        sender = row.authors.strip()
        recipient = row.recipients.strip()
        if G.has_edge(sender, recipient):
            G[sender][recipient]["weight"] += 1
        else:
            G.add_edge(sender, recipient, weight=1)

    plt.figure(figsize=(12, 8))

    pos = nx.spring_layout(G, k=0.5, seed=42)

    nx.draw_networkx_nodes(G, pos, node_size=700, node_color="lightblue")

    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=10, width=1)

    nx.draw_networkx_labels(G, pos, font_size=10, font_family="serif")

    edge_labels = nx.get_edge_attributes(G, "weight")

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title("Correspondence Network (Post-Madison Presidency)")

    plt.axis("off")

    plt.tight_layout()

    plt.savefig("correspondence_network_post_madison.png")

    plt.show()

    file_path = "post-madison.csv"

    df = pd.read_csv(file_path)

    df["date_from"] = pd.to_datetime(df["date_from"])

    df["authors"] = df["authors"].str.strip()

    df["recipients"] = df["recipients"].str.strip()

    adams_df = df[
        (df["authors"] == "Adams, John") | (df["recipients"] == "Adams, John")
    ].dropna(subset=["authors", "recipients"])

    correspondents = []

    for row in adams_df.itertuples(index=False):
        if row.authors == "Adams, John":
            correspondents.append(row.recipients)
        else:
            correspondents.append(row.authors)

    top_corr = {k for k, v in Counter(correspondents).items() if v >= 10}

    adams_filtered = adams_df[
        (adams_df["authors"] == "Adams, John") & adams_df["recipients"].isin(top_corr)
        | (adams_df["recipients"] == "Adams, John") & adams_df["authors"].isin(top_corr)
    ].copy()

    adams_filtered["date_str"] = adams_filtered["date_from"].dt.strftime("%Y-%m-%d")

    dates = sorted(adams_filtered["date_str"].unique())

    msgs_by_date = {d: adams_filtered[adams_filtered["date_str"] == d] for d in dates}

    G = nx.DiGraph()

    for r in adams_filtered.itertuples(index=False):
        G.add_edge(r["authors"], r["recipients"])

    layout = nx.shell_layout(
        G, nlist=[["Adams, John"], [n for n in G.nodes if n != "Adams, John"]]
    )

    fig, ax = plt.subplots(figsize=(8, 8))

    main()


if __name__ == "__main__":
    main()
