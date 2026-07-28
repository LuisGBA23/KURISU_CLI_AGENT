import subprocess

def guardar_archivo(archivo: str, dispositivo: str) -> dict: 
    '''Guarda un archivo en un dispositivo'''
    return {"file": archivo, "device": dispositivo}

def command_exec(comando: str) -> str: 
    '''Ejecuta un comando en la terminal del sistema (Debian)'''
    if comando.startswith("sudo"):
        print(f"Do you want to execute: {comando}?")
        confirmation= input("y/n/modify: ")

        if confirmation == 'y': 
            pass
        elif confirmation == 'n': 
            return
        elif confirmation == 'modify':
            print(f"Comando actual: {comando}")
            comando= input(">> ")

    try:
        comm= subprocess.run(
            comando, 
            check= True, 
            capture_output= True, 
            text= True,
            shell= True
        )

        return comm.stdout
    except subprocess.CalledProcessError as e: 
        return f"Error al ejecutar el comando: [{e.stderr}]"