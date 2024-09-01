import tkinter as tk
from PIL import Image, ImageTk
import webbrowser

from gestion_distribuidores import gestionar_distribuidores
from gestion_empacadores import empaquetar_producto
from gestion_importaciones import ver_importaciones
from gestion_paquetes import ver_paquetes
from gestion_compradores import ver_compradores

def main():
    global root
    root = tk.Tk()
    root.title("Sistema de Información - Comercializadora Gremlins")

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    window_width = 600
    window_height = 500
    centrar_ventana(root, window_width, window_height)

    cargar_logo(root)

    gestion_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Compradores", menu=gestion_menu)
    gestion_menu.add_command(label="Gestionar Compradores", command=ver_compradores)
    
    productos_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Distribuidores", menu=productos_menu)
    productos_menu.add_command(label="Gestionar Distribuidores", command=gestionar_distribuidores)

    seguimiento_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Empaquetamiento", menu=seguimiento_menu)
    seguimiento_menu.add_command(label="Gestionar empaquetamiento", command=empaquetar_producto)
    
    transporte_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Paquetes", menu=transporte_menu)
    transporte_menu.add_command(label="Gestionar Paquetes", command=ver_paquetes)
    
    importaciones_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Importaciones", menu=importaciones_menu)
    importaciones_menu.add_command(label="Gestionar Importaciones", command=ver_importaciones)

    importaciones_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Documento-Word", menu=importaciones_menu)
    importaciones_menu.add_command(label="Abrir archivo de Word", command=abrir_archivo_word)

    root.mainloop()

def abrir_archivo_word():
    url = "https://uniminuto0-my.sharepoint.com/:w:/g/personal/pablo_villegas-m_uniminuto_edu_co/ERS2unwRa_lKn_0I6gD5yjkBi9WH060o30LVnU5gYwS9XQ?e=62chqb"
    webbrowser.open(url)

def centrar_ventana(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")

def cargar_logo(ventana):
    imagen_original = Image.open("logo.png")
    
    nuevo_ancho = 600
    nuevo_alto = 500
    imagen_redimensionada = imagen_original.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
    
    logo_tk = ImageTk.PhotoImage(imagen_redimensionada)
    
    label_logo = tk.Label(ventana, image=logo_tk)
    label_logo.image = logo_tk
    label_logo.pack()

if __name__ == "__main__":
    main()