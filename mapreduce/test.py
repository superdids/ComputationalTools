import json

class Test:
    def start(self):
        print(json.load(open('jsun.json')))

Test().start()

