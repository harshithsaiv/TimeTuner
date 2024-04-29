# chatgpt_interface.py
import openai
import os
from dotenv import load_dotenv

# Ensure your .env file has the OPENAI_API_KEY variable defined
load_dotenv()

def chat_with_chatgpt(document_content):
    """Interacts with ChatGPT using the provided document content as context."""
    # Set API key from environment variable
    openai.api_key = os.getenv('OPENAI_API_KEY')

    print("You can now ask questions related to the office hours document. Type 'quit' to exit.")
    session_prompt = f"The following content is extracted from the office hours document:\n{document_content}\n\n###\n\n"
    
    while True:
        user_input = input("Ask a question: ")
        if user_input.lower() == 'quit':
            break
        try:
            # Using the 'create' method from 'openai.Completion' with the updated parameters
            response = openai.completions.create(
                model="gpt-3.5-turbo",  # Ensure you use an available model; adjust as necessary
                prompt=session_prompt + user_input,
                max_tokens=150,
                stop=None  # Adjust stopping conditions based on your requirements
            )
            print("AI:", response.choices[0].text.strip())
        except Exception as e:
            print(f"An error occurred: {e}")
