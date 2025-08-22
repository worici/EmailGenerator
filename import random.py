import random
import json
import os
from datetime import datetime

class EmailGenerator:
    def __init__(self):
        self.domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com", "icloud.com"]
        self.first_names = {
            'male': ["James", "Michael", "William", "David", "John", "Robert", "Thomas", "Charles", "Christopher", "Daniel"],
            'female': ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen"],
            'neutral': ["Alex", "Taylor", "Jordan", "Casey", "Riley", "Morgan", "Avery", "Skyler", "Quinn", "Peyton"]
        }
        self.last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        self.cultures = {
            'generic': {'first': self.first_names, 'last': self.last_names},
            'irish': {'first': ["Sean", "Liam", "Siobhan", "Maeve"], 'last': ["O'Connor", "Murphy", "Kelly", "Ryan"]},
            'italian': {'first': ["Giovanni", "Sofia", "Marco", "Giulia"], 'last': ["Rossi", "Russo", "Ferrari", "Esposito"]},
            'japanese': {'first': ["Hiroshi", "Yuki", "Sakura", "Aiko"], 'last': ["Sato", "Suzuki", "Takahashi", "Tanaka"]},
            'indian': {'first': ["Arjun", "Priya", "Rahul", "Anika"], 'last': ["Patel", "Sharma", "Kumar", "Singh"]}
        }
        self.formats = ["{first}.{last}@{domain}", "{first}{last}@{domain}", "{first}_{last}@{domain}", 
                        "{first}{random_num}@{domain}", "{initial}{last}@{domain}"]
        self.history_file = "email_history.json"
        self.history = []

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)

    def save_history(self, email_data):
        self.history.append(email_data)
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=4)

    def validate_input(self, value, options):
        if value.lower() in options:
            return value.lower()
        raise ValueError(f"Invalid choice. Choose from: {', '.join(options)}")

    def validate_count(self, count):
        try:
            count = int(count)
            if 1 <= count <= 50:
                return count
            raise ValueError("Count must be between 1 and 50.")
        except ValueError:
            raise ValueError("Invalid number. Please enter a number between 1 and 50.")

    def generate_email(self, gender, culture):
        if culture == 'generic':
            first_names = self.cultures[culture]['first'][gender]
            last_names = self.cultures[culture]['last']
        else:
            first_names = self.cultures[culture]['first']
            last_names = self.cultures[culture]['last']
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        domain = random.choice(self.domains)
        email_format = random.choice(self.formats)
        
        random_num = str(random.randint(1, 999)) if "{random_num}" in email_format else ""
        initial = first_name[0].lower() if "{initial}" in email_format else ""
        
        email = email_format.format(
            first=first_name.lower(),
            last=last_name.lower(),
            initial=initial,
            random_num=random_num,
            domain=domain
        ).replace(" ", "")
        
        return email

    def generate_multiple_emails(self, count, gender, culture):
        emails = []
        for _ in range(count):
            email = self.generate_email(gender, culture)
            email_data = {
                'email': email,
                'gender': gender,
                'culture': culture,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            emails.append(email_data)
            self.save_history(email_data)
        return emails

    def display_history(self):
        if not self.history:
            print("No history available.")
            return
        print("\nEmail Generation History:")
        for entry in self.history:
            print(f"Time: {entry['timestamp']}, Email: {entry['email']}, "
                  f"Gender: {entry['gender'].capitalize()}, Culture: {entry['culture'].capitalize()}")

    def search_emails(self, prefix, gender, culture):
        matching_emails = [entry['email'] for entry in self.history 
                          if entry['email'].lower().startswith(prefix.lower()) 
                          and entry['gender'] == gender 
                          and entry['culture'] == culture]
        return matching_emails

    def run(self):
        self.load_history()
        while True:
            print("\nAdvanced Email Generator")
            print("1. Generate Emails")
            print("2. View History")
            print("3. Search Emails by Prefix")
            print("4. Exit")
            choice = input("Choose an option (1-4): ")

            if choice == '1':
                try:
                    count = self.validate_count(input("How many emails to generate? (1-50): "))
                    gender = self.validate_input(input("Choose gender (male/female/neutral): "), 
                                               ['male', 'female', 'neutral'])
                    culture = self.validate_input(input(f"Choose culture ({', '.join(self.cultures.keys())}): "), 
                                                self.cultures.keys())
                    emails = self.generate_multiple_emails(count, gender, culture)
                    print("\nGenerated Emails:")
                    for email_data in emails:
                        print(f"{email_data['email']} (Gender: {email_data['gender'].capitalize()}, "
                              f"Culture: {email_data['culture'].capitalize()})")
                except ValueError as e:
                    print(e)
            elif choice == '2':
                self.display_history()
            elif choice == '3':
                try:
                    prefix = input("Enter email prefix to search: ").strip()
                    gender = self.validate_input(input("Choose gender (male/female/neutral): "), 
                                               ['male', 'female', 'neutral'])
                    culture = self.validate_input(input(f"Choose culture ({', '.join(self.cultures.keys())}): "), 
                                                self.cultures.keys())
                    matching_emails = self.search_emails(prefix, gender, culture)
                    if matching_emails:
                        print("\nMatching Emails:")
                        for email in matching_emails:
                            print(email)
                    else:
                        print("No emails found with that prefix.")
                except ValueError as e:
                    print(e)
            elif choice == '4':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    generator = EmailGenerator()
    generator.run()