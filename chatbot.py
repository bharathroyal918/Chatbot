from gradio import ChatInterface
import gradio as gr
from groq import Groq
from google.colab import userdata

def generate_chat_response(message, history):
    api_key = userdata.get('GROQ_API_KEY')
    client = Groq(api_key=api_key)
    if not client:
        print('''Error: Groq client is not initialized. 
        please check your API key ''')
        return

    history_groq_format = []
    for user_msg, bot_msg in history:
        history_groq_format.append({"role": "user", "content": user_msg})
        history_groq_format.append({"role": "assistant", "content": bot_msg})  # Changed role to assistant here
    
    history_groq_format.append({"role": "user", "content": message})

    try:
        stream = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=history_groq_format,
            temperature=0.6,
            max_tokens=4096,
            top_p=0.95,
            stream=True,
            stop=None,
        )
        partial_response = ""
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content is not None:
                partial_response += content
                yield partial_response  # fixed typo 'yiels_partial_response' to 'yield partial_response'
    except groq.APIError as e:
        print(f"An API error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

chatbot_ui = gr.ChatInterface(
    fn=generate_chat_response,
    title="Hello",
    description="Hello this is workshop",
    examples=[
        "hello this",
        "is the workshop",
    ],
    theme="soft",
)

if __name__ == "__main__":
    chatbot_ui.launch(server_name="0.0.0.0",debug=True)
