import time

from models.llm_model import get_llm

llm = get_llm()

start = time.perf_counter()

print("Starting...")

for i, chunk in enumerate(llm.stream("Hi"), 1):

    elapsed = time.perf_counter() - start

    print(
        f"Chunk {i} | {elapsed:.2f}s | {repr(chunk.content)}",
        flush=True
    )

print("DONE")