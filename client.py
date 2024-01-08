#Client GUI Chat 
import tkinter, socket, threading, json
from tkinter import DISABLED, VERTICAL, END, NORMAL, StringVar

#Definir ventana
root = tkinter.Tk()
root.title("Circle Talk")
root.iconbitmap("message_icon.ico")
root.geometry("600x600")
root.resizable(0,0)

my_font = ('Poppins', 13)
beige = "#F3EEEE"  # azulclaro 
negro = "#000000"
azulclaro = "#BBCAD6"
text_color = "#000000"  # Negro
pink = "#ff1493"  # Rosa más fuerte
red = "#ff0000"  # Rojo brillante
orange = "#ff8c00"  # Naranja intenso
yellow = "#ffd700"  # Amarillo brillante
green = "#00ff00"  # Verde brillante
blue = "#1e90ff"  # Azul brillante
purple = "#8a2be2"  # Morado intenso
root.config(bg='#F3EEEE') # BASE BEIGE

class Connection():
    '''Clase para almacenar una conexión'''
    def __init__(self):
        self.encoder = "utf-8"
        self.bytesize = 1024


def connect(connection):
    '''Conectar a un servidor en una dirección IP/puerto determinados'''
    # Limpiar cualquier chat anterior
    my_listbox.delete(0, END)

    # Obtener la información necesaria para la conexión desde los campos de entrada
    connection.name = name_entry.get()
    connection.target_ip = ip_entry.get()
    connection.port = port_entry.get()
    connection.color = color.get()

    try:
        # Crear un socket de cliente
        connection.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.client_socket.connect((connection.target_ip, int(connection.port)))

        # Recibir un paquete de mensaje entrante del servidor
        message_json = connection.client_socket.recv(connection.bytesize)
        process_message(connection, message_json)
    except:
        my_listbox.insert(0, "Conexión no establecida")


def disconnect(connection):
    '''Desconectar al cliente del servidor'''
    # Crear un paquete de mensaje para enviar
    message_packet = create_message("DISCONNECT", connection.name, "Me voy!.", connection.color)
    message_json = json.dumps(message_packet)
    connection.client_socket.send(message_json.encode(connection.encoder))

    # Deshabilitar la GUI para el chat
    gui_end()


def gui_start():
    '''Iniciar oficialmente la conexión actualizando la GUI'''
    connect_button.config(state=DISABLED)
    disconnect_button.config(state=NORMAL)
    send_button.config(state=NORMAL)
    name_entry.config(state=DISABLED)
    ip_entry.config(state=DISABLED)
    port_entry.config(state=DISABLED)

    for button in color_buttons:
        button.config(state=DISABLED)


def gui_end():
    '''Finalizar oficialmente la conexión actualizando la GUI'''
    connect_button.config(state=NORMAL)
    disconnect_button.config(state=DISABLED)
    send_button.config(state=DISABLED)
    name_entry.config(state=NORMAL)
    ip_entry.config(state=NORMAL)
    port_entry.config(state=NORMAL)

    for button in color_buttons:
        button.config(state=NORMAL)


def create_message(flag, name, message, color):
    '''Devolver un paquete de mensaje para enviar'''
    message_packet = {
        "flag": flag,
        "name": name,
        "message": message,
        "color": color,
    }
    return message_packet


def process_message(connection, message_json):
    '''Actualizar el cliente según la bandera del paquete de mensaje'''
    # Actualizar el historial del chat primero desempaquetando el mensaje JSON.
    message_packet = json.loads(message_json) 
    flag = message_packet["flag"]
    name = message_packet["name"]
    message = message_packet["message"]
    color = message_packet["color"]

    if flag == "INFO":
        # El servidor está solicitando información para verificar la conexión. Enviar la información.
        message_packet = create_message("INFO", connection.name, "Se ha unido a Circle Talk!", connection.color)
        message_json = json.dumps(message_packet)
        connection.client_socket.send(message_json.encode(connection.encoder))

        # Habilitar la GUI para el chat
        gui_start()

        # Crear un hilo para recibir continuamente mensajes del servidor
        recieve_thread = threading.Thread(target=recieve_message, args=(connection,))
        recieve_thread.start()
    
    elif flag == "MESSAGE":
        # El servidor ha enviado un mensaje, así que mostrarlo.
        my_listbox.insert(0, f"{name}: {message}")
        my_listbox.itemconfig(0, fg=color)


    elif flag == "DISCONNECT":
        # El servidor te está pidiendo que te vayas.
        my_listbox.insert(0, f"{name}: {message}")
        my_listbox.itemconfig(0, fg=color)
        disconnect(connection)

    else:
        # Captura de errores...
        my_listbox.insert(0, "Error procesando el mensaje...")


def send_message(connection):
    '''Enviar un mensaje al servidor'''
    # Enviar el mensaje al servidor
    message_packet = create_message("MESSAGE", connection.name, input_entry.get(), connection.color)
    message_json = json.dumps(message_packet)
    connection.client_socket.send(message_json.encode(connection.encoder))

    # Limpiar la entrada de texto
    input_entry.delete(0, END)


