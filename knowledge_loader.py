def load_knowledge(file_path="knowledge.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return text