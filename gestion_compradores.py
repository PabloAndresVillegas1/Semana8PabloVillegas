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

def obtener_compradores():
    mydb = conectar_db()
    if mydb:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM compradores")
        compradores = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return compradores
    else:
        return []

def ver_compradores():
    root = tk.Toplevel()
    root.title("Ver Compradores")
    
    window_width = 600
    window_height = 350
    root.geometry(f"{window_width}x{window_height}")
    
    centrar_ventana(root, window_width, window_height)

    columns = ("ID", "Nombre", "Apellido", "Documento", "Teléfono", "Dirección", "Correo")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Apellido", text="Apellido")
    tree.heading("Documento", text="Documento")
    tree.heading("Teléfono", text="Teléfono")
    tree.heading("Dirección", text="Dirección")
    tree.heading("Correo", text="Correo")
    
    tree.column("ID", width=30, anchor='center')
    tree.column("Nombre", width=70, anchor='center')
    tree.column("Apellido", width=70, anchor='center')
    tree.column("Documento", width=70, anchor='center')
    tree.column("Teléfono", width=70, anchor='center')
    tree.column("Dirección", width=130, anchor='center')
    tree.column("Correo", width=130, anchor='center')
    
    for comprador in obtener_compradores():
        tree.insert("", tk.END, values=comprador)

    tree.pack(fill="both", expand=True)

    btn_agregar = ttk.Button(root, text="Agregar Comprador", command=agregar_comprador)
    btn_agregar.pack(side="left", padx=10, pady=10)

    btn_editar = ttk.Button(root, text="Editar Comprador", command=lambda: editar_comprador(tree))
    btn_editar.pack(side="left", padx=10, pady=10)

    btn_eliminar = ttk.Button(root, text="Eliminar Comprador", command=lambda: eliminar_comprador(tree))
    btn_eliminar.pack(side="left", padx=10, pady=10)

    cerrar_btn = ttk.Button(root, text="Cerrar", command=root.destroy)
    cerrar_btn.pack(pady=10)

