# Plug in API key and LLM configuration and run file to test API connection. 
# Then you can run the code to ask questions and get responses from the LLM.
# Type 'exit' to exit out of conversation.

# Generate API key from - https://platform.openai.com/account/api-keys 
#     --> Set openai.openai_key

# IMPORTANT --- DO NOT UPLOAD YOUR API KEY TO GITHUB IF YOU ARE USING A PAID LLM API KEY (ex: ChatGPT). ---

import openai

# Your OpenAI API key
openai.api_key = "YOUR_API_KEY"

def ask_chatgpt(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=1,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        if response:
            return response.choices[0].message['content'].strip()
        else:
            print("Error: No response from API")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    while True:
        user_message = input("You: ")
        if user_message.lower() in ["exit"]:
            print(" ---- Exited ---- ")
            break
        response = ask_chatgpt(user_message)
        if response:
            print("ChatGPT:", response)

