import dotenv
from langchain.llms.openai import OpenAI

# loads .env into your environment
dotenv.load_dotenv()

text: str = "what is langchain?"

# OpenAI example
openai_llm: OpenAI = OpenAI(temperature=0.9)
print(openai_llm(text))
