import speech_recognition as sr 

def start_voice() -> str: 
    r= sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration= 1.5)
        audio= r.listen(source, )

        what_you_said= r.recognize_google(audio, language= "es-ES")

    return what_you_said