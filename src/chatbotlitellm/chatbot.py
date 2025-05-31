import os
import json
import chainlit as cl
from litellm import completion
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API configuration for OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
# Set environment variable for OpenRouter
os.environ["OPENROUTER_API_KEY"] = OPENROUTER_API_KEY

# Model configuration - using a simpler OpenAI-compatible model via OpenRouter
MODEL = os.getenv("MODEL", "openrouter/anthropic/claude-3-haiku")

# Chat history storage
chat_history = []

class Message:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content
    
    def to_dict(self) -> Dict:
        return {
            "role": self.role,
            "content": self.content
        }

def save_chat_history():
    """Save the chat history to a JSON file."""
    if not chat_history:
        return
    
    history_data = [msg.to_dict() for msg in chat_history]
    
    with open("chat_history.json", "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=2, ensure_ascii=False)
    
    print(f"Chat history saved to chat_history.json")

@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session."""
    global chat_history
    chat_history = []
    
    # Check API key
    if not OPENROUTER_API_KEY:
        print("\n⚠️ Warning: OPENROUTER_API_KEY is not set. The chatbot may not function correctly.")
        print("Please set the OPENROUTER_API_KEY in your .env file.")
    
    # Send an initial message
    await cl.Message(
        content="👋 Welcome! I'm your assistant via OpenRouter. How can I help you today?",
        author="Assistant"
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    """Handle incoming user messages."""
    # Add user message to history
    chat_history.append(Message(
        role="user",
        content=message.content
    ))
    
    # Prepare message history for LLM in the format it expects
    messages = [
        {"role": msg.role, "content": msg.content}
        for msg in chat_history
    ]
    
    # Create and send a thinking message
    thinking_msg = cl.Message(content="", author="Assistant")
    await thinking_msg.send()
    
    try:
        # Get response from LiteLLM
        full_response = ""
        
        # Start the completion with streaming
        response = completion(
            model=MODEL,
            messages=messages,
            stream=True,
        )
        
        # Process each chunk in the stream
        for chunk in response:
            if hasattr(chunk, 'choices') and chunk.choices:
                content = chunk.choices[0].delta.content
                if content:
                    full_response += content
                    # Update the message content
                    thinking_msg.content = full_response
                    await thinking_msg.update()
        
        # Add assistant response to history
        chat_history.append(Message(
            role="assistant",
            content=full_response
        ))
        
    except Exception as e:
        error_message = f"Error: {str(e)}"
        thinking_msg.content = error_message
        await thinking_msg.update()
        print(f"Error generating response: {str(e)}")

@cl.on_chat_end
async def on_chat_end():
    """Handle chat session end."""
    save_chat_history()
    print("Chat session ended. History saved to chat_history.json")

if __name__ == "__main__":
    cl.run()
