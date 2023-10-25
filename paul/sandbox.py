import dotenv
from langchain.llms.openai import OpenAI
from langchain.llms.huggingface_hub import HuggingFaceHub

# loads .env into your environment
dotenv.load_dotenv()

text: str = "what is langchain?"

# OpenAI example
openai_llm: OpenAI = OpenAI(temperature=0.9)
print(openai_llm(text))

# HuggingFace example
huggingface_llm: HuggingFaceHub = HuggingFaceHub(
    repo_id="google/flan-t5-xl",
    model_kwargs={"temperature": 0.75}
)
print(huggingface_llm(text))
