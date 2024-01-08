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
black = "#F3EEEE" # Beige
light_green = "#BBCAD6" # Azul claro
light_greenn = "#000000" # Negro
root.config(bg='#F3EEEE') # Beige base


class Connection():
    '''Clase para almacenar una conexión'''
    def __init__(self):
        self.host_ip = socket.gethostbyname(socket.gethostname())
        self.encoder = 'utf-8'
        self.bytesize = 1024

        self.client_sockets = []
        self.client_ips = []
        self.banned_ips = []


def start_server(connection):
    '''Iniciar el servidor en un número de puerto dado'''
    #Obtener el número de puerto para ejecutar el servidor y adjuntar al objeto de conexión
    connection.port = int(port_entry.get())

    #Crear socket del servidor
    connection.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.server_socket.bind((connection.host_ip, connection.port))
    connection.server_socket.listen()

    #Actualizar GUI
    history_listbox.delete(0, END)
    history_listbox.insert(0, f"Servidor iniciado en puerto: {connection.port}.")
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
    '''Iniciar el proceso de cierre del servidor'''
    # Alertar a todos los usuarios que el servidor se está cerrando
    message_packet = create_message("DISCONNECT", "Admin (broadcast)", "El servidor se está cerrando...", light_greenn)
    message_json = json.dumps(message_packet)
    broadcast_message(connection, message_json.encode(connection.encoder))

    # Actualizar GUI
    history_listbox.insert(0, f"Servidor cerrándose en puerto {connection.port}.")
    end_button.config(state=DISABLED)
    self_broadcast_button.config(state=DISABLED)
    message_button.config(state=DISABLED)
    kick_button.config(state=DISABLED)
    ban_button.config(state=DISABLED)
    start_button.config(state=NORMAL)

    # Cerrar socket del servidor
    connection.server_socket.close()


def connect_client(connection):
    '''Conectar un cliente entrante al servidor'''
    while True:
        try:
            client_socket, client_address = connection.server_socket.accept()
            # Verificar si la IP del cliente está prohibida.
            if client_address[0] in connection.banned_ips:
                message_packet = create_message("DISCONNECT", "Admin (private)", "Has sido baneado por violar nuestras normas", light_greenn)
                message_json = json.dumps(message_packet)
                client_socket.send(message_json.encode(connection.encoder))

                # Cerrar el socket del cliente
                client_socket.close()
            else:
                # Enviar un paquete de mensaje para recibir la información del cliente
                message_packet = create_message("INFO", "Admin (private)", "Por favor envía tu nombre", light_greenn)
                message_json = json.dumps(message_packet)
                client_socket.send(message_json.encode(connection.encoder))

                # Esperar el mensaje de confirmación que verifica la conexión
                message_json = client_socket.recv(connection.bytesize)
                process_message(connection, message_json, client_socket, client_address)
        except:
            break


def create_message(flag, name, message, color):
    '''Devolver un paquete de mensaje para ser enviado'''
    message_packet = {
        "flag": flag,
        "name": name,
        "message": message,
        "color": color,
    }

    return message_packet


def process_message(connection, message_json, client_socket, client_address=(0,0)):
    '''Actualizar información del servidor basada en una bandera del paquete de mensaje'''
    message_packet = json.loads(message_json) 
    flag = message_packet["flag"]
    name = message_packet["name"]
    message = message_packet["message"]
    color = message_packet["color"]

    if flag == "INFO":
        # Agregar la nueva información del cliente a las listas apropiadas
        connection.client_sockets.append(client_socket)
        connection.client_ips.append(client_address[0])

        # Difundir el nuevo cliente que se une y actualizar la GUI
        message_packet = create_message("MESSAGE", "Admin (broadcast)", f"{name} se ha unido a Circle Talk!!!", light_greenn)
        message_json = json.dumps(message_packet)
        broadcast_message(connection, message_json.encode(connection.encoder))

        # Actualizar interfaz de usuario del servidor
        client_listbox.insert(END, f"Nombre: {name}        IP Addr: {client_address[0]}")

         # Ahora que se ha establecido un cliente, iniciar un hilo para recibir mensajes
        recieve_thread = threading.Thread(target=recieve_message, args=(connection, client_socket,))
        recieve_thread.start()
    
    elif flag == "MESSAGE":
        # Difundir el mensaje dado
        broadcast_message(connection, message_json)

        # Actualizar interfaz de usuario del servidor
        history_listbox.insert(0, f"{name}: {message}")
        history_listbox.itemconfig(0, fg=color)

    elif flag == "DISCONNECT":
        # Cerrar/eliminar socket del cliente
        index = connection.client_sockets.index(client_socket)
        connection.client_sockets.remove(client_socket)
        connection.client_ips.pop(index)
        client_listbox.delete(index)
        client_socket.close()
 
        # Avisar a todos los usuarios que el cliente ha abandonado el chat
        message_packet = create_message("MESSAGE", "Admin (broadcast)", f"{name} ha salido de Circle Talk...", light_greenn)
        message_json = json.dumps(message_packet)
        broadcast_message(connection, message_json.encode(connection.encoder))

        # Actualizar interfaz de usuario del servidor
        history_listbox.insert(0, f"Admin (broadcast): {name} ha salido de Circle Talk...")

    else:
        # Captura de errores...
        history_listbox.insert(0, "Error procesando el mensaje...")


def broadcast_message(connection, message_json):
    '''Enviar un mensaje a todos los sockets de cliente conectados al servidor... TODOS LOS JSON ESTÁN CODIFICADOS'''
    for client_socket in connection.client_sockets:
        client_socket.send(message_json)


def recieve_message(connection, client_socket):
    '''Recibir un mensaje entrante de un cliente'''
    while True:
        # Obtener un mensaje_json de un cliente
        try:
            message_json = client_socket.recv(connection.bytesize)
            process_message(connection, message_json, client_socket)
        except:
            break