def recieve_message(connection):
    '''Recibir un mensaje del servidor'''
    while True:
        # Recibir un paquete de mensaje entrante del servidor
        try:
            # Recibir un paquete de mensaje entrante
            message_json = connection.client_socket.recv(connection.bytesize)
            process_message(connection, message_json)
        except:
            # No se puede recibir el mensaje, cerrar la conexión y salir
            my_listbox.insert(0, "La conexión se ha cerrado, hasta la proxima!...")
            break


# Definir la disposición de la GUI
# Crear marcos
info_frame = tkinter.Frame(root, bg=beige)
color_frame = tkinter.Frame(root, bg=beige)
output_frame = tkinter.Frame(root, bg=beige)
input_frame = tkinter.Frame(root, bg=beige)

info_frame.pack()
color_frame.pack()
output_frame.pack(pady=10)
input_frame.pack()

# Disposición del marco de información
name_label = tkinter.Label(info_frame, text="Nombre:", font=my_font, fg=negro, bg=beige)
name_entry = tkinter.Entry(info_frame, borderwidth=3, font=my_font)
ip_label = tkinter.Label(info_frame, text="IP:", font=my_font, fg=negro, bg=beige)
ip_entry = tkinter.Entry(info_frame, borderwidth=3, font=my_font)
port_label = tkinter.Label(info_frame, text="Puerto:", font=my_font, fg=negro, bg=beige)
port_entry = tkinter.Entry(info_frame, borderwidth=3, font=my_font, width=10)
connect_button = tkinter.Button(info_frame, text="Conectar", font=my_font, bg=azulclaro, borderwidth=5, width=10, command=lambda:connect(my_connection))
disconnect_button = tkinter.Button(info_frame, text="Desconectar", font=my_font, bg=azulclaro, borderwidth=5, width=10, state=DISABLED, command=lambda:disconnect(my_connection))

name_label.grid(row=0, column=0, padx=2, pady=10)
name_entry.grid(row=0, column=1, padx=2, pady=10)
port_label.grid(row=0, column=2, padx=2, pady=10)
port_entry.grid(row=0, column=3, padx=2, pady=10)
ip_label.grid(row=1, column=0, padx=2, pady=5)
ip_entry.grid(row=1, column=1, padx=2, pady=5)
connect_button.grid(row=1, column=2, padx=4, pady=5)
disconnect_button.grid(row=1, column=3, padx=4, pady=5)

# Disposición del marco de colores
color = StringVar()
color.set(pink)
pink_button = tkinter.Radiobutton(color_frame, width=5, text="Rosa", variable=color, value=pink, bg=beige, fg=negro, font=my_font)
red_button = tkinter.Radiobutton(color_frame, width=5, text="Rojo", variable=color, value=red, bg=beige, fg=negro, font=my_font)
orange_button = tkinter.Radiobutton(color_frame, width=5, text="Naranja", variable=color, value=orange, bg=beige, fg=negro, font=my_font)
yellow_button = tkinter.Radiobutton(color_frame, width=5, text="Amarillo", variable=color, value=yellow, bg=beige, fg=negro, font=my_font)
green_button = tkinter.Radiobutton(color_frame, width=5, text="Verde", variable=color, value=green, bg=beige, fg=negro, font=my_font)
blue_button = tkinter.Radiobutton(color_frame, width=5, text="Azul", variable=color, value=blue, bg=beige, fg=negro, font=my_font)
purple_button = tkinter.Radiobutton(color_frame, width=5, text="Morado", variable=color, value=purple, bg=beige, fg=negro, font=my_font)
color_buttons = [pink_button, red_button, orange_button, yellow_button, green_button, blue_button, purple_button]

pink_button.grid(row=1, column=0, padx=2, pady=2)
red_button.grid(row=1, column=1, padx=2, pady=2)
orange_button.grid(row=1, column=2, padx=2, pady=2)
yellow_button.grid(row=1, column=3, padx=2, pady=2)
green_button.grid(row=1, column=4, padx=2, pady=2)
blue_button.grid(row=1, column=5, padx=2, pady=2)
purple_button.grid(row=1, column=6, padx=2, pady=2)

# Disposición del marco de salida
my_scrollbar = tkinter.Scrollbar(output_frame, orient=VERTICAL)
my_listbox = tkinter.Listbox(output_frame, height=20, width=55, borderwidth=3, bg=beige, fg=negro, font=my_font, yscrollcommand=my_scrollbar.set)
my_scrollbar.config(command=my_listbox.yview)

my_listbox.grid(row=0, column=0)
my_scrollbar.grid(row=0, column=1, sticky="NS")

# Disposición del marco de entrada
input_entry = tkinter.Entry(input_frame, width=45, borderwidth=3, font=my_font)
send_button = tkinter.Button(input_frame, text="Enviar", borderwidth=5, width=10, font=my_font, bg=azulclaro, state=DISABLED, command=lambda:send_message(my_connection))
input_entry.grid(row=0, column=0, padx=5)
send_button.grid(row=0, column=1, padx=5)

# Crear un objeto de conexión y ejecutar el bucle principal de la ventana root
my_connection = Connection()
root.mainloop()