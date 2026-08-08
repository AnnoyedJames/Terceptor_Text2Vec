# Terceptor Text2Vec

Embeds short text terms into 1024-dimensional vectors using [BGE-M3](https://huggingface.co/BAAI/bge-m3). Uses GPU automatically if available.

## Setup

Requires Python 3.13 and a CUDA-capable GPU (optional but faster).

```
setup.bat
```

This creates a virtual environment and installs all dependencies. The BGE-M3 model (~2.3 GB) downloads on first run.

## Input

A plain `.txt` file named `input.txt` containing comma-separated terms (1–2 words each). Underscores are treated as spaces.

```
fire_truck, ambulance, police car, helicopter, jet_ski
```

## Running

```
venv\Scripts\python.exe embed.py
```

## Output

`output.txt` — one entry per line, each a `[term, vector]` pair:

```
['fire truck', [0.0234, -0.0412, ..., 0.0071]]
['ambulance',  [0.0198, -0.0387, ..., 0.0103]]
```

Vectors are FP32, 1024 dimensions.
