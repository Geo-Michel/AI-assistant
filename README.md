Voice + Text Chat with Ollama and LangChain

This project is a simple chat interface that lets you talk to an Ollama model (e.g. deepseek-r1) either by typing text or by using your microphone.
The conversation history is stored in a JSON file (context.json), so the assistant can remember past interactions. 

Features:

Voice input via microphone (using speech_recognition)

Text input via terminal

Conversation history saved as a JSON file (context.json)

Context is loaded at startup so the model can keep track of previous chats

Say "exit" or "shut down" to end the session (with the option to save or discard context)

Make sure you have installed the following Python packages:

langchain-ollama

langchain-core

SpeechRecognition, *for speech recognition

PyAudio, *for speech recognition

Also ensure:

You have Ollama installed on your system and at least one model pulled (e.g. ollama pull deepseek-r1).

You have a working microphone if you want to use voice chat.
