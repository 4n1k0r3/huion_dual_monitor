import os
import subprocess
from pynput import keyboard

# Archivo para almacenar el estado
state_file = '/tmp/toggle_output_state'

# Verifica si el archivo de estado existe, si no, lo crea y lo inicializa en 0
if not os.path.exists(state_file):
    with open(state_file, 'w') as f:
        f.write('0')

# Función para obtener el ID del dispositivo Huion
def get_huion_id():
    try:
        # Ejecuta el comando xinput y busca el ID del dispositivo Huion
        output = subprocess.check_output("xinput | grep 'HUION'", shell=True, text=True)
        # Extrae el ID del dispositivo de la salida
        for line in output.splitlines():
            if 'HUION' in line:
                return line.split('id=')[1].split()[0]  # Obtiene el ID
    except Exception as e:
        print(f'Error al obtener el ID del dispositivo: {e}')
    return None

# Función para alternar el estado
def toggle_output():
    huion_id = get_huion_id()
    if huion_id is None:
        print("No se pudo encontrar el ID del dispositivo Huion.")
        return

    with open(state_file, 'r') as f:
        state = int(f.read().strip())

    if state == 0:
        # Cambia a la salida DP-1
        result = subprocess.run(['xinput', 'map-to-output', huion_id, 'DP-1'], capture_output=True, text=True)
        new_state = 1
    else:
        # Cambia a la salida eDP-1
        result = subprocess.run(['xinput', 'map-to-output', huion_id, 'eDP-1'], capture_output=True, text=True)
        new_state = 0

    if result.returncode != 0:
        print(f'Error al ejecutar el comando: {result.stderr}')

    with open(state_file, 'w') as f:
        f.write(str(new_state))

# Función que se llama al presionar una tecla
def on_press(key):
    try:
        if key == keyboard.Key.f4:
            toggle_output()
    except Exception as e:
        print(f'Error: {e}')

# Configura el listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

