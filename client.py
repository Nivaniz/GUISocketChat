#Client GUI Chat 
import tkinter as tk, socket, threading
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

def connect():
  pass


def verify_connection():
    '''Verificar que la conexión del servidor sea válida y pase la información requerida'''
    pass


def disconnect():
    '''Desconectar del servidor'''

    pass


def send_message():
    '''Enviar un mensaje al servidor para ser transmitido.'''
    pass


def recieve_message():
    '''Recibir un mensaje entrante del servidor'''
    pass


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
connect_button = tk.Button(info_frame, text="Conectar", font=my_font, bg=button_color, borderwidth=5, width=10, command=connect)
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
colors_buttons =[white_button, red_button, orange_button, yellow_button, green_button, blue_button, purple_button]

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
root.mainloop()