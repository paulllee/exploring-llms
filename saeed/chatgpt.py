# Plug in API key and LLM configuration and run file to test API connection. 
# Then you can run the code to ask questions and get responses from the LLM.
# Type 'exit' to exit out of conversation.

# Generate API key from - https://platform.openai.com/account/api-keys 
#     --> Set openai.openai_key

# IMPORTANT --- DO NOT UPLOAD YOUR API KEY TO GITHUB IF YOU ARE USING A PAID LLM API KEY (ex: ChatGPT). ---

import openai
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv

# Your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)  # Updated class name here
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"An error occurred while extracting text from PDF: {e}")
        return None

def ask_chatgpt(question, context=None):
    try:
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": question
            }
        ]
        
        if context:
            messages.insert(0, {
                "role": "system",
                "content": context
            })

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=1,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        if response:
            return response.choices[0].message['content'].strip()
        else:
            print("Error: No response from the API")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

    
if __name__ == "__main__":
    # Ask for the path to the PDF
    pdf_path = input("Do you want to provide a PDF? Please provide the full path to the PDF (Type 'no' to ignore): ")
    
    # Check if the file exists
    if pdf_path.lower() != "no":
        if os.path.exists(pdf_path) and pdf_path.lower().endswith('.pdf'):
            # Extract text from PDF
            context = extract_text_from_pdf(pdf_path)
            print(context)
            # Check if extraction was successful
            if context:
                while True:
                    user_message = input("You: ")
                    if user_message.lower() in ["exit"]:
                        print(" ---- Exited ---- ")
                        break
                    
                    # Ask a question, providing the PDF text as context
                    response = ask_chatgpt(user_message, context)
                    
                    if response:
                        print("ChatGPT:", response)
            else:
                print("Could not extract text from the PDF.")
    else:
        print("No PDF provided")
        while True:
                user_message = input("You: ")
                if user_message.lower() in ["exit"]:
                    print(" ---- Exited ---- ")
                    break
                
                response = ask_chatgpt(user_message)
                
                if response:
                    print("ChatGPT:", response)