# Glacier Communicator Firmware
# Database
# By Johnny Stene

import json

class Database:
    def __init__(self):
        self._phonebook = {}
        self._messages = {}
    
    def load(self, filename): # load from a json file. TODO: when uos gets implemented this will need to change
        print("Loading database from " + filename)
        try:
            with open(filename) as file:
                data = json.load(file)
                self._phonebook = data["phonebook"]
                self._messages = data["messages"]
        except:
            print("Failed to load")

    def save(self, filename): # just dumps to a json file. TODO: when uos gets implemented this will need to change
        print("Saving database to " + filename)
        try:
            with open(filename, "w") as file:
                file.write(json.dumps({"phonebook":self._phonebook,"messages":self._messages}))
        except:
            print("Failed to save")

    def add_phonebook_entry(self, number, name, email=None): # does what it says on the tin
        if number in self._phonebook:
            return False

        self._phonebook[number] = {}
        self._phonebook[number]["name"] = name
        if email:
            self._phonebook[number]["email"] = email

        return True

    def get_name(self, number): # return name for a given number, or, return the number if not in contacts yet
        if not number in self._phonebook:
            return number
        
        return self._phonebook[number]["name"]
    
    def get_email(self, number): # TODO: do we need this? might not even include an email client
        if not number in self._phonebook:
            return None
        
        if not "email" in self._phonebook[number]:
            return None
        
        return self._phonebook[number]["email"]
    
    def add_message_entry(self, message): # take in an sms message object and add it to db
        if not message.number in self._messages:
            self._messages[message.number] = []
        
        time = 0 # TODO: calculate seconds since epoch based on message.date and message.time
        self._messages[message.number].append({"time":time, "message": message.message})
    
    def get_message_thread(self, number): # return all messages with a certain number sorted by time
        if not number in self._messages:
            return []
        
        return sorted(self._messages[number], key=lambda t: t["time"])