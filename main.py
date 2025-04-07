from langgraph.graph import StateGraph

from data_models import ChatState
from nodes import start_node, handle_command, handle_question, detect_intent, handle_response
from utils import decide_intent

graph = StateGraph(ChatState)

graph.add_node("start", start_node)
graph.add_node("detect_intent", detect_intent)
graph.add_node("handle_question", handle_question)
graph.add_node("handle_command", handle_command)
graph.add_node("handle_response", handle_response)

graph.set_entry_point("start")
graph.add_edge("start", "detect_intent")
graph.add_conditional_edges("detect_intent", decide_intent)
graph.add_edge("handle_question", "handle_response")
graph.add_edge("handle_command", "handle_response")

graph2 = graph.compile()

state = ChatState(user_input="How are you?")
graph2.invoke(state)

