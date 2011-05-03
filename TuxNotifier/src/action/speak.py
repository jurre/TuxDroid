
class SpeakAction():

    def __init__(self, text):
        self.text = text
        
    def setTux(self, tux):
        self.tux = tux
        
    def execute(self):
        self.tux.speak(self.text)
