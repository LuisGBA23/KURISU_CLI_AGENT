from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from colorama import Fore, Style
import Utilities, Chats_history, Functions

load_dotenv()
API_LIST= os.getenv("GEMINI_KEYS").split(',')
if not API_LIST: 
    raise ValueError("missing env vars")
REGISTRY= [Functions.command_exec, Functions.work_with_files]

def cargar_conf(): 
    kurisu_config= Utilities.open_file("/home/luisgba23/Personal/Documentos/KURISU_CLI_AGENT/configs/Kurisu_config.json", do= 'read_json')
    system_instruction= Utilities.open_file("/home/luisgba23/Personal/Documentos/KURISU_CLI_AGENT/configs/system_instruction.md")
    config_mod= types.GenerateContentConfig(
        tools= REGISTRY,
        system_instruction= system_instruction,
        temperature= kurisu_config['temperature'],
        top_p= kurisu_config['top_p']
    )

    return kurisu_config, config_mod

while True:
    try:
        chose_api= Utilities.elegir_api(API_LIST)
        kurisu_config, config_mod= cargar_conf()
        hist= Chats_history.cargar_historial("/home/luisgba23/Personal/Documentos/KURISU_CLI_AGENT/configs/historial.pkl")
        client= genai.Client(api_key= chose_api)
        chat= client.chats.create( 
            model= kurisu_config['model_name'],
            history= hist,
            config= config_mod
        )

        inp= input(Fore.CYAN + "(Christina) >> " + Fore.RESET)
        if inp.lower() == "close": 
            print(Fore.RESET)
            break

        for chunk in chat.send_message_stream(inp): 
            for part in chunk.candidates[0].content.parts: 
                if part.thought: continue
                else: print(Style.BRIGHT + f"{part.text}", end= '', flush= True)
        #resp= chat.send_message(inp)
        #print(Style.BRIGHT + f"{resp.text}\n")
        print(Style.RESET_ALL)

        historial_act= chat.get_history()
        hist= historial_act
        Chats_history.guardar_historial(
            "/home/luisgba23/Personal/Documentos/KURISU_CLI_AGENT/configs/historial.pkl",
            chat_list= hist
        )

        client.close()
    except genai.errors.ServerError as e:
        disp_model= ( 
            "models/gemini-3.5-flash"
            if kurisu_config['model_name'] == "models/gemini-2.5-flash" 
            else "models/gemini-2.5-flash"
        )

        Utilities.set_attribute(
            'model_name', 
            disp_model, 
            conf_file= "/home/luisgba23/Personal/Documentos/KURISU_CLI_AGENT/configs/Kurisu_config.json"
        )
        kurisu_config, config_mod= cargar_conf()
