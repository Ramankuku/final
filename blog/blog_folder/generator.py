from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.chains import LLMChain
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")




def generate_blog(topic):
    '''
    Generate a blog post based on the topic provided using the model
    '''
    template_prompt = '''Write a detailed blog on this topic {topic}
    You are a professional blog writter
    Structure the blog with:
    - Include catchy words
    - Informative and detailed content based on the given topic
    - Include a conclusion at the end of the blog post
    Keep the blog post engaging and informative
    '''
    template = PromptTemplate(input_variables=['topic'],
                              template=template_prompt)
    
    llm_model = ChatOpenAI(model='gpt-4', openai_api_key=OPENAI_API_KEY)
    llm_chain = LLMChain(llm=llm_model, prompt =template)
    return llm_chain.run(topic=topic)
    


# if __name__ == "__main__":
#     generate_blog("How AI is Transforming Small Businesses")