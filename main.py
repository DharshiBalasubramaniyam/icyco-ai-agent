import os
from langchain_google_genai import GoogleGenerativeAI
from langgraph.graph import StateGraph

from data_models import ChatState
from google import genai
from nodes import end, handle_response, start_node, detect_intent, question_answer, filter_products, product_query, handle_unrelated_questions
from utils import get_vector_store

router_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
qa_vector_store = get_vector_store(os.getenv("QA_INDEX_NAME"))       
qa_client = GoogleGenerativeAI(model="gemini-2.0-flash", api_key=os.getenv("GOOGLE_API_KEY"))      

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
graph_builder.add_edge("handle_response", "start")

graph = graph_builder.compile()

graph.invoke(ChatState())

