import ollama

try:
    models = ollama.list()
    print("Successfully connected to Ollama!")
    print("Available models:")
    for model in models['models']:
        print(f"- {model['name']}")
except Exception as e:
    print(f"Error connecting to Ollama: {e}")
