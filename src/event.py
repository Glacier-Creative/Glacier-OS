# Glacier Communicator Firmware
# Event System
# By Johnny Stene

class EventSystem:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_name, callback): # add function to list to be called when event triggers
        if not event_name in self._subscribers:
            self._subscribers[event_name] = []
        
        self._subscribers[event_name].append(callback)
    
    def unsubscribe(self, event_name, callback): # remove function from list. don't know if this works but it would be really sick if it did
        if event_name in self._subscribers:
            if callback in self._subscribers[event_name]:
                self._subscribers[event_name].remove(callback)
    
    def publish(self, event_name, **kwargs): # trigger an event. also i learned about kwargs! 
        if event_name in self._subscribers:
            for callback in self._subscribers[event_name]:
                callback(**kwargs)

