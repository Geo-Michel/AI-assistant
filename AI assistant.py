from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import speech_recognition as sr
import time
import json

#This method saves the logs (conversation) as a json file
def save_context(context):
    with open('context.json', 'w') as f:
        json.dump(context, f ,indent=4)

#This method loads the context that is saved on the .json file if any
def load_context():
    try:
        with open('context.json','r') as f:
            data=json.load(f)
            return data
    except(FileNotFoundError, ValueError):
        print("There is no saved context")
        return []

#This method handles the speech recognition and returns a string with the user's prompt
r=sr.Recognizer()
r.pause_threshold=2
def audio_input(ask=False):
    if ask:
        print(ask)
    with sr.Microphone() as source:
        voice_data=''
        while voice_data=="":
            try:
                print("You: ")
                time.sleep(2)
                audio= r.listen(source)                 #If the mic can't capture audio or the mic is not working the code will get stuck here 
                voice_data=r.recognize_google(audio)
                print(voice_data)
            except sr.UnknownValueError:
                print('Sorry, I did not understand that. Can you repeat?')
                time.sleep(3)
            except sr.RequestError:
                print('Sorry my service is down.')
                break
        return voice_data
            
#context (e.g. "You are an expirienced programmer that helps me develop apps")should be written on line 44 
template= """

Here is the conversation history: {context}

Prompt: {question}

Answer:
"""
model=OllamaLLM(model="deepseek-r1")    #Insert the name of the Ollama model you have installed in your device
prompt=ChatPromptTemplate.from_template(template)      #Create a prompt template (structure for combining conversation history and user input)
chain=prompt | model                    # Build the chain: feed the prompt into the model to get responses

def conversation(call_audio_input):
    context=load_context()      #Loading the context saved in the .json file
    while True:
        if (call_audio_input):
            user_prompt=audio_input()
        else:
            user_prompt=input("You: ")
#If the prompt is exit or shut down the chat is terminated and the user chooses whether or not to save the conversation as context for the model
        if (user_prompt.lower()=="shut down" or user_prompt.lower()=="exit"):
            save=input("Do you wish to save the conversation?\n")
            if(save.lower()=="yes"):
                save_context(context)
            else:
                while True:
                    save2=input("Are you sure?\n")
                    if (save2.lower()=="no"):
                        save_context(context)
                    elif(save2.lower()=="yes"):
                        break
                    
            break
        responce= chain.invoke({"context": context, "question":user_prompt})
        print("Assistant:\n", responce)
        print("---------------------------------------------------------------------------------------------------------------------------------")
        context.append({"role":"User","content":user_prompt })
        context.append({"role":"Assistant","content":responce })



if __name__=="__main__":
    voice_chat=" "
    while (voice_chat!="yes" and voice_chat!="no"):
        voice_chat=input("Do you want to use voice chat? (yes/no)\n")
    if (voice_chat=="yes"):
        call_audio_input=True
    else:
        call_audio_input=False
    conversation(call_audio_input)