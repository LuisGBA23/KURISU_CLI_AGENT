from google import genai
from google.genai import types
from dotenv import load_dotenv
from pynput import keyboard
import os
import re
import Utilities, Functions

load_dotenv()
API_LIST= os.getenv("GEMINI_KEYS").split(',')
if not API_LIST: 
    raise ValueError("missing env vars")

PREFIXS= ("makise", "kurisu", "christina")
REGISTRY= [Functions.command_exec, Functions.guardar_archivo]
buffer_teclas= []

def on_press(key): 
    global buffer_teclas, REGISTRY, API_LIST, PREFIXS

    try: 
        if key.char != None:
            buffer_teclas.append(key.char)
    except AttributeError: 
        if key == keyboard.Key.space:
            buffer_teclas.append(key)

        elif key == keyboard.Key.enter: 
            if buffer_teclas: 
                prompt= ''.join(buffer_teclas)
                low_prompt= prompt.lower()
                if low_prompt.startswith(PREFIXS):
                    clean_prompt = re.sub(r"^\s*(?:makise|kurisu|christina)\b[\s,:]*", "", low_prompt)

                    print(clean_prompt)
                else: 
                    pass

        elif key == keyboard.Key.backspace: 
            if buffer_teclas: 
                buffer_teclas.pop()


client= genai.Client(api_key= Utilities.elegir_api(API_LIST))

inp= input("Di algo: ")
response= client.models.generate_content( 
    model= "gemini-2.5-flash",
    contents= inp, 
    config= types.GenerateContentConfig(
        tools= REGISTRY,
        system_instruction= Utilities.open_file("./configs/system_instruction.md")
    ),
)

print(response.text)

with keyboard.Listener(on_press= on_press) as listener: 
    listener.join()