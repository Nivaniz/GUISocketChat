#Server GUI Chat (Admin)
import tkinter, socket, threading, json
from tkinter import DISABLED, VERTICAL

# Definir ventana principal
root = tkinter.Tk()
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

# Crear una clase de conexión para mantener el socket de servidor
class Connection():
    ''' Se guarda la conexión'''
    def __init__(self):
        pass

# Definir funciones
def start_server(connection):
    ''' Comenzar el servidor en un puerto dado'''
    pass

def end_server(connection):
    ''' Terminar el proceso de terminar el seridor '''
    pass

def connect_client(connection):
    ''' Conectar un cliente al servidor '''
    pass

def create_message(flag, name, message, color):
    ''' Regresar un mensaje a enviar'''
    pass

def process_message(connection, flag, message_message_json, client_socket, client_address=(0,0)):
    ''' Actualizar la información del servidor basado en mensajes '''
    pass

def broadcast_message(connection, message_json):
    ''' Enviar un mensaje a todos los clientes conectados al servidor '''
    pass

def recieve_message(connection, client_socket):
    ''' Recibir mensajes de un cliente '''
    pass

def self_broadcast(connection):
    ''' Enviar un mensaje especial del administrador a todos los clientes '''
    pass

def private_message(connection):
    ''' Enviar un mensaje privado a un cliente '''
    pass

def kick_client(connection):
    ''' Expulsar a un cliente dado '''
    pass

def ban_client(connection):
    ''' Banear a un cliente por su '''
    pass

# Definir Layout GUI
connection_frame = tkinter.Frame(root, bg=bg_color)
history_frame = tkinter.Frame(root, bg=bg_color)
client_frame = tkinter.Frame(root, bg=bg_color)
message_frame = tkinter.Frame(root, bg=bg_color)
admin_frame = tkinter.Frame(root, bg=bg_color)

connection_frame.pack(pady=5)
history_frame.pack()
client_frame.pack(pady=5)
message_frame.pack()
admin_frame.pack()

# Layout de la conexión
port_label = tkinter.Label(connection_frame, text="Numero de Puerto:", font=my_font, bg=bg_color, fg=text_color)
port_entry = tkinter.Entry(connection_frame, width=10, borderwidth=3, font=my_font)
start_button = tkinter.Button(connection_frame, text="Comenzar Servidor", borderwidth=5, width=15, font=my_font, bg=button_color)
end_button = tkinter.Button(connection_frame, text="Finalizar Servidor", borderwidth=5, width=15, font=my_font, bg=button_color, state=DISABLED)

port_label.grid(row=0, column=0, padx=2, pady=10)
port_entry.grid(row=0, column=1, padx=2, pady=10)
start_button.grid(row=0, column=2, padx=5, pady=10)
end_button.grid(row=0, column=3, padx=5, pady=10)

#Layout del historial
history_scrollbar = tkinter.Scrollbar(history_frame, orient=VERTICAL)
history_listbox = tkinter.Listbox(history_frame, height=10, width=55, borderwidth=3, font=my_font, bg=bg_color, fg=text_color, yscrollcommand=history_scrollbar.set)
history_scrollbar.config(command=history_listbox.yview)

history_listbox.grid(row=0, column=0)
history_scrollbar.grid(row=0, column=1, sticky="NS")

#Layout del cliente
client_scrollbar = tkinter.Scrollbar(client_frame, orient=VERTICAL)
client_listbox = tkinter.Listbox(client_frame, height=10, width=55, borderwidth=3, font=my_font, bg=bg_color, fg=text_color, yscrollcommand=client_scrollbar.set)
client_scrollbar.config(command=client_listbox.yview)

client_listbox.grid(row=0, column=0)
client_scrollbar.grid(row=0, column=1, sticky="NS")

#Layout del mensaje
input_entry = tkinter.Entry(message_frame, width=40, borderwidth=3, font=my_font)
self_broadcast_button = tkinter.Button(message_frame, text="Broadcast", width=13, borderwidth=5, font=my_font, bg=button_color, state=DISABLED)

input_entry.grid(row=0, column=0, padx=5, pady=5)
self_broadcast_button.grid(row=0, column=1, padx=5, pady=5)

#Layout del administrador
message_button = tkinter.Button(admin_frame, text="PM", borderwidth=5, width=15, font=my_font, bg=button_color, state=DISABLED)
kick_button = tkinter.Button(admin_frame, text="Kick", borderwidth=5, width=15, font=my_font, bg=button_color, state=DISABLED)
ban_button = tkinter.Button(admin_frame, text="Ban", borderwidth=5, width=15, font=my_font, bg=button_color, state=DISABLED)

message_button.grid(row=0, column=0, padx=5, pady=5)
kick_button.grid(row=0, column=1, padx=5, pady=5)
ban_button.grid(row=0, column=2, padx=5, pady=5)


# Iniciar ventana
root.mainloop() 