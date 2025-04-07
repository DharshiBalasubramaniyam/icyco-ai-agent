def decide_intent(state):
    if state.intent == "question":
        return "handle_question"
    return "handle_command"
