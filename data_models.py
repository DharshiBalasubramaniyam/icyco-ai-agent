class ChatState:
    def __init__(self, user_input):
        self.user_input = user_input
        self.intent = None
        self.response = None