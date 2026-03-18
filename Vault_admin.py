import json
import base64
from datetime import datetime

def seal_memory():
    name = input("Classmate Name: ")
    quote = input("Secret Message: ")
    unlock_date = input("Unlock Date (YYYY-MM-DD): ")
    image_url = input("Photo URL (or placeholder link): ")

    # Encode message so it's not plain text in the JSON
    encoded_msg = base64.b64encode(quote.encode()).decode()

    new_memory = {
        "name": name,
        "message": encoded_msg,
        "unlock_date": unlock_date,
        "image": image_url or "https://via.placeholder.com/150"
    }

    # Load existing or create new
    try:
        with open('memories.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(new_memory)

    with open('memories.json', 'w') as f:
        json.dump(data, f, indent=4)
    print(f"✅ {name}'s memory has been added to the vault!")

if __name__ == "__main__":
    seal_memory()
