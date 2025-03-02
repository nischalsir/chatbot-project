from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Allow frontend origin
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Load GPT-2 model and tokenizer
model_name = "gpt2"  # You can also use "EleutherAI/gpt-neo-125M" for GPT-Neo 125M
generator = pipeline("text-generation", model=model_name)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Chatbot API! Use the /chat endpoint to interact with the chatbot."}

class ChatRequest(BaseModel):
    message: str  # Only the message field is needed

# Chat endpoint
@app.post("/chat")
async def chat(request: ChatRequest):
    # Create a prompt for the model
    prompt = request.message  # Use the user's message directly
    
    # Generate a response
    response = generator(prompt, max_length=100, do_sample=True, temperature=0.7)[0]['generated_text']
    
    # Return the response
    return {"response": response}