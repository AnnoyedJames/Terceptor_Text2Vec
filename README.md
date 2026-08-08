# Terceptor Text2Vec

Embeds short text terms into 1024-dimensional vectors using [BGE-M3](https://huggingface.co/BAAI/bge-m3). Uses GPU automatically if available.

## Setup

Requires Python 3.13 and a CUDA-capable GPU (optional but faster).

```
setup.bat
```

This creates a virtual environment and installs all dependencies. The BGE-M3 model (~2.3 GB) downloads on first run.

## Running

Double-click `start_embed.bat`, or run:

```
.\start_embed.bat
```

It creates the virtual environment and installs any missing dependencies before
embedding the terms in `input.txt`.

## Input

A plain `.txt` file named `input.txt` containing comma-separated terms (1–2 words each). Underscores are treated as spaces.

```
holy, fire, goblin, earth, winter, demon_prince
```

## Output

`output.txt` — one entry per line, each a `[term, vector]` pair:

```
['holy', [0.0234, -0.0412, ..., 0.0071]]
['fire',  [0.0198, -0.0387, ..., 0.0103]]
```

Vectors are FP32, 1024 dimensions.

## Visualization

After generating `output.txt`, create an interactive 3D UMAP map:

```
.\start_visualize.bat
```

This opens `embedding_visualization.html` in the browser. Labels are visible by
default, and the Show labels/Hide labels control lets you declutter the map.
Hovering a point also shows its term. The projection uses cosine distance with
up to 15 neighbors, `min_dist=0.1`, and a fixed random seed.

For a 2D visualization:

```
venv\Scripts\python.exe visualize.py --dimensions 2
```

The map is useful for inspecting clusters and neighborhoods, but its 2D/3D
distances are not exact cosine similarities from the original embedding space.
