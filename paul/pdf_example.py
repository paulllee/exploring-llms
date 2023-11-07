from pathlib import Path
from typing import Any, Union

import dotenv
import pypdf
import streamlit as st

from langchain import chains, embeddings, memory, text_splitter
from langchain.llms import openai
from langchain.vectorstores import faiss

import chat_html


def extract_pdf_text(pdf_path: Union[Path, Any]) -> str:
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
    faiss_vectorestore: faiss.FAISS,
) -> chains.ConversationalRetrievalChain:
    """
    gets the LOCALLY persistent conversational chain from user inputs in chat
    """
    llm: openai.OpenAI = openai.OpenAI()

    # creates a locally persistent storage of the chat history
    # also storing in session_state for clearing later
    st.session_state.conversation_memory: memory.ConversationBufferMemory = (
        memory.ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    )

    conversation_chain: chains.ConversationalRetrievalChain = (
        chains.ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=faiss_vectorestore.as_retriever(),
            memory=st.session_state.conversation_memory,
        )
    )
    return conversation_chain


def handle_user_input(current_user_input: str) -> None:
    """
    handles a given user input by grabbing the response via coversation_chain and displaying
    """
    bot_response: str = st.session_state.conversation_chain(
        {
            "chat_history": st.session_state.chat_history,
            "question": current_user_input,
        }
    )
    st.session_state.chat_history = bot_response["chat_history"]

    # rewrite the chat history every new user input
    is_user: bool = True
    for message in st.session_state.chat_history:
        if is_user:
            st.write(
                chat_html.USER_TEMPLATE.replace("{{MSG}}", message.content),
                unsafe_allow_html=True,
            )
        else:
            st.write(
                chat_html.BOT_TEMPLATE.replace("{{MSG}}", message.content),
                unsafe_allow_html=True,
            )

        # flips the boolean
        is_user: bool = not is_user


if __name__ == "__main__":
    # loads .env into your environment
    dotenv.load_dotenv()

    # styling
    st.write(chat_html.CHAT_CSS, unsafe_allow_html=True)

    # setting default values if not already set
    if "conversation_memory" not in st.session_state:
        st.session_state.conversation_memory = None
    if "conversation_chain" not in st.session_state:
        st.session_state.conversation_chain = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # main chat portion
    st.header("PDF Chat")
    user_input: str = st.text_input(
        "ask a question with your PDF context:",
        key="user_input_widget",
    )
    if user_input:
        handle_user_input(user_input)

    # allow for easy clearing
    if st.button("clear history"):
        with st.spinner("clearing"):
            st.session_state.chat_history = None
            if st.session_state.conversation_memory is not None:
                st.session_state.conversation_memory.clear()

    # processing
    with st.sidebar:
        st.subheader("Current PDF Selection")
        pdf: Any = st.file_uploader(
            label="upload ONLY ONE pdf", accept_multiple_files=False
        )
        if st.button("process"):
            with st.spinner("processing"):
                pdf_text: str = extract_pdf_text(pdf)
                text_chunks: list[str] = split_text_chunks(pdf_text)
                new_faiss_vectorestore: faiss.FAISS = get_faiss(text_chunks)

                # setting conversation_chain to the session state for access later
                st.session_state.conversation_chain = get_conversation_chain(
                    new_faiss_vectorestore
                )
