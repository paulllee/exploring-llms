from pathlib import Path

import dotenv
import pypdf
from langchain import chains, embeddings, memory, text_splitter
from langchain.vectorstores import faiss
from langchain.llms import openai


def extract_pdf_text(pdf_path: Path) -> str:
    """
    extracts text from a given pdf path
    """
    pdf_pages: list[str] = []
    pdf_reader: pypdf.PdfReader = pypdf.PdfReader(pdf_path)
    for page in pdf_reader.pages:
        pdf_pages.append(page.extract_text())
    return "\n".join(pdf_pages)


def split_text_chunks(text: str) -> list[str]:
    """
    splits a string of text into smaller chunks
    """
    splitter: text_splitter.CharacterTextSplitter = text_splitter.CharacterTextSplitter(
        separator="\n",
        chunk_size=2000,  # default is 4000
        chunk_overlap=100  # default is 200
        # chunk_overlap is to prevent data loss between chunks
    )
    return splitter.split_text(text)


def get_faiss(texts: list[str]) -> faiss.FAISS:
    """
    gets vector store from a list of strings using faiss

    faiss -> Facebook AI Similarity Search
    """
    return faiss.FAISS.from_texts(texts=texts, embedding=embeddings.OpenAIEmbeddings())


def get_conversation_chain(
    vectorstore: faiss.FAISS,
) -> chains.ConversationalRetrievalChain:
    """
    gets the persistent conversational chain from user inputs in chat
    """
    openai_llm: openai.OpenAIChat = openai.OpenAIChat()

    conversation_memory: memory.ConversationBufferMemory = (
        memory.ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    )

    conversation_chain: chains.ConversationalRetrievalChain = (
        chains.ConversationalRetrievalChain(
            llm=openai_llm,
            retriever=vectorstore.as_retriever(),
            memory=conversation_memory,
        )
    )
    return conversation_chain


# loads .env into your environment
dotenv.load_dotenv()

human_text: str = "what is langchain?"

paul_path: Path = Path(__file__).parent
basics_401k_pdf_path: Path = paul_path / "basics_401k.pdf"

# OpenAI example
# openai_llm: OpenAI = OpenAI()
# print(openai_llm(text))