def self_broadcast(connection):
    '''Transmitir un mensaje especial del administrador a todos los clientes'''
    # Crear un paquete de mensaje
    message_packet = create_message("MESSAGE", "Admin (broadcast)", input_entry.get(), light_greenn)
    message_json = json.dumps(message_packet)
    broadcast_message(connection, message_json.encode(connection.encoder))

    # Limpiar la entrada de texto
    input_entry.delete(0, END)


def private_message(connection):
    '''Enviar un mensaje privado a un solo cliente'''
    # Seleccionar el cliente de la lista de clientes y acceder a su socket de cliente
    index = client_listbox.curselection()[0]
    client_socket = connection.client_sockets[index]

    # Crear un paquete de mensaje y enviar
    message_packet = create_message("MESSAGE", "Admin (private)", input_entry.get(), light_greenn)
    message_json = json.dumps(message_packet)
    client_socket.send(message_json.encode(connection.encoder))

    # Limpiar la entrada de texto
    input_entry.delete(0, END)


def kick_client(connection):
    '''Expulsar a un cliente específico del servidor'''
    # Seleccionar un cliente de la lista
    index = client_listbox.curselection()[0]
    client_socket = connection.client_sockets[index]

    # Crear el paquete de mensaje
    message_packet = create_message("DISCONNECT", "Admin (private)", "Tu has sido kickeado...", light_green)
    message_json = json.dumps(message_packet)
    client_socket.send(message_json.encode(connection.encoder))


def ban_client(connection):
    '''Prohibir a un cliente específico según su dirección IP'''
    # Seleccionar un cliente de la lista
    index = client_listbox.curselection()[0]
    client_socket = connection.client_sockets[index]

    # Crear el paquete de mensaje
    message_packet = create_message("DISCONNECT", "Admin (private)", "Tu has sido baneado...", light_greenn)
    message_json = json.dumps(message_packet)
    client_socket.send(message_json.encode(connection.encoder))

    # Prohibir la dirección IP del cliente
    connection.banned_ips.append(connection.client_ips[index])


# Definir la disposición de la GUI
# Crear marcos
connection_frame = tkinter.Frame(root, bg=black)
history_frame = tkinter.Frame(root, bg=black)
client_frame = tkinter.Frame(root, bg=black)
message_frame = tkinter.Frame(root, bg=black)
admin_frame = tkinter.Frame(root, bg=black)

connection_frame.pack(pady=5)
history_frame.pack()
client_frame.pack(pady=5)
message_frame.pack()
admin_frame.pack()

#Connexión
port_label = tkinter.Label(connection_frame, text="Puerto:", font=my_font, bg=black, fg=light_greenn)
port_entry = tkinter.Entry(connection_frame, width=10, borderwidth=3, font=my_font)
start_button = tkinter.Button(connection_frame, text="Iniciar", borderwidth=5, width=15, font=my_font, bg=light_green, command=lambda:start_server(my_connection))
end_button = tkinter.Button(connection_frame, text="Cerrar", borderwidth=5, width=15, font=my_font, bg=light_green, state=DISABLED, command=lambda:end_server(my_connection))

port_label.grid(row=0, column=0, padx=2, pady=10)
port_entry.grid(row=0, column=1, padx=2, pady=10)
start_button.grid(row=0, column=2, padx=5, pady=10)
end_button.grid(row=0, column=3, padx=5, pady=10)

#Historial
history_scrollbar = tkinter.Scrollbar(history_frame, orient=VERTICAL)
history_listbox = tkinter.Listbox(history_frame, height=10, width=55, borderwidth=3, font=my_font, bg=black, fg=light_greenn, yscrollcommand=history_scrollbar.set)
history_scrollbar.config(command=history_listbox.yview)

history_listbox.grid(row=0, column=0)
history_scrollbar.grid(row=0, column=1, sticky="NS")

#Cliente
client_scrollbar = tkinter.Scrollbar(client_frame, orient=VERTICAL)
client_listbox = tkinter.Listbox(client_frame, height=10, width=55, borderwidth=3, font=my_font, bg=black, fg=light_greenn, yscrollcommand=client_scrollbar.set)
client_scrollbar.config(command=client_listbox.yview)

client_listbox.grid(row=0, column=0)
client_scrollbar.grid(row=0, column=1, sticky="NS")

#Mensaje
input_entry = tkinter.Entry(message_frame, width=40, borderwidth=3, font=my_font)
self_broadcast_button = tkinter.Button(message_frame, text="Enviar", width=13, borderwidth=5, font=my_font, bg=light_green, state=DISABLED, command=lambda:self_broadcast(my_connection))

input_entry.grid(row=0, column=0, padx=5, pady=5)
self_broadcast_button.grid(row=0, column=1, padx=5, pady=5)

#Admin 
message_button = tkinter.Button(admin_frame, text="Privado", borderwidth=5, width=15, font=my_font, bg=light_green, state=DISABLED, command=lambda:private_message(my_connection))
kick_button = tkinter.Button(admin_frame, text="Kickear", borderwidth=5, width=15, font=my_font, bg=light_green, state=DISABLED, command=lambda:kick_client(my_connection))
ban_button = tkinter.Button(admin_frame, text="Banear", borderwidth=5, width=15, font=my_font, bg=light_green, state=DISABLED, command=lambda:ban_client(my_connection))

message_button.grid(row=0, column=0, padx=5, pady=5)
kick_button.grid(row=0, column=1, padx=5, pady=5)
ban_button.grid(row=0, column=2, padx=5, pady=5)

# Crear un objeto de conexión y ejecutar el bucle principal de la ventana root
my_connection = Connection()
root.mainloop()