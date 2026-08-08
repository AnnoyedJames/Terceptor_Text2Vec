"""Project embeddings from output.txt into an interactive 3D or 2D map."""

import argparse
import ast
from pathlib import Path

import numpy as np
import plotly.express as px
import umap


def load_embeddings(path: Path) -> tuple[list[str], np.ndarray]:
    labels = []
    vectors = []

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            label, vector = ast.literal_eval(line)
        except (SyntaxError, ValueError) as error:
            raise ValueError(f"Invalid embedding on line {line_number} of {path}.") from error

        if not isinstance(label, str):
            raise ValueError(f"Expected a text label on line {line_number} of {path}.")

        vectors.append(np.asarray(vector, dtype=np.float32))
        labels.append(label)

    if not vectors:
        raise ValueError(f"No embeddings found in {path}.")

    try:
        return labels, np.vstack(vectors)
    except ValueError as error:
        raise ValueError("All embeddings must have the same number of dimensions.") from error


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("output.txt"))
    parser.add_argument("--output", type=Path, default=Path("embedding_visualization.html"))
    parser.add_argument("--dimensions", type=int, choices=(2, 3), default=3)
    args = parser.parse_args()

    labels, vectors = load_embeddings(args.input)
    minimum_embeddings = args.dimensions + 2
    if len(labels) < minimum_embeddings:
        raise ValueError(
            f"{args.dimensions}D UMAP requires at least {minimum_embeddings} embeddings."
        )
    points = umap.UMAP(
        n_components=args.dimensions,
        metric="cosine",
        n_neighbors=min(15, len(labels) - 1),
        min_dist=0.1,
        random_state=42,
        n_jobs=1,
    ).fit_transform(vectors)

    if args.dimensions == 2:
        figure = px.scatter(x=points[:, 0], y=points[:, 1], hover_name=labels)
        marker_size = 8
        figure.update_traces(
            marker={"size": marker_size},
            mode="markers+text",
            text=labels,
            textposition="top center",
        )
        label_buttons = [
            {
                "label": "Show labels",
                "method": "restyle",
                "args": [{"mode": "markers+text"}],
            },
            {
                "label": "Hide labels",
                "method": "restyle",
                "args": [{"mode": "markers"}],
            },
        ]
    else:
        figure = px.scatter_3d(
            x=points[:, 0], y=points[:, 1], z=points[:, 2], hover_name=labels
        )
        marker_size = 4
        annotations = [
            {
                "x": x,
                "y": y,
                "z": z,
                "text": label,
                "showarrow": False,
                "xanchor": "left",
                "yanchor": "bottom",
                "xshift": 6,
                "yshift": 6,
            }
            for (x, y, z), label in zip(points, labels)
        ]
        figure.update_traces(marker={"size": marker_size}, mode="markers")
        figure.update_layout(scene={"annotations": annotations})
        label_buttons = [
            {
                "label": "Show labels",
                "method": "relayout",
                "args": [{"scene.annotations": annotations}],
            },
            {
                "label": "Hide labels",
                "method": "relayout",
                "args": [{"scene.annotations": []}],
            },
        ]

    figure.update_layout(
        title=f"Embedding visualization ({args.dimensions}D UMAP)",
        updatemenus=[
            {
                "type": "buttons",
                "direction": "right",
                "showactive": True,
                "x": 1,
                "xanchor": "right",
                "y": 1.15,
                "yanchor": "top",
                "buttons": label_buttons,
            }
        ],
    )
    figure.write_html(args.output, auto_open=True)
    print(f"Wrote interactive visualization to {args.output}")


if __name__ == "__main__":
    main()
