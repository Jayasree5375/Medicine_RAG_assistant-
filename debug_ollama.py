import ollama
import json

try:
    models_info = ollama.list()
    print(f"Type of models_info: {type(models_info)}")
    print(f"Raw models_info: {models_info}")
    
    if 'models' in models_info:
        print(f"Type of models list: {type(models_info['models'])}")
        if len(models_info['models']) > 0:
            first_model = models_info['models'][0]
            print(f"Type of first model: {type(first_model)}")
            print(f"First model content: {first_model}")
            try:
                print(f"Accessing ['name']: {first_model['name']}")
            except Exception as e:
                print(f"Error accessing ['name']: {e}")
            
            try:
                print(f"Accessing .model: {first_model.model}")
            except Exception as e:
                print(f"Error accessing .model: {e}")

except Exception as e:
    print(f"Error: {e}")
