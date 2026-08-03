from pathlib import Path
import ollama

image_path = next(Path("uploads/images").glob("*"))

print(image_path)

response = ollama.chat(
    model="qwen2.5vl:3b",
    messages=[
        {
            "role": "user",
            "content": "Describe this image.",
            "images": [str(image_path)]
        }
    ]
)

print(response)