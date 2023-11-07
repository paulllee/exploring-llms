
#pip3 install -q grobid-client langchain openai faiss-cpu PyPDF2 tiktoken (setup)

import os
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS

wget https://github.com/kairess/toy-datasets/ramaster/Demian.pdf

# Preprocess a PDF file
reader = PdfReader("samplePDF")
raw_text = ""

for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        raw_text += text

# Summarize
from langchain import llama2  # Hypothetical import
from langchain.chains import AnalyzeDocumentChain
from langchain.chains.summarize import load_summarize_chain

llm = llama2(temperature=0)  # Hypothetical instantiation
summary_chain = load_summarize_chain(llm, chain_type="map_reduce")

summarize_document_chain = AnalyzeDocumentChain(combine_docs_chain=summary_chain)
summarize_document_chain.run(raw_text)

# Question Answering
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatLlama2  # Hypothetical import

model = ChatLlama2(model="llama2-turbo")  # Hypothetical model string
qa_chain = load_qa_chain(model, chain_type="map_reduce")
qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)

qa_document_chain.run(input_document=raw_text, question="sample Q1?")
qa_document_chain.run(input_document=raw_text, question="sample Q2?")
qa_document_chain.run(input_document=raw_text, question="sample Q3")

# For another hypothetical llama2 model variant
model = ChatLlama2(model="llama2-nextgen")  # Adjust as needed
qa_chain = load_qa_chain(model, chain_type="map_reduce")
qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)
qa_document_chain.run(input_document=raw_text, question="sample Q4")

# excel, search cvs, Aggregation
import pandas as pd
df = pd.read_csv("https://github.com/kairess/toy-datasets/raw/master/titanic.csv")
from langchain.agents import create_pandas_dataframe_agent
agent = create_pandas_dataframe_agent(llama2(temperature=0), df, verbose=True)  # Hypothetical instantiation
agent.run("how many rows are there?")
agent.run("a")
agent.run("b")
agent.run("c")
agent.run("d")
