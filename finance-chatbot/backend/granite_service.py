
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_API_KEY")  
MODEL_ID = "ibm-granite/granite-3.3-8b-base"

client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)

def ask_granite(prompt: str) -> str:
    try:
        response = client.text_generation(
            prompt,
            max_new_tokens=150,
            do_sample=True,
            temperature=0.7
        )

       
        if isinstance(response, str):
            return response
        elif isinstance(response, list) and "generated_text" in response[0]:
            return response[0]["generated_text"]
        elif isinstance(response, dict) and "generated_text" in response:
            return response["generated_text"]
        else:
            return str(response)

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
