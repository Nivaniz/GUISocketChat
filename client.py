#Client GUI Chat 
import tkinter as tk, socket, threading, json
from tkinter import DISABLED, VERTICAL, END, NORMAL, StringVar

#Definir ventana
root = tk.Tk()
root.title("Circle Talk")
root.iconbitmap("message_icon.ico")
root.geometry("600x600")
root.resizable(0,0)

# Definir fuentes y colores
my_font = ('Poppins', 13)
bg_color = "#F3EEEE"  # Beige 
button_color = "#BBCAD6"  # Azul claro
text_color = "#000000"  # Negro
white = "#ffffff"
red = "#ffb6c1"  # Rosa pastel
orange = "#ffd700"  # Amarillo pastel
yellow = "#ffebcd"  # Amarillo claro pastel
green = "#98fb98"  # Verde claro pastel
blue = "#add8e6"  # Azul claro pastel
purple = "#e6e6fa"  # Lila pastel


#Definir constantes
ENCODER = 'utf-8'
BYTESIZE = 1024

class Connection():
    ''' Una clase para guardar la información'''
    def __init__(self):
        self.encoder = "utf-8"
        self.bytesize = 1024

def connect(connection):
    #Borrar cualquier chats previos
    my_listbox.delete(0, END)

    #Recuperar la información para la conexión de los campos
    connection.name = name_entry.get()
    connection.target_ip = ip_entry.get()
    connection.port = port_entry.get()
    connection.color = color.get()

    try:
        #Crear un socket client
        connection.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.client_socket.connect((connection.target_ip, int(connection.port)))

        #Recibir paquetes de mensaje al servidor
        message_json = connection.client_socket.recv(connection.bytesize)
        process_message(connection, message_json)
    except:
        my_listbox.insert(0, "Error. Conexión no establecida.")

def disconnect(connection):
    ''' Desconectar el cliente del servidor'''
    pass

def gui_start():
    ''' Oficialmente comenzar una conexión actualizando el GUI'''
    connect_button.config(state=DISABLED)
    disconnect_button.config(state=NORMAL)
    send_button.config(state=NORMAL)
    name_entry.config(state=DISABLED)
    ip_entry.config(state=DISABLED)
    port_entry.config(state=DISABLED)

    for button in color_buttons:
        button.config(state=DISABLED)

def gui_end():
    ''' Oficialmente terminar una conexión actualizando el GUI'''
    pass

def create_message(flag, name, message, color):
    ''' Regresar un mensaje '''
    message_packet = {
        "flag": flag,
        "name": name,
        "message": message,
        "color": color,
    }
    return message_packet

def process_message(connection, message_json):
    ''' Regresar un mensaje '''
    #Actualizar el cliente 
    message_packet = json.loads(message_json)
    flag = message_packet["flag"]
    name = message_packet["name"]
    message = message_packet["message"]
    color = message_packet["color"]

    if flag == "INFO":
        #El servidor pide información para verificar la conexión. Enviar la info
        message_packet = create_message("INFO", connection.name, "Se une al servidor!", connection.color)
        message_json = json.dumps(message_packet)
        connection.client_socket.send(message_json.encode(connection.encoder))

        #Activar GUI para el chat
        gui_start()

        #Crear un hilo para continuamente recibir información
        recieve_thread = threading.Thread(target=recieve_message, args=(connection,))
        recieve_thread.start()
    
    elif flag == "MESSAGE":
        #El servidor envia un mensaje y se muestra
        my_listbox.insert(0, f"{name}: {message}")
        my_listbox.itemconfig(0, fg=color)


    elif flag == "DISCONNECT":
        #El servidor pide salir
        my_listbox.insert(0, f"{name}: {message}")
        my_listbox.itemconfig(0, fg=color)
        disconnect(connection)

    else:
        my_listbox.insert(0, "Error procesando el mensaje...")

def send_message(connection):
    ''' Enviar un mensaje al servidor '''
    pass

def recieve_message(connection):
    ''' Recibir un mensaje del servidor '''
    while True:
        try:
            message_json = connection.client_socket.recv(connection.bytesize)
            process_message(connection, message_json)
        except:
            my_listbox.insert(0, "La conexión se ha cerrado....")
            break

# GUI Layout
info_frame = tk.Frame(root, bg=bg_color)
color_frame = tk.Frame(root, bg=bg_color)
output_frame = tk.Frame(root, bg=bg_color)
input_frame = tk.Frame(root, bg=bg_color)

