from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

prompt = ChatPromptTemplate.from_template("Tell me a fun fact about {topic} in one simple sentence.")

model = ChatOpenAI(model="gpt-4o-mini")

chain = prompt | model | StrOutputParser()

topic = "space exploration"

print("Input:", prompt.format(topic=topic))

print("Output:", chain.invoke({"topic": topic}))