def agregar_comprador():
    root = tk.Toplevel()
    root.title("Agregar Nuevo Comprador")

    window_width = 400
    window_height = 300
    root.geometry(f"{window_width}x{window_height}")

    centrar_ventana(root, window_width, window_height)

    tk.Label(root, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
    entry_nombre = tk.Entry(root)
    entry_nombre.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Apellido:").grid(row=1, column=0, padx=10, pady=10)
    entry_apellido = tk.Entry(root)
    entry_apellido.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(root, text="Documento:").grid(row=2, column=0, padx=10, pady=10)
    entry_documento = tk.Entry(root)
    entry_documento.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(root, text="Teléfono:").grid(row=3, column=0, padx=10, pady=10)
    entry_telefono = tk.Entry(root)
    entry_telefono.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(root, text="Dirección:").grid(row=4, column=0, padx=10, pady=10)
    entry_direccion = tk.Entry(root)
    entry_direccion.grid(row=4, column=1, padx=10, pady=10)

    tk.Label(root, text="Correo:").grid(row=5, column=0, padx=10, pady=10)
    entry_correo = tk.Entry(root)
    entry_correo.grid(row=5, column=1, padx=10, pady=10)

    def guardar_comprador():
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        documento = entry_documento.get()
        telefono = entry_telefono.get()
        direccion = entry_direccion.get()
        correo = entry_correo.get()

        if nombre and apellido and documento and telefono and direccion and correo:
            mydb = conectar_db()
            if mydb:
                mycursor = mydb.cursor()
                sql = "INSERT INTO compradores (Nombre, Apellido, Documento, Teléfono, Dirección, Correo) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (nombre, apellido, documento, telefono, direccion, correo)
                mycursor.execute(sql, val)
                mydb.commit()
                mycursor.close()
                mydb.close()

                messagebox.showinfo("Éxito", "Comprador agregado con éxito")
                root.destroy()
                ver_compradores()
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    btn_guardar = tk.Button(root, text="Guardar", command=guardar_comprador)
    btn_guardar.grid(row=6, column=0, columnspan=2, pady=10)

def editar_comprador(tree):
    selected_item = tree.selection()
    if selected_item:
        comprador_info = tree.item(selected_item)["values"]
        comprador_id = comprador_info[0]
        
        mydb = conectar_db()
        if mydb:
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM compradores WHERE ID = %s", (comprador_id,))
            comprador = mycursor.fetchone()
            mycursor.close()
            mydb.close()

            if comprador:
                root = tk.Toplevel()
                root.title("Editar Comprador")

                window_width = 400
                window_height = 300
                root.geometry(f"{window_width}x{window_height}")

                centrar_ventana(root, window_width, window_height)

                tk.Label(root, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
                entry_nombre = tk.Entry(root)
                entry_nombre.grid(row=0, column=1, padx=10, pady=10)
                entry_nombre.insert(0, comprador[1])

                tk.Label(root, text="Apellido:").grid(row=1, column=0, padx=10, pady=10)
                entry_apellido = tk.Entry(root)
                entry_apellido.grid(row=1, column=1, padx=10, pady=10)
                entry_apellido.insert(0, comprador[2])

                tk.Label(root, text="Documento:").grid(row=2, column=0, padx=10, pady=10)
                entry_documento = tk.Entry(root)
                entry_documento.grid(row=2, column=1, padx=10, pady=10)
                entry_documento.insert(0, comprador[3])

                tk.Label(root, text="Teléfono:").grid(row=3, column=0, padx=10, pady=10)
                entry_telefono = tk.Entry(root)
                entry_telefono.grid(row=3, column=1, padx=10, pady=10)
                entry_telefono.insert(0, comprador[4])

                tk.Label(root, text="Dirección:").grid(row=4, column=0, padx=10, pady=10)
                entry_direccion = tk.Entry(root)
                entry_direccion.grid(row=4, column=1, padx=10, pady=10)
                entry_direccion.insert(0, comprador[5])

                tk.Label(root, text="Correo:").grid(row=5, column=0, padx=10, pady=10)
                entry_correo = tk.Entry(root)
                entry_correo.grid(row=5, column=1, padx=10, pady=10)
                entry_correo.insert(0, comprador[6])

                def guardar_cambios():
                    nuevo_nombre = entry_nombre.get()
                    nuevo_apellido = entry_apellido.get()
                    nuevo_documento = entry_documento.get()
                    nuevo_telefono = entry_telefono.get()
                    nueva_direccion = entry_direccion.get()
                    nuevo_correo = entry_correo.get()

                    if nuevo_nombre and nuevo_apellido and nuevo_documento and nuevo_telefono and nueva_direccion and nuevo_correo:
                        mydb = conectar_db()
                        if mydb:
                            mycursor = mydb.cursor()
                            sql = "UPDATE compradores SET Nombre=%s, Apellido=%s, Documento=%s, Teléfono=%s, Dirección=%s, Correo=%s WHERE ID=%s"
                            val = (nuevo_nombre, nuevo_apellido, nuevo_documento, nuevo_telefono, nueva_direccion, nuevo_correo, comprador_id)
                            mycursor.execute(sql, val)
                            mydb.commit()
                            mycursor.close()
                            mydb.close()

                            messagebox.showinfo("Éxito", "Comprador actualizado con éxito")
                            root.destroy()
                            ver_compradores()
                        else:
                            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                    else:
                        messagebox.showerror("Error", "Todos los campos son obligatorios")

                btn_guardar = tk.Button(root, text="Guardar Cambios", command=guardar_cambios)
                btn_guardar.grid(row=6, column=0, columnspan=2, pady=10)
            else:
                messagebox.showerror("Error", "No se encontró el comprador seleccionado")
    else:
        messagebox.showerror("Error", "Por favor selecciona un comprador para editar")

def eliminar_comprador(tree):
    selected_item = tree.selection()
    if selected_item:
        comprador_info = tree.item(selected_item)["values"]
        comprador_id = comprador_info[0]

        respuesta = messagebox.askyesno("Confirmación", "¿Estás seguro de eliminar este comprador?")
        if respuesta:
            mydb = conectar_db()
            if mydb:
                mycursor = mydb.cursor()
                sql = "DELETE FROM compradores WHERE ID = %s"
                mycursor.execute(sql, (comprador_id,))
                mydb.commit()
                mycursor.close()
                mydb.close()

                messagebox.showinfo("Éxito", "Comprador eliminado con éxito")
                ver_compradores()
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
    else:
        messagebox.showerror("Error", "Por favor selecciona un comprador para eliminar")

def centrar_ventana(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")
