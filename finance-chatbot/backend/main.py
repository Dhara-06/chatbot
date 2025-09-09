
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from granite_service import ask_granite  

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Personal Finance Chatbot Backend Running"}

import traceback

@app.post("/generate")
async def generate_handler(request: Request):
    data = await request.json()
    user_input = data.get("text", "")

    try:
        output_text = ask_granite(user_input)
        return {"response": output_text}
    except Exception as e:
        print("DEBUG ERROR:", traceback.format_exc()) 
        return {"error": str(e)}


