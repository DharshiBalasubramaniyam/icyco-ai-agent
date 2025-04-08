import json
import os

from langchain_google_genai import GoogleGenerativeAI
from utils import createRagChain, get_vector_store, getLLM

from langchain_core.prompts import PromptTemplate

qa_vector_store = get_vector_store(os.getenv("QA_INDEX_NAME"))       
qa_client = GoogleGenerativeAI(model="gemini-2.0-flash", api_key=os.getenv("GOOGLE_API_KEY"))      

def question_answer_tool(question):
   prompt = PromptTemplate(
      template="""
            You are a helpful, friendly, and engaging AI assistant for **Icyco**, an ice cream shop. 
            Your job is to answer user questions related to Icyco’s products, services, events, or company info in a way that is both informative and delightful.

            Use the following retrieved documents to provide an accurate and engaging response.

            - If the user’s question is **not related to Icyco**, politely respond with:  
              *"I’m here to help with questions about Icyco only — let me know if there’s something specific you’re curious about!"*

            - If the user’s question **is related to Icyco** but you **cannot find the answer** in the provided documents, say:  
              *"That’s a great question about Icyco, but I couldn’t find the answer in the info I have. You might want to reach out to Icyco directly for the most up-to-date details!"*

            Your tone should be:
            - Friendly and conversational 🧁  
            - Engaging and easy to understand  
            - Accurate — don’t make up any information

            If it fits naturally, feel free to show enthusiasm, add a touch of personality, or relate to the excitement around ice cream!

            ---  
            Context:  
            {context}

            question: {question}
         """,
      input_variables=["context", "question"],
   )
   try:
     rag_chain = createRagChain(qa_client, qa_vector_store, prompt)  
     response = rag_chain.invoke({"query": question})  
     return response["result"] if response else "Oops! Something went wrong while processing your request."
   except Exception as e:
     print(f"Error: {e}")
     return "Sorry, I couldn't process your query. Please try again after some time!"


def product_filter_tool(keywords, start_price, end_price, start_rating, end_rating):
   with open('resources/products.json', 'r') as file:
        data = json.load(file)
   products_by_keyword = []
   for product in data['products']:
        if keywords and any(
            keyword.lower() in product['name'].lower() or
            keyword.lower() in product['description'].lower() or
            keyword.lower() in [ing.lower() for ing in product['ingredients']]
            for keyword in keywords
        ):
            products_by_keyword.append(product)

   filtered_products = products_by_keyword

   if start_price != -1:
        filtered_products = [product for product in filtered_products if product['price'] >= start_price]
   if end_price != -1:
        filtered_products = [product for product in filtered_products if product['price'] <= end_price]
   if start_rating != -1:
        filtered_products = [product for product in filtered_products if product['rating'] >= start_rating]
   if end_rating != -1:
        filtered_products = [product for product in filtered_products if product['rating'] <= end_rating]
   return filtered_products[:5] if len(filtered_products) > 5 else filtered_products

def product_query_tool(ice_cream_name, query):
   with open('resources/products.json', 'r') as file:
        data = json.load(file)

   keywords = ice_cream_name.split(",")
   products_by_keyword = [product for product in data['products'] if any(keyword.lower() in product['name'].lower() for keyword in keywords)]

   if not products_by_keyword:
        return f"Sorry, I couldn't find any information about {ice_cream_name}. Please check the name and try again!"

   prompt_template = f"""
            You are a helpful, friendly, and engaging AI assistant for **Icyco**, an ice cream shop. 
            Your job is to answer user question related to one of the icyco products using the provided context.

            - If you **cannot find the details of the product in the question from the context** , say:  
                **"Sorry, I couldn't find any information about {ice_cream_name}.** in friendly an dengaing manner
            - If you find more than one product related to question, answer the question for top 5 products only.

            Your tone should be:
            - Friendly and conversational 🧁  
            - Engaging and easy to understand  
            - Accurate — don’t make up any information

            If it fits naturally, feel free to show enthusiasm, add a touch of personality, or relate to the excitement around ice cream!

            ---  
            Context:  
            {products_by_keyword}

            question: {query}
        """
   try:
     llm = getLLM()
     response = llm.invoke(prompt_template)
     return response
   except Exception as e:
            print(f"Error: {e}")
            return "Sorry, I couldn't find any information about the product. Please try again after some time!"