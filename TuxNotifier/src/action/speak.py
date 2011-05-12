from action.printAction import PrintAction

class SpeakAction():

    def __init__(self, text):
        self.text = text
        
    def setTux(self, tux):
        self.tux = tux
        
    def execute(self):
        PrintAction(self.text, "tux_speak")
        self.tux.speak(str(self.text))
