from data_models import ChatState


def start_node(state: ChatState):
    print(f"User: {state.user_input}")
    return state


def detect_intent(state: ChatState):
    if state.user_input[-1] == '?':
        state.intent = "question"
    else:
        state.intent = "command"
    return state


def handle_question(state: ChatState):
    state.response = "Nice question"
    return state


def handle_command(state: ChatState):
    state.response = "Nice command"
    return state


def handle_response(state: ChatState):
    print(f"Assistant: {state.response}")
    return state
