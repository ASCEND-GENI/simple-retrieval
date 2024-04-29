from langchain import hub

# Prompt
prompt = hub.pull("rlm/rag-prompt")
print(prompt)

with open("prompt.json", "w") as f:
    f.write(prompt)