# 🧠 AI Assistant for Icyco, an ice cream shop

![image](https://github.com/user-attachments/assets/9b7dc3c1-0502-430e-8d70-b9df01675a70)

This project implements an AI assistant powered by a multi-tool orchestration agent using [LangGraph](https://github.com/langchain-ai/langgraph). 
It is designed to intelligently detect user intent, route requests to appropriate tools, and return relevant, structured responses.

## Overview

The assistant functions as an **intent-aware, tool-using agent** capable of:

- Answering general questions using a **LangChain RAG pipeline**.
- Recommending products based on user preferences from JSON dataset (simulating a database).
- Fetching information related to specific product from JSON dataset (simulating a database).
- Handling questions which are not related to icyco.
- Gracefully falling back when no tool is available.

## Technologies

| Component | Technology |
| --------- | ---------- |
| Agent Framework	| LangGraph | 
| LLM	Google | Gemini via Google Generative AI | 
| Embeddings	| FastEmbed (for RAG system) | 
| Vector Store	| Pinecone | 
| Question Answering	| LangChain RAG chain | 
| Product Data Source	| JSON file (simulating a database) | 
| Intent Detection	| Google GenAI + Function Calling | 
| Routing Logic	| LangGraph conditional edges | 

## Nodes & Logic

### 🧩 Start

Entry point of the graph

### 🧩 Intent Detection Node

Determines user intent using function calling and tool description context. Returns the appropriate tool name and its arguments. Logic:

Input: `query`, `available tools`
Output: `tool_name`, `arguments`

Uses Gemini + function calling to identify the correct tool.

### 🧩 Tool Nodes

#### 1. Question answer node

Input: `query`

Calls a LangChain RAG chain:

- Embedding: FastEmbed

- Vector DB: Pinecone

- LLM: Gemini

Returns: `Answer`
   
#### 2. Product recommendation node

Input: `keywords`, `price`, `rating`

Logic: Matches conditions from a JSON file representing sample product data.

Returns: List of recommended `products`
   
#### 3. Product query node

Input: `product name`, `query`

Logic: Searches JSON file for product info, augments with LLM-based clarification

Returns: Product details  

#### 4. Third-party question node

Logic: Used for queries that don’t fit into icyco.

Returns: A message

### 🧩 End

Processes raw tool outputs into user-friendly responses. This is the final output node before exiting.











