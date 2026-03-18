import json
import os
import base64
from datetime import datetime

class YearBookVault:
    def __init__(self, filename="highschool_vault.json"):
        self.filename = filename
        self.vault = self.load_vault()

    def load_vault(self):
        """Loads data from the JSON file or creates a new dictionary."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return {}

    def save_vault(self):
        """Saves the current vault state to the JSON file."""
        with open(self.filename, 'w') as f:
            json.dump(self.vault, f, indent=4)

    def obfuscate(self, text):
        """Simple encoding so quotes aren't plain text in the JSON file."""
        return base64.b64encode(text.encode()).decode()

    def deobfuscate(self, encoded_text):
        """Decodes the hidden text for display."""
        return base64.b64decode(encoded_text.encode()).decode()

    def add_memory(self):
        print("\n--- 🔒 SEAL A NEW MEMORY ---")
        name = input("Classmate Name: ").strip().title()
        superlative = input(f"What was {name} 'Most Likely To' do? ")
        message = input(f"Write a secret message/quote for {name}: ")
        
        print("When should this be unlocked? (Format: YYYY-MM-DD)")
        unlock_date = input("Unlock Date: ")

        try:
            # Validate date format
            datetime.strptime(unlock_date, "%Y-%m-%d")
            
            self.vault[name] = {
                "superlative": superlative,
                "message": self.obfuscate(message),  # Hide the message
                "unlock_date": unlock_date,
                "created_at": datetime.now().strftime("%Y-%m-%d")
            }
            self.save_vault()
            print(f"\n✅ Memory for {name} sealed until {unlock_date}!")
        except ValueError:
            print("\n❌ Invalid date format! Memory not saved.")

    def view_vault(self):
        if not self.vault:
            print("\nThe vault is currently empty.")
            return

        print(f"\n{'NAME':<15} | {'STATUS':<12} | {'SUPERLATIVE':<20} | {'MESSAGE'}")
        print("-" * 80)

        for name, data in self.vault.items():
            unlock_dt = datetime.strptime(data['unlock_date'], "%Y-%m-%d")
            is_locked = datetime.now() < unlock_dt
            
            if is_locked:
                status = "🔒 LOCKED"
                display_msg = f"Available on {data['unlock_date']}"
            else:
                status = "🔓 OPEN"
                display_msg = self.deobfuscate(data['message'])

            print(f"{name:<15} | {status:<12} | {data['superlative']:<20} | {display_msg}")

    def countdown_stats(self):
        """Shows how many memories are still waiting to be opened."""
        locked_count = sum(1 for d in self.vault.values() if datetime.now() < datetime.strptime(d['unlock_date'], "%Y-%m-%d"))
        print(f"\n📊 Vault Stats: {len(self.vault)} total memories | {locked_count} still under lock and key.")

def main():
    app = YearBookVault()
    
    while True:
        print("\n======================================")
        print("🎓 SENIOR YEAR DIGITAL TIME CAPSULE 🎓")
        print("======================================")
        print("1. Add a Classmate/Memory")
        print("2. Open the Vault")
        print("3. View Statistics")
        print("4. Exit")
        
        choice = input("\nWhat would you like to do? ")

        if choice == "1":
            app.add_memory()
        elif choice == "2":
            app.view_vault()
        elif choice == "3":
            app.countdown_stats()
        elif choice == "4":
            print("\nGoodbye! Stay in touch. 🎓")
            break
        else:
            print("\nInvalid choice, try again.")

if __name__ == "__main__":
    main()
