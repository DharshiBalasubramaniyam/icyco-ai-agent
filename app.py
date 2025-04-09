from langgraph.graph import StateGraph

from data_models import ChatState
from nodes import end, handle_response, start_node, detect_intent, question_answer, filter_products, product_query, handle_unrelated_questions

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


graph_builder = StateGraph(ChatState)

graph_builder.add_node("start", start_node)
graph_builder.add_node("detect_intent", detect_intent)
graph_builder.add_node("question_answer", question_answer)
graph_builder.add_node("filter_products", filter_products)
graph_builder.add_node("product_query", product_query)
graph_builder.add_node("handle_unrelated_questions", handle_unrelated_questions)
graph_builder.add_node("handle_response", handle_response)
graph_builder.add_node("end_node", end)

graph_builder.set_entry_point("start")
graph_builder.set_finish_point("end_node")
graph_builder.add_edge("start", "detect_intent")
graph_builder.add_conditional_edges("detect_intent", lambda state: state.intent)
graph_builder.add_edge("question_answer", "handle_response")
graph_builder.add_edge("filter_products", "handle_response")
graph_builder.add_edge("product_query", "handle_response")
graph_builder.add_edge("handle_unrelated_questions", "handle_response")
graph_builder.add_edge("handle_response", "end_node")

graph = graph_builder.compile()

@app.route('/test', methods=['GET'])
def test():
    return "API is working!"


@app.post('/chat')
def chat():
   data = request.get_json()

   query = data["query"]
   chat_history = data["chat_history"]

   state = graph.invoke(ChatState(user_input=query, chat_history=chat_history))
   return jsonify({
        "result": state.response,
   }), 200

if __name__ == '__main__':
   app.run()
