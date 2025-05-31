# LiteLLM Chatbot with OpenRouter

An intelligent chatbot built with Chainlit and LiteLLM that features streaming responses and conversation history management. The chatbot uses Google's Palm-2 model via OpenRouter.

## Features

- Browser-based user interface built with Chainlit
- Real-time streaming of AI responses
- Conversation memory throughout the session
- Automatic saving of complete chat history to JSON file

```bash
chainlit run src/chatbotlitellm/chatbot.py
```

## Chat History

At the end of each session, the complete chat history is automatically saved to `chat_history.json` in the current directory. This JSON file contains all user messages and AI responses with timestamps.

## Requirements

- Python 3.11+
- Chainlit
- LiteLLM
- python-dotenv
- rich

## Screenshot
![Chatbot using litellm Browser Screenshot](LITELLM.png)" 
"# CHATBOT_LITELLM" 
