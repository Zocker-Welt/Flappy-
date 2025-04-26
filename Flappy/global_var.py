import json

def get(key):
    with open('global.json', 'r') as file:
        data = json.load(file)
        return data.get(key)

def set(key, value):
    with open('global.json', 'r+') as file:
        data = json.load(file)
        data[key] = value
        file.seek(0)
        json.dump(data, file)
        file.truncate()
