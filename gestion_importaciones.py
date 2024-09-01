import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

db_config = {
    'host': 'bd-especializacion-comercializadoragremlins.g.aivencloud.com',
    'user': 'avnadmin',
    'password': 'AVNS_U0Rkp43qcL6pyg8qK0u',
    'database': 'defaultdb',
    'port': 20489
}

def conectar_db():
    try:
        mydb = mysql.connector.connect(**db_config)
        return mydb
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {err}")
        return None

def actualizar_treeview(tree):
    tree.delete(*tree.get_children())
    mydb = conectar_db()
    if mydb:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM importaciones")
        importaciones = cursor.fetchall()
        for importacion in importaciones:
            tree.insert("", tk.END, values=(importacion["ID"], importacion["Producto"], importacion["Proveedor"], importacion["Estado"], importacion["Fecha de Importación"]))
        cursor.close()
        mydb.close()

def ver_importaciones():
    root = tk.Toplevel()
    root.title("Ver Importaciones")

    window_width = 600
    window_height = 400
    root.geometry(f"{window_width}x{window_height}")

    centrar_ventana(root, window_width, window_height)

    columns = ("ID", "Producto", "Proveedor", "Estado", "Fecha de Importación")
    
    container = ttk.Frame(root)
    container.pack(fill="both", expand=True)

    tree = ttk.Treeview(container, columns=columns, show="headings")
    tree.pack(fill="both", expand=True)

    tree.heading("ID", text="ID")
    tree.column("ID", width=30, anchor='center')

    tree.heading("Producto", text="Producto")
    tree.column("Producto", width=70, anchor='center')

    tree.heading("Proveedor", text="Proveedor")
    tree.column("Proveedor", width=70, anchor='center')

    tree.heading("Estado", text="Estado")
    tree.column("Estado", width=70, anchor='center')

    tree.heading("Fecha de Importación", text="Fecha de Importación")
    tree.column("Fecha de Importación", width=70, anchor='center')

    actualizar_treeview(tree)

    btn_cerrar = ttk.Button(root, text="Cerrar", command=root.destroy)
    btn_cerrar.pack(pady=10)

def centrar_ventana(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")
