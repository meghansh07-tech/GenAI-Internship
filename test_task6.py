from chatbot.chatbot import ask_question


print("\n--- TEST 1 ---")
response1 = ask_question(
    "What is machine learning?"
)

print("Assistant:", response1)


print("\n--- TEST 2 ---")
response2 = ask_question(
    "अब इसे आसान भाषा में समझाओ।"
)

print("Assistant:", response2)


print("\n--- TEST 3 ---")
response3 = ask_question(
    "¿Puedes darme un ejemplo?"
)

print("Assistant:", response3)