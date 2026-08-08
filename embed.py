from FlagEmbedding import BGEM3FlagModel

INPUT_FILE = "input.txt"
OUTPUT_FILE = "output.txt"
MODEL_NAME = "BAAI/bge-m3"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw = f.read()

terms = [t.strip().replace("_", " ") for t in raw.split(",") if t.strip()]

model = BGEM3FlagModel(MODEL_NAME, use_fp16=True)  # uses GPU if available, else CPU
result = model.encode(terms, batch_size=32)
dense_vecs = result["dense_vecs"]  # shape: (N, dim), float32

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for term, vec in zip(terms, dense_vecs):
        f.write(f"[{repr(term)}, {vec.tolist()}]\n")
        print(f"Tag:{term} vectorized as {vec}")

print(f"Wrote {len(terms)} embeddings to {OUTPUT_FILE}")
