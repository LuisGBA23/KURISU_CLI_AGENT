import re
from pynput import keyboard

buffer_teclas= []
PREFIXS= ("makise", "kurisu", "christina")

def on_press(key): 
    global buffer_teclas, PREFIXS

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
                    buffer_teclas.clear()
                else: 
                    pass

        elif key == keyboard.Key.backspace: 
            if buffer_teclas: 
                buffer_teclas.pop()

with keyboard.Listener(on_press= on_press) as listener: 
    listener.join()