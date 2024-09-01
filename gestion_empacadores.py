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
        cursor.execute("SELECT * FROM paquetes")
        paquetes = cursor.fetchall()
        for paquete in paquetes:
            tree.insert("", tk.END, values=(paquete["ID"], paquete["Cliente"], paquete["Distribuidor"], paquete["Estado"], paquete["Fase"], paquete["Fecha_Salida"], paquete["Hora_Salida"], paquete["Fecha_Llegada"], paquete["Hora_Llegada"]))
        cursor.close()
        mydb.close()

def empaquetar_producto():
    root = tk.Toplevel()
    root.title("Empaquetar Producto")

    window_width = 500
    window_height = 400
    root.geometry(f"{window_width}x{window_height}")

    centrar_ventana(root, window_width, window_height)

    tk.Label(root, text="ID del Producto:").grid(row=0, column=0, padx=10, pady=10)
    entry_id_producto = tk.Entry(root)
    entry_id_producto.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Cliente:").grid(row=1, column=0, padx=10, pady=10)
    entry_cliente = tk.Entry(root)
    entry_cliente.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(root, text="Distribuidor:").grid(row=2, column=0, padx=10, pady=10)
    entry_distribuidor = tk.Entry(root)
    entry_distribuidor.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(root, text="Fecha de Salida (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=10)
    entry_fecha_salida = tk.Entry(root)
    entry_fecha_salida.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(root, text="Hora de Salida (HH:MM:SS):").grid(row=4, column=0, padx=10, pady=10)
    entry_hora_salida = tk.Entry(root)
    entry_hora_salida.grid(row=4, column=1, padx=10, pady=10)

    tk.Label(root, text="Fecha de Llegada (YYYY-MM-DD):").grid(row=5, column=0, padx=10, pady=10)
    entry_fecha_llegada = tk.Entry(root)
    entry_fecha_llegada.grid(row=5, column=1, padx=10, pady=10)

    tk.Label(root, text="Hora de Llegada (HH:MM:SS):").grid(row=6, column=0, padx=10, pady=10)
    entry_hora_llegada = tk.Entry(root)
    entry_hora_llegada.grid(row=6, column=1, padx=10, pady=10)

    def confirmar_empaquetado():
        producto_id = entry_id_producto.get()
        cliente = entry_cliente.get()
        distribuidor = entry_distribuidor.get()
        fecha_salida = entry_fecha_salida.get()
        hora_salida = entry_hora_salida.get()
        fecha_llegada = entry_fecha_llegada.get()
        hora_llegada = entry_hora_llegada.get()

        mydb = conectar_db()
        if mydb:
            cursor = mydb.cursor()
            # Verificar si el ID ya existe
            cursor.execute("SELECT COUNT(*) FROM paquetes WHERE ID = %s", (producto_id,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", f"El ID {producto_id} ya existe en la base de datos.")
                cursor.close()
                mydb.close()
                return

            # Insertar nuevo registro
            cursor.execute(
                "INSERT INTO paquetes (ID, Cliente, Distribuidor, Estado, Fase, Fecha_Salida, Hora_Salida, Fecha_Llegada, Hora_Llegada) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (producto_id, cliente, distribuidor, "Pendiente", "En almacén", fecha_salida, hora_salida, fecha_llegada, hora_llegada)
            )
            mydb.commit()
            cursor.close()
            mydb.close()

            messagebox.showinfo("Éxito", f"Producto {producto_id} empaquetado con éxito para {cliente}. Estado: Pendiente")
            root.destroy()
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")

    btn_confirmar = tk.Button(root, text="Confirmar Empaquetado", command=confirmar_empaquetado)
    btn_confirmar.grid(row=7, column=0, columnspan=2, pady=10)

    btn_cerrar = ttk.Button(root, text="Cerrar", command=root.destroy)
    btn_cerrar.grid(row=8, column=0, columnspan=2, pady=10)

def centrar_ventana(ventana, width, height):
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    ventana.geometry(f'{width}x{height}+{x}+{y}')