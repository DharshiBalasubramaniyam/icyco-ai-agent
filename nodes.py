from data_models import ChatState

from google.genai import types

from function_declarations import f_question_answer, f_filter_products, f_handle_unrelated_questions, f_product_query
from tools import product_filter_tool, product_query_tool, question_answer_tool
from main import router_client


def start_node(state: ChatState):
    state.user_input = input("User: ")
    return state

def detect_intent(state: ChatState):
    if state.user_input.lower() == "exit":
        state.intent = "end"
        print(f"Assistant: Thank you for using Icyco! Have a great day!")
        return state
    
    tools = types.Tool(function_declarations=[f_question_answer, f_filter_products, f_handle_unrelated_questions, f_product_query])
    config = types.GenerateContentConfig(tools=[tools])

    response = router_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=state.user_input,
        config=config,
    )

    if response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        print(f"Function to call: {function_call.name}")
        print(f"Arguments: {function_call.args}")
        state.intent = function_call.name
        state.intent_arguments = function_call.args
    else:
        state.response = response.text if hasattr(response, 'text') else f"Oops! Something went wrong while processing your request."
        state.intent = "handle_response"
        state.intent_arguments = {'question': state.user_input}
    return state

def question_answer(state: ChatState):
    state.response = question_answer_tool(state.user_input)
    return state

def filter_products(state: ChatState):
    keywords = state.intent_arguments.get('keywords', [])
    start_price = state.intent_arguments.get('start_price', -1)
    end_price = state.intent_arguments.get('end_price', -1)
    start_rating = state.intent_arguments.get('start_rating', -1)
    end_rating = state.intent_arguments.get('end_rating', -1)

    filtered_products = product_filter_tool(keywords, start_price, end_price, start_rating, end_rating)
    if not filtered_products:
        state.response = "Sorry, but I couldn't find any products that match your criteria. Please try again with different filters!"
        return state

    state.response = "Here are some products that match your criteria:\n"
    for product in filtered_products:
        state.response += f"- {product['name']}: {product['description']} (Rating: {product['rating']})\n"
    state.response += "\n Let me know if you have any other questions!"
    
    return state

def product_query(state: ChatState):
    ice_cream_name = state.intent_arguments.get('ice_cream_name', '')
    state.response = product_query_tool(ice_cream_name, state.intent_arguments.get('question', ''))

    return state

def handle_unrelated_questions(state: ChatState):
    state.response = "I’m here to help with questions about Icyco only — let me know if there’s something specific you’re curious about Icyco 🧁."
    return state

def handle_response(state: ChatState):
    print(f"Assistant: {state.response}")
    return state

def end(state: ChatState):
    return state

