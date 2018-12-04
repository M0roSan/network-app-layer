import json

class Message:

    filename = None
    command = None
    payload = None

    def __init__(self, filename = None, command = None, payload = None):
        self.filename = filename
        self.command = command
        self.payload = payload
    
    def export(self):
        return json.dumps({
            'filename': self.filename,
            'command': self.command,
            'payload': self.payload
        })
    
    def decode(self, data):
        data = json.loads(data)
        self.filename = data['filename'] 
        self.command = data['command']
        self.payload = data['payload']