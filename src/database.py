# Glacier Communicator Firmware
# Database
# By Johnny Stene

import json

class Database:
    def __init__(self):
        self._phonebook = {}
        self._messages = {}
    
    def load(self, filename):
        print("Loading database from " + filename)
        try:
            with open(filename) as file:
                data = json.load(file)
                self._phonebook = data["phonebook"]
                self._messages = data["messages"]
        except:
            print("Failed to load")

    def save(self, filename):
        print("Saving database to " + filename)
        try:
            with open(filename, "w") as file:
                file.write(json.dumps({"phonebook":self._phonebook,"messages":self._messages}))
        except:
            print("Failed to save")

    def add_phonebook_entry(self, number, name, email=None):
        if number in self._phonebook:
            return False

        self._phonebook[number] = {}
        self._phonebook[number]["name"] = name
        if email:
            self._phonebook[number]["email"] = email

        return True

    def get_name(self, number):
        if not number in self._phonebook:
            return number
        
        return self._phonebook[number]["name"]
    
    def get_email(self, number):
        if not number in self._phonebook:
            return None
        
        if not "email" in self._phonebook[number]:
            return None
        
        return self._phonebook[number]["email"]
    
    def add_message_entry(self, message):
        if not message.number in self._messages:
            self._messages[message.number] = []
        
        time = 0 # TODO: calculate seconds since epoch based on message.date and message.time
        self._messages[message.number].append({"time":time, "message": message.message})
    
    def get_message_thread(self, number):
        if not number in self._messages:
            return []
        
        return sorted(self._messages[number], key=lambda t: t["time"])