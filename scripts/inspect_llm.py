from app.llm import LocalLLM


llm = LocalLLM()

response = llm.generate(
    "say just a random word"
)

print(response)
