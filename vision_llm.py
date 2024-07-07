import os
from vertexai.preview.generative_models import GenerativeModel
import json

def generate_outfit_combinations(items):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "drgenai-7daf412ca440.json"
    model = GenerativeModel("gemini-1.0-pro")

    # Format the items data for the LLM prompt
    items_str = json.dumps(items, indent=2)
    prompt = f"""Given the following clothing items:

{items_str}

Generate 7 outfit combinations for a week for men, ensuring color coordination and style matching. 
Each outfit should consist of one top and one bottom.
Consider the following rules:
1. Match colors that complement according to men and dont use both dark and bold colours for tops and bottoms.
2. Pair similar styles (e.g., casual with casual, formal with formal).
3. Avoid repeating the same item in the same week for shirts.
4. Try to create a variety of looks throughout the week.

Return the results as a JSON-formatted list of dictionaries, where each dictionary represents a day and contains 'top' and 'bottom' keys with the corresponding item IDs.
Ensure that the output is valid JSON that can be parsed by Python's json.loads() function.

Example output format:
[
  {{"day": 1, "top": 1, "bottom": 4}},
  {{"day": 2, "top": 2, "bottom": 5}},
  ...
]
"""

    response = model.generate_content(prompt)
    
    try:
        # Attempt to parse the response as JSON
        outfit_combinations = json.loads(response.text)
        
        # Validate the structure of the parsed data
        if not isinstance(outfit_combinations, list):
            raise ValueError("Response is not a list")
        
        for outfit in outfit_combinations:
            if not isinstance(outfit, dict) or 'top' not in outfit or 'bottom' not in outfit:
                raise ValueError("Invalid outfit structure")
        
        return outfit_combinations
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Raw response: {response.text}")
        return []
    except ValueError as e:
        print(f"Error validating response structure: {e}")
        print(f"Parsed response: {outfit_combinations}")
        return []