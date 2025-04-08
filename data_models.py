class ChatState:
    def __init__(self, user_input, chat_history):
        self.user_input = user_input
        self.intent = None
        self.intent_arguments = None
        self.response = None
        self.chat_history = chat_history
