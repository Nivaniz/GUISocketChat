#Server GUI Chat (Admin)
import tkinter, socket, threading, json
from tkinter import DISABLED, VERTICAL, NORMAL, END

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
light_green = "#1fc742"

# Crear una clase de conexión para mantener el socket de servidor
class Connection():
    ''' Se guarda la conexión'''
    def __init__(self):
        self.host_ip = socket.gethostbyname(socket.gethostname())
        # 192.168.77.1
        self.encoder = 'utf-8'
        self.bytesize = 1024

        self.client_sockets = []
        self.client_ips = []
        self.banned_ips = []

# Definir funciones
def start_server(connection):
    ''' Comenzar el servidor en un puerto dado'''
    #Conseguir el numero de puerto para comenzar el servidor y unirlo al objeto de la conexión
    connection.port = int(port_entry.get())

    #Crear un socket de servidor
    connection.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.server_socket.bind((connection.host_ip, connection.port))
    connection.server_socket.listen()

    #Actualizar el estado de los botones
    history_listbox.delete(0, END)
    history_listbox.insert(0, f"Servidor iniciado en el puerto: {connection.port}.")
    end_button.config(state=NORMAL)
    self_broadcast_button.config(state=NORMAL)
    message_button.config(state=NORMAL)
    kick_button.config(state=NORMAL)
    ban_button.config(state=NORMAL)
    start_button.config(state=DISABLED)

    #Crear un hilo para escuchar continuamente las conexiones
    connect_thread = threading.Thread(target=connect_client, args=(connection,))
    connect_thread.start()


def end_server(connection):
    ''' Terminar el proceso de terminar el seridor '''
    pass

def connect_client(connection):
    ''' Conectar un cliente al servidor '''
    while True:
        try:
            client_socket, client_address = connection.server_socket.accept()
            #Checar si el IP del cliente está baneada
            if client_address[0] in connection.banned_ips:
                message_packet = create_message("Desconectado", "Admin (privado)", "Tu has sido baneado... Hasta pronto!", light_green)
                message_json = json.dumps(message_packet)
                client_socket.send(message_json.encode(connection.encoder))

                #Cerrar el socket del cliente
                client_socket.close()
            else:
                #Enviar el paquete del mensaje para recibir información del cliente
                message_packet = create_message("INFO", "Admin (privado)", "Por favor envia tu nombre", light_green)
                message_json = json.dumps(message_packet)
                client_socket.send(message_json.encode(connection.encoder))

                #Esperar por el mensaje de confirmación de ser enviado para verigicar la conexión
                message_json = client_socket.recv(connection.bytesize)
                process_message(connection, message_json, client_socket, client_address)
        except:
            break

def create_message(flag, name, message, color):
    ''' Regresar un mensaje en formato a enviar'''
    message_packet = {
        "flag": flag,
        "name": name,
        "message": message,
        "color": color,
    }

    return message_packet

def process_message(connection, flag, message_message_json, client_socket, client_address=(0,0)):
    ''' Actualizar la información del servidor basado en mensajes '''
    message_packet = json.loads(message_json) #decodificar y hacerlo diccionario
    flag = message_packet["flag"]
    name = message_packet["name"]
    message = message_packet["message"]
    color = message_packet["color"]

    if flag == "INFO":
        #Agregar la info del nuevo cliente a la lista
        connection.client_sockets.append(client_socket)
        connection.client_ips.append(client_address[0])

        #Enviar al nuevo cliente la actualización
        message_packet = create_message("MESSAGE", "Admin", f"{name} se ha unido al servidor!!!", light_green)
        message_json = json.dumps(message_packet)
        broadcast_message(connection, message_json.encode(connection.encoder))

        #Actualizar interfaz del servidor
        client_listbox.insert(END, f"Nombre: {name}        IP Addr: {client_address[0]}")

        #Una vez establecido el cliente, comenzar un hilo para recibir mensajes
        recieve_thread = threading.Thread(target=recieve_message, args=(connection, client_socket,))
        recieve_thread.start()
    
    elif flag == "MESSAGE":
        #Enviar el mensaje dado
        broadcast_message(connection, message_json)

        #Actualizar interfaz del servidor
        history_listbox.insert(0, f"{name}: {message}")
        history_listbox.itemconfig(0, fg=color)

    elif flag == "DISCONNECT":
        #Cerrar y remover el socket del cliente
        index = connection.client_sockets.index(client_socket)
        connection.client_sockets.remove(client_socket)
        connection.client_ips.pop(index)
        client_listbox.delete(index)
        client_socket.close()
 
        # Mensaje a los usuarios que el cliente ha salido
        message_packet = create_message("MESSAGE", "Admin", f"{name} ha salido del sevidor...", light_green)
        message_json = json.dumps(message_packet)
        broadcast_message(connection, message_json.encode(connection.encoder))

        #Actualizar interfaz del servidor
        history_listbox.insert(0, f"Admin: {name} ha salido del servidor...")

    else:
        history_listbox.insert(0, "Error procesando el mensaje...")

def broadcast_message(connection, message_json):
    ''' Enviar un mensaje a todos los clientes conectados al servidor / Todos los JSON estan encoded '''
    for client_socket in connection.client_sockets:
        client_socket.send(message_json)

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
start_button = tkinter.Button(connection_frame, text="Comenzar Servidor", borderwidth=5, width=15, font=my_font, bg=button_color, command=lambda:start_server(my_connection))
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

# Crear una connexión y correr la ventana principal
my_connection = Connection()
# Iniciar ventana
root.mainloop() 