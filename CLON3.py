import os
import requests
from stem import Signal
from stem.control import Controller
import pyperclip
import colorama

colorama.init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_html_source(url):
    try:
        if ".onion" in url:
            # Configuramos un proxy para acceder a sitios Onion
            with Controller.from_port(port=9051) as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)

            proxies = {'http': 'socks5h://localhost:9050',
                       'https': 'socks5h://localhost:9050'}

            response = requests.get(url, proxies=proxies)
        else:
            response = requests.get(url)
        
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error: No se pudo obtener el código fuente. Código de estado: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def copy_to_clipboard(text):
    try:
        pyperclip.copy(text)
        print(colorama.Fore.YELLOW + "El código fuente ha sido copiado al portapapeles.")
    except Exception as e:
        print(f"Error al copiar al portapapeles: {e}")

def main():
    clear_screen()

    print(colorama.Fore.YELLOW + """
  _____ ___  _____  ______    _____ _      ____  _   _ ____  
 / ____/ _ \|  __ \|  ____|  / ____| |    / __ \| \ | |___ \ 
| |   | | | | |  | | |__    | |    | |   | |  | |  \| | __) |
| |   | | | | |  | |  __|   | |    | |   | |  | | . ` ||__ < 
| |___| |_| | |__| | |____  | |____| |___| |__| | |\  |___) |
 \_____\___/|_____/|______|  \_____|______\____/|_| \_|____/ 
                                                              
                                                               """)

    print("Bienvenido a la herramienta para obtener el código fuente de una página web.")
    print("Por favor, introduce la URL de la página web que deseas inspeccionar.")

    while True:
        url = input(colorama.Fore.YELLOW + "URL: ")
        if url.lower() == "exit":
            print("Saliendo del programa...")
            break
        html_source = get_html_source(url)
        if html_source:
            print(f"\nCódigo fuente de {url}:\n")
            print(html_source)
            print("\n")
            print("¿Quieres inspeccionar otra página web o copiar el código al portapapeles?")
            print("1. Inspeccionar otra página web")
            print("2. Copiar al portapapeles")
            choice = input(colorama.Fore.YELLOW + "Elige una opción: ")
            if choice == "2":
                copy_to_clipboard(html_source)
            print("\n")
        else:
            print("\nNo se pudo obtener el código fuente de la página web.")
            print("Por favor, asegúrate de que la URL sea válida e inténtalo de nuevo.")
            print("También puedes escribir 'exit' para salir del programa.")

if __name__ == "__main__":
    main()
