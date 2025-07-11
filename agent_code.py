import os
from langchain_community.document_loaders import PyPDFLoader,DirectoryLoader
from langchain.text_splitter import TextSplitter,RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.tools import tool
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from sympy import sympify
from langchain.memory import ConversationBufferMemory
import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
import requests


# load_dotenv()
API_KEY = "API_KEY"
llm = ChatOpenAI(model="gpt-4o-mini", api_key=API_KEY)
embedding = OpenAIEmbeddings(model="text-embedding-3-small")
pdf_dir = 'Data/data.pdf'
searching = DuckDuckGoSearchRun()

memory = ConversationBufferMemory(
    memory_key = 'chat_history',
    return_messages = True
)


def pdf_data(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents

def chunk_data(data):
    splitter = RecursiveCharacterTextSplitter(chunk_size=170, chunk_overlap=25)
    chunks = splitter.split_documents(data)
    return chunks

def index_pdf(file_path):
    data = pdf_data(file_path)
    chunks = chunk_data(data)
    vectorstore = FAISS.from_documents(chunks, embedding)
    vectorstore.save_local("faiss.index")

@tool
def query_pdf_tool(question: str) -> str:
    """Query information from the uploaded PDF"""
    try:
        vectorstore = FAISS.load_local("faiss.index", embedding)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
        return qa_chain.run(question)
    except Exception as e:
        return f"Error: {str(e)}"




@tool 
def get_weather(city: str, key_words='full') -> str:
    """Get the weather of a city based on a keyword (temperature, description, or coordinates)."""
    try:
        url = f'http://api.weatherstack.com/current?access_key=a785803b9b20610c149bd8ac90b50ba9&query={city}'
        data = requests.get(url)
        response = data.json()

        location = response['location']['name']
        temperature = response['current']['temperature']
        weather_descriptions = ', '.join(response['current']['weather_descriptions'])
        latitude = response['location']['lat']
        longitude = response['location']['lon']

        if key_words == 'temperature':
            return f'The temperature of {location} is {temperature}°C.'
        elif key_words == 'weather_descriptions':
            return f'The weather in {location} is {weather_descriptions}.'
        elif key_words in ['coordinates', 'latitude', 'longitude']:
            return f'The latitude and longitude of {location} are {latitude} and {longitude}.'
        else:
            return (
                f'The weather in {location} is {weather_descriptions} with a temperature of {temperature}°C. '
                f'Latitude: {latitude}, Longitude: {longitude}.'
            )

    except Exception as e:
        return f'Failed to get the weather of {city}. Please try again later. Error: {str(e)}'

@tool
def web_search(query:str)->str:
    """Search the web for a query and return the first result."""
    search = searching.invoke(query)
    return search


@tool
def generate_blog(topic: str) -> str:
    """Generate a blog post on a given topic using GPT-4."""
    blog_llm = ChatOpenAI(model="gpt-4", api_key=API_KEY)
    
    prompt = f"Write a detailed, catchy-words, engaging, and well-structured blog post about: {topic}"
    
    return blog_llm.invoke(prompt)

@tool
def calculation_exp(expression: str)->str:
    """Evaluate a mathematical expression like '2+3+4*7', 'sqrt(16)', 'sqrt(18.9)', 'cos(90)', cos(-180) and more arithmetic operation and return the result."""
    try:
        expression = expression.replace("sin(", "sin(pi/180*")
        expression = expression.replace("cos(", "cos(pi/180*")
        expression = expression.replace("tanh(", "tanh(pi/180*")
        result = sympify(expression).evalf()
        return float(result)
    except Exception as e:
        return f'Not able to give answer. Please provide quite simple problems'



search_tools = [query_pdf_tool,web_search, get_weather, calculation_exp, generate_blog]

prompt = PromptTemplate.from_template("""
You are an AI agent that can use the following tools:
{tools}

Here is the conversation so far:
{chat_history}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original question

IMPORTANT:
- Do not write "Action: None required".
- If you do not need to use a tool, directly proceed to "Final Answer".

Begin!

Question: {input}
{agent_scratchpad}
""")




agent = create_react_agent(
    llm = llm,
    prompt = prompt,
    tools=search_tools
)

agent_executor = AgentExecutor(
    agent=agent,
    memory=memory,
    tools=search_tools,
    verbose=True,
    handle_parsing_errors=True
)

def main_agent_call(question: str)->str:
    response = agent_executor.invoke({"input": question})
    print("\n--- Memory Content ---")
    for msg in memory.chat_memory.messages:
        print(f"{msg.type.upper()}: {msg.content}")
    print("----------------------\n")
    # return response['output']
    return response.get('output', "No answer returned by agent.")