info_frame.pack()
color_frame.pack()
output_frame.pack(pady=10)
input_frame.pack()

# Info Frame Layout
name_label = tk.Label(info_frame, text="Nombre:", font=my_font, fg=text_color, bg=bg_color)
name_entry = tk.Entry(info_frame, borderwidth=3, font=my_font)
ip_label = tk.Label(info_frame, text="IP:", font=my_font, fg=text_color, bg=bg_color)
ip_entry = tk.Entry(info_frame, borderwidth=3, font=my_font)
port_label = tk.Label(info_frame, text="Puerto:", font=my_font, fg=text_color, bg=bg_color)
port_entry = tk.Entry(info_frame, borderwidth=3, font=my_font, width=10)
connect_button = tk.Button(info_frame, text="Conectar", font=my_font, bg=button_color, borderwidth=5, width=10, command=lambda:connect(my_connection))
disconnect_button = tk.Button(info_frame, text="Desconectar", font=my_font, bg=button_color, borderwidth=5, width=10, state=DISABLED, command=disconnect)

name_label.grid(row=0, column=0, padx=2, pady=10)
name_entry.grid(row=0, column=1, padx=2, pady=10)
port_label.grid(row=0, column=2, padx=2, pady=10)
port_entry.grid(row=0, column=3, padx=2, pady=10)
ip_label.grid(row=1, column=0, padx=2, pady=5)
ip_entry.grid(row=1, column=1, padx=2, pady=5)
connect_button.grid(row=1, column=2, padx=4, pady=5)
disconnect_button.grid(row=1, column=3, padx=4, pady=5)

# Color frame Layout
color = StringVar()
color.set(white)
white_button = tk.Radiobutton(color_frame, width=5, text="Blanco", variable=color, value=white, bg=bg_color, fg=text_color, font=my_font)
red_button = tk.Radiobutton(color_frame, width=5, text="Rojo", variable=color, value=red, bg=bg_color, fg=text_color, font=my_font)
orange_button = tk.Radiobutton(color_frame, width=5, text="Naranja", variable=color, value=orange, bg=bg_color, fg=text_color, font=my_font)
yellow_button = tk.Radiobutton(color_frame, width=5, text="Amarillo", variable=color, value=yellow, bg=bg_color, fg=text_color, font=my_font)
green_button = tk.Radiobutton(color_frame, width=5, text="Verde", variable=color, value=green, bg=bg_color, fg=text_color, font=my_font)
blue_button = tk.Radiobutton(color_frame, width=5, text="Azul", variable=color, value=blue, bg=bg_color, fg=text_color, font=my_font)
purple_button = tk.Radiobutton(color_frame, width=5, text="Morado", variable=color, value=purple, bg=bg_color, fg=text_color, font=my_font)
color_buttons =[white_button, red_button, orange_button, yellow_button, green_button, blue_button, purple_button]

white_button.grid(row=1, column=0, padx=2, pady=2)
red_button.grid(row=1, column=1, padx=2, pady=2)
orange_button.grid(row=1, column=2, padx=2, pady=2)
yellow_button.grid(row=1, column=3, padx=2, pady=2)
green_button.grid(row=1, column=4, padx=2, pady=2)
blue_button.grid(row=1, column=5, padx=2, pady=2)
purple_button.grid(row=1, column=6, padx=2, pady=2)



# Output Frame Layout
my_scrollbar = tk.Scrollbar(output_frame, orient=VERTICAL)
my_listbox = tk.Listbox(output_frame, height=20, width=55, borderwidth=3, bg=bg_color, fg=text_color, font=my_font, yscrollcommand=my_scrollbar.set)
my_scrollbar.config(command=my_listbox.yview)

my_listbox.grid(row=0, column=0)
my_scrollbar.grid(row=0, column=1, sticky="NS")

# Input Frame Layout
input_entry = tk.Entry(input_frame, width=45, borderwidth=3, font=my_font)
send_button = tk.Button(input_frame, text="Enviar", borderwidth=5, width=10, font=my_font, bg=button_color, state=DISABLED, command=send_message)
input_entry.grid(row=0, column=0, padx=5)
send_button.grid(row=0, column=1, padx=5)

# Configurar colores
root.config(bg=bg_color)
info_frame.config(bg=bg_color)
output_frame.config(bg=bg_color)
input_frame.config(bg=bg_color)

# Iniciar ventana
my_connection = Connection()
root.mainloop()