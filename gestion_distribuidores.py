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
        cursor.execute("SELECT * FROM distribuidores")
        distribuidores = cursor.fetchall()
        for distribuidor in distribuidores:
            tree.insert("", tk.END, values=(distribuidor["ID"], distribuidor["Nombre"], distribuidor["NIT"], distribuidor["Teléfono"], distribuidor["Dirección"], distribuidor["Correo"]))
        cursor.close()
        mydb.close()

def gestionar_distribuidores():
    ver_distribuidores_window = tk.Toplevel()
    ver_distribuidores_window.title("Ver Distribuidores")
    
    window_width = 600
    window_height = 300
    ver_distribuidores_window.geometry(f"{window_width}x{window_height}")
    
    centrar_ventana(ver_distribuidores_window, window_width, window_height)

    columns = ("ID", "Nombre", "NIT", "Teléfono", "Dirección", "Correo")
    tree = ttk.Treeview(ver_distribuidores_window, columns=columns, show="headings")
    
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("NIT", text="NIT")
    tree.heading("Teléfono", text="Teléfono")
    tree.heading("Dirección", text="Dirección")
    tree.heading("Correo", text="Correo")
    
    tree.column("ID", width=30, anchor='center')
    tree.column("Nombre", width=70, anchor='center')
    tree.column("NIT", width=70, anchor='center')
    tree.column("Teléfono", width=70, anchor='center')
    tree.column("Dirección", width=120, anchor='center')
    tree.column("Correo", width=120, anchor='center')
    
    actualizar_treeview(tree)
    
    tree.pack(fill="both", expand=True)

    btn_agregar = ttk.Button(ver_distribuidores_window, text="Agregar Distribuidor", command=agregar_distribuidor)
    btn_agregar.pack(side="left", padx=10, pady=10)

    btn_editar = ttk.Button(ver_distribuidores_window, text="Editar Distribuidor", command=lambda: editar_distribuidor(tree))
    btn_editar.pack(side="left", padx=10, pady=10)

    btn_eliminar = ttk.Button(ver_distribuidores_window, text="Eliminar Distribuidor", command=lambda: eliminar_distribuidor(tree))
    btn_eliminar.pack(side="left", padx=10, pady=10)

    cerrar_btn = ttk.Button(ver_distribuidores_window, text="Cerrar", command=ver_distribuidores_window.destroy)
    cerrar_btn.pack(pady=10)

def agregar_distribuidor():
    ventana_agregar_distribuidor = tk.Toplevel()
    ventana_agregar_distribuidor.title("Agregar Nuevo Distribuidor")

    window_width = 350
    window_height = 250
    ventana_agregar_distribuidor.geometry(f"{window_width}x{window_height}")
    
    centrar_ventana(ventana_agregar_distribuidor, window_width, window_height)

    tk.Label(ventana_agregar_distribuidor, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
    entry_nombre = tk.Entry(ventana_agregar_distribuidor)
    entry_nombre.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(ventana_agregar_distribuidor, text="NIT:").grid(row=1, column=0, padx=10, pady=10)
    entry_nit = tk.Entry(ventana_agregar_distribuidor)
    entry_nit.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(ventana_agregar_distribuidor, text="Teléfono:").grid(row=2, column=0, padx=10, pady=10)
    entry_telefono = tk.Entry(ventana_agregar_distribuidor)
    entry_telefono.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(ventana_agregar_distribuidor, text="Dirección:").grid(row=3, column=0, padx=10, pady=10)
    entry_direccion = tk.Entry(ventana_agregar_distribuidor)
    entry_direccion.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(ventana_agregar_distribuidor, text="Correo:").grid(row=4, column=0, padx=10, pady=10)
    entry_correo = tk.Entry(ventana_agregar_distribuidor)
    entry_correo.grid(row=4, column=1, padx=10, pady=10)

    def guardar_distribuidor():
        nombre = entry_nombre.get()
        nit = entry_nit.get()
        telefono = entry_telefono.get()
        direccion = entry_direccion.get()
        correo = entry_correo.get()

        if nombre and nit and telefono and direccion and correo:
            mydb = conectar_db()
            if mydb:
                cursor = mydb.cursor()
                cursor.execute("""
                    INSERT INTO distribuidores (Nombre, NIT, Teléfono, Dirección, Correo)
                    VALUES (%s, %s, %s, %s, %s)
                """, (nombre, nit, telefono, direccion, correo))
                mydb.commit()
                cursor.close()
                mydb.close()

                messagebox.showinfo("Éxito", "Distribuidor agregado con éxito")
                ventana_agregar_distribuidor.destroy()
                gestionar_distribuidores()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    btn_guardar = tk.Button(ventana_agregar_distribuidor, text="Guardar", command=guardar_distribuidor)
    btn_guardar.grid(row=5, column=0, columnspan=2, pady=10)

    ventana_agregar_distribuidor.mainloop()

def editar_distribuidor(tree):
    selected_item = tree.selection()
    if selected_item:
        distribuidor_info = tree.item(selected_item)["values"]
        distribuidor_id = distribuidor_info[0]
        
        mydb = conectar_db()
        if mydb:
            cursor = mydb.cursor(dictionary=True)
            cursor.execute("SELECT * FROM distribuidores WHERE ID = %s", (distribuidor_id,))
            distribuidor = cursor.fetchone()
            cursor.close()
            mydb.close()

            if distribuidor:
                ventana_editar = tk.Toplevel()
                ventana_editar.title("Editar Distribuidor")
                
                window_width = 350
                window_height = 250
                ventana_editar.geometry(f"{window_width}x{window_height}")

                centrar_ventana(ventana_editar, window_width, window_height)

                tk.Label(ventana_editar, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
                entry_nombre = tk.Entry(ventana_editar)
                entry_nombre.grid(row=0, column=1, padx=10, pady=10)
                entry_nombre.insert(0, distribuidor["Nombre"])

                tk.Label(ventana_editar, text="NIT:").grid(row=1, column=0, padx=10, pady=10)
                entry_nit = tk.Entry(ventana_editar)
                entry_nit.grid(row=1, column=1, padx=10, pady=10)
                entry_nit.insert(0, distribuidor["NIT"])

                tk.Label(ventana_editar, text="Teléfono:").grid(row=2, column=0, padx=10, pady=10)
                entry_telefono = tk.Entry(ventana_editar)
                entry_telefono.grid(row=2, column=1, padx=10, pady=10)
                entry_telefono.insert(0, distribuidor["Teléfono"])

                tk.Label(ventana_editar, text="Dirección:").grid(row=3, column=0, padx=10, pady=10)
                entry_direccion = tk.Entry(ventana_editar)
                entry_direccion.grid(row=3, column=1, padx=10, pady=10)
                entry_direccion.insert(0, distribuidor["Dirección"])

                tk.Label(ventana_editar, text="Correo:").grid(row=4, column=0, padx=10, pady=10)
                entry_correo = tk.Entry(ventana_editar)
                entry_correo.grid(row=4, column=1, padx=10, pady=10)
                entry_correo.insert(0, distribuidor["Correo"])

                def guardar_cambios():
                    nombre = entry_nombre.get()
                    nit = entry_nit.get()
                    telefono = entry_telefono.get()
                    direccion = entry_direccion.get()
                    correo = entry_correo.get()

                    if nombre and nit and telefono and direccion and correo:
                        mydb = conectar_db()
                        if mydb:
                            cursor = mydb.cursor()
                            cursor.execute("""
                                UPDATE distribuidores 
                                SET Nombre = %s, NIT = %s, Teléfono = %s, Dirección = %s, Correo = %s
                                WHERE ID = %s
                            """, (nombre, nit, telefono, direccion, correo, distribuidor_id))
                            mydb.commit()
                            cursor.close()
                            mydb.close()

                            messagebox.showinfo("Éxito", "Distribuidor actualizado con éxito")
                            ventana_editar.destroy()
                            gestionar_distribuidores()
                    else:
                        messagebox.showerror("Error", "Todos los campos son obligatorios")

                btn_guardar = tk.Button(ventana_editar, text="Guardar Cambios", command=guardar_cambios)
                btn_guardar.grid(row=5, column=0, columnspan=2, pady=10)

                ventana_editar.mainloop()
    else:
        messagebox.showerror("Error", "Seleccione un distribuidor para editar")

def eliminar_distribuidor(tree):
    selected_item = tree.selection()
    if selected_item:
        distribuidor_info = tree.item(selected_item)["values"]
        distribuidor_id = distribuidor_info[0]

        mydb = conectar_db()
        if mydb:
            cursor = mydb.cursor()
            cursor.execute("DELETE FROM distribuidores WHERE ID = %s", (distribuidor_id,))
            mydb.commit()
            cursor.close()
            mydb.close()

            messagebox.showinfo("Éxito", "Distribuidor eliminado con éxito")
            gestionar_distribuidores()
    else:
        messagebox.showerror("Error", "Seleccione un distribuidor para eliminar")

def centrar_ventana(ventana, width, height):
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    ventana.geometry(f'{width}x{height}+{x}+{y}')
