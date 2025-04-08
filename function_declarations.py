f_question_answer = {
    "name": "question_answer",
    "description": "Answer the questions related to 'Icyco' privacy policy, terms and conditions, FAQs. Icyco is an ice cream shop.",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question asked by the user.",
            },
        },
        "required": ["question"],
    },
}

f_filter_products = {
    "name": "filter_products",
    "description": "Recommend ice creams from database based on metadata, for 'Icyco' customers. Icyco is an ice cream shop.",
    "parameters": {
        "type": "object",
        "properties": {
            "keywords": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of keywords extracted from user query to recommend products. Keyword is a one word, which can be anything which describe ice cream. E.g., ingredients, flavors, icecream types, etc.",
            },
            "start_price": {
                "type": "integer",
                "description": "Starting price of the range. Value is -1, if user wants to extract products less than a price"
            },
            "end_price": {
                "type": "integer",
                "description": "Ending price of the range. Value is -1, if user wants to extract products greater than a price"
            },
            "start_rating": {
                "type": "integer",
                "description": "Start rating of the range. Value is -1, if user wants to extract products less than a rating"
            },
            "end_rating": {
                "type": "integer",
                "description": "End rating of the range. Value is -1, if user wants to extract products greater than a rating"
            }
        },
        "required": ["keywords", "start_price", "end_price", "start_rating", "end_rating"],
    },
}

f_product_query = {
    "name": "product_query",
    "description": "Extracts information about a specific ice cream from the database, i.e., ingredients, flavors, price etc. Icyco is an ice cream shop.",
    "parameters": {
        "type": "object",
        "properties": {
            "ice_cream_name": {
                "type": "string",
                "description": "The name of the ice cream user is interested in.",
            },
            "question": {
                "type": "string",
                "description": "The question asked by the user.",
            }
        },
        "required": ["ice_cream_name", "question"],
    },
}

f_handle_unrelated_questions = {
    "name": "handle_unrelated_questions",
    "description": "Handles user queries which are unrelated to 'Icyco'. Icyco is an ice cream shop.",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question asked by the user.",
            },
        },
        "required": ["question"],
    },
}
