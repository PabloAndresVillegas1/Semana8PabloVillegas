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

def ver_paquetes():
    root = tk.Toplevel()
    root.title("Ver Paquetes")

    window_width = 700
    window_height = 400
    root.geometry(f"{window_width}x{window_height}")

    centrar_ventana(root, window_width, window_height)

    columns = ("ID", "Cliente", "Distribuidor", "Estado", "Fase", "Fecha_Salida", "Hora_Salida", "Fecha_Llegada", "Hora_Llegada")
    tree = ttk.Treeview(root, columns=columns, show="headings")

    column_widths = {
        "ID": 30,
        "Cliente": 70,
        "Distribuidor": 100,
        "Estado": 70,
        "Fase": 70,
        "Fecha_Salida": 70,
        "Hora_Salida": 70,
        "Fecha_Llegada": 70,
        "Hora_Llegada": 70
    }
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=column_widths.get(col, 100), anchor='center')

    mydb = conectar_db()
    if mydb:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM paquetes")
        paquetes = cursor.fetchall()
        for paquete in paquetes:
            tree.insert("", tk.END, values=(paquete["ID"], paquete["Cliente"], paquete["Distribuidor"], paquete["Estado"], paquete["Fase"], paquete["Fecha_Salida"], paquete["Hora_Salida"], paquete["Fecha_Llegada"], paquete["Hora_Llegada"]))
        cursor.close()
        mydb.close()

    tree.pack(fill="both", expand=True)

    btn_aceptar = ttk.Button(root, text="Aceptar Paquete", command=lambda: aceptar_paquete(tree))
    btn_aceptar.pack(side="left", padx=10, pady=10)

    btn_cancelar = ttk.Button(root, text="Cancelar Paquete", command=lambda: cancelar_paquete(tree))
    btn_cancelar.pack(side="left", padx=10, pady=10)

    btn_cambiar_datos = ttk.Button(root, text="Cambiar Datos", command=lambda: cambiar_datos(tree))
    btn_cambiar_datos.pack(side="left", padx=10, pady=10)

    btn_cambiar_fase = ttk.Button(root, text="Cambiar Fase", command=lambda: cambiar_fase(tree))
    btn_cambiar_fase.pack(side="left", padx=10, pady=10)

    btn_cambiar_fechas = ttk.Button(root, text="Cambiar Fechas y Horarios", command=lambda: cambiar_fechas(tree))
    btn_cambiar_fechas.pack(side="left", padx=10, pady=10)

    cerrar_btn = ttk.Button(root, text="Cerrar", command=root.destroy)
    cerrar_btn.pack(pady=10)

def aceptar_paquete(tree):
    selected_item = tree.selection()
    if selected_item:
        paquete_info = tree.item(selected_item)["values"]
        paquete_id = paquete_info[0]

        mydb = conectar_db()
        if mydb:
            cursor = mydb.cursor()
            cursor.execute("UPDATE paquetes SET Estado = %s WHERE ID = %s", ("Aceptado", paquete_id))
            mydb.commit()

            tree.item(selected_item, values=(
                paquete_id,
                paquete_info[1],
                paquete_info[2],
                "Aceptado",
                paquete_info[4],
                paquete_info[5],
                paquete_info[6],
                paquete_info[7],
                paquete_info[8]
            ))
            cursor.close()
            mydb.close()
            messagebox.showinfo("Éxito", "Paquete aceptado con éxito")
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
    else:
        messagebox.showerror("Error", "Seleccione un paquete para aceptar")

def cancelar_paquete(tree):
    selected_item = tree.selection()
    if selected_item:
        paquete_info = tree.item(selected_item)["values"]
        paquete_id = paquete_info[0]

        confirm = messagebox.askyesno("Confirmar Cancelación", "¿Está seguro de que desea cancelar este paquete?")

        if confirm:
            mydb = conectar_db()
            if mydb:
                cursor = mydb.cursor()
                cursor.execute("DELETE FROM paquetes WHERE ID = %s", (paquete_id,))
                mydb.commit()

                tree.delete(selected_item)
                cursor.close()
                mydb.close()
                messagebox.showinfo("Éxito", "Paquete cancelado con éxito")
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
    else:
        messagebox.showerror("Error", "Seleccione un paquete para cancelar")

def cambiar_datos(tree):
    selected_item = tree.selection()
    if selected_item:
        paquete_info = tree.item(selected_item)["values"]
        paquete_id = paquete_info[0]
        
        root = tk.Toplevel()
        root.title("Cambiar Datos del Paquete")

        window_width = 300
        window_height = 250
        root.geometry(f"{window_width}x{window_height}")

        centrar_ventana(root, window_width, window_height)

        tk.Label(root, text="Cliente:").grid(row=0, column=0, padx=10, pady=10)
        entry_cliente = tk.Entry(root)
        entry_cliente.grid(row=0, column=1, padx=10, pady=10)
        entry_cliente.insert(0, paquete_info[1])

        tk.Label(root, text="Distribuidor:").grid(row=1, column=0, padx=10, pady=10)
        entry_distribuidor = tk.Entry(root)
        entry_distribuidor.grid(row=1, column=1, padx=10, pady=10)
        entry_distribuidor.insert(0, paquete_info[2])

        def guardar_cambios():
            nuevo_cliente = entry_cliente.get()
            nuevo_distribuidor = entry_distribuidor.get()

            mydb = conectar_db()
            if mydb:
                cursor = mydb.cursor()
                cursor.execute(
                    "UPDATE paquetes SET Cliente = %s, Distribuidor = %s WHERE ID = %s",
                    (nuevo_cliente, nuevo_distribuidor, paquete_id)
                )
                mydb.commit()
                cursor.close()
                mydb.close()

                tree.item(selected_item, values=(
                    paquete_id,
                    nuevo_cliente,
                    nuevo_distribuidor,
                    paquete_info[3],
                    paquete_info[4],
                    paquete_info[5],
                    paquete_info[6],
                    paquete_info[7],
                    paquete_info[8]
                ))
                messagebox.showinfo("Éxito", "Datos actualizados con éxito")
                root.destroy()
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")

        btn_guardar = tk.Button(root, text="Guardar Cambios", command=guardar_cambios)
        btn_guardar.grid(row=2, column=0, columnspan=2, pady=10)
    else:
        messagebox.showerror("Error", "Seleccione un paquete para cambiar datos")

def cambiar_fase(tree):
    selected_item = tree.selection()
    if selected_item:
        paquete_info = tree.item(selected_item)["values"]
        paquete_id = paquete_info[0]

        root = tk.Toplevel()
        root.title("Cambiar Fase del Paquete")

        window_width = 300
        window_height = 150
        root.geometry(f"{window_width}x{window_height}")

        centrar_ventana(root, window_width, window_height)

        tk.Label(root, text="Nueva Fase:").grid(row=0, column=0, padx=10, pady=10)
        entry_fase = tk.Entry(root)
        entry_fase.grid(row=0, column=1, padx=10, pady=10)
        entry_fase.insert(0, paquete_info[4])

        def guardar_fase():
            nueva_fase = entry_fase.get()

            mydb = conectar_db()
            if mydb:
                cursor = mydb.cursor()
                cursor.execute("UPDATE paquetes SET Fase = %s WHERE ID = %s", (nueva_fase, paquete_id))
                mydb.commit()
                cursor.close()
                mydb.close()

                tree.item(selected_item, values=(
                    paquete_id,
                    paquete_info[1],
                    paquete_info[2],
                    paquete_info[3],
                    nueva_fase,
                    paquete_info[5],
                    paquete_info[6],
                    paquete_info[7],
                    paquete_info[8]
                ))
                messagebox.showinfo("Éxito", "Fase actualizada con éxito")
                root.destroy()
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")

        btn_guardar = tk.Button(root, text="Guardar Cambios", command=guardar_fase)
        btn_guardar.grid(row=1, column=0, columnspan=2, pady=10)
    else:
        messagebox.showerror("Error", "Seleccione un paquete para cambiar fase")

def cambiar_fechas(tree):
    selected_item = tree.selection()
    if selected_item:
        paquete_info = tree.item(selected_item)["values"]
        paquete_id = paquete_info[0]

        root = tk.Toplevel()
        root.title("Cambiar Fechas y Horarios del Paquete")

        window_width = 300
        window_height = 250
        root.geometry(f"{window_width}x{window_height}")

        centrar_ventana(root, window_width, window_height)

        tk.Label(root, text="Fecha de Salida (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
        entry_fecha_salida = tk.Entry(root)
        entry_fecha_salida.grid(row=0, column=1, padx=10, pady=10)
        entry_fecha_salida.insert(0, paquete_info[5])

        tk.Label(root, text="Hora de Salida (HH:MM):").grid(row=1, column=0, padx=10, pady=10)
        entry_hora_salida = tk.Entry(root)
        entry_hora_salida.grid(row=1, column=1, padx=10, pady=10)
        entry_hora_salida.insert(0, paquete_info[6])

        tk.Label(root, text="Fecha de Llegada (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=10)
        entry_fecha_llegada = tk.Entry(root)
        entry_fecha_llegada.grid(row=2, column=1, padx=10, pady=10)
        entry_fecha_llegada.insert(0, paquete_info[7])

        tk.Label(root, text="Hora de Llegada (HH:MM):").grid(row=3, column=0, padx=10, pady=10)
        entry_hora_llegada = tk.Entry(root)
        entry_hora_llegada.grid(row=3, column=1, padx=10, pady=10)
        entry_hora_llegada.insert(0, paquete_info[8])

        def guardar_fechas():
            nueva_fecha_salida = entry_fecha_salida.get()
            nueva_hora_salida = entry_hora_salida.get()
            nueva_fecha_llegada = entry_fecha_llegada.get()
            nueva_hora_llegada = entry_hora_llegada.get()

            mydb = conectar_db()
            if mydb:
                cursor = mydb.cursor()
                cursor.execute(
                    "UPDATE paquetes SET Fecha_Salida = %s, Hora_Salida = %s, Fecha_Llegada = %s, Hora_Llegada = %s WHERE ID = %s",
                    (nueva_fecha_salida, nueva_hora_salida, nueva_fecha_llegada, nueva_hora_llegada, paquete_id)
                )
                mydb.commit()
                cursor.close()
                mydb.close()

                tree.item(selected_item, values=(
                    paquete_id,
                    paquete_info[1],
                    paquete_info[2],
                    paquete_info[3],
                    paquete_info[4],
                    nueva_fecha_salida,
                    nueva_hora_salida,
                    nueva_fecha_llegada,
                    nueva_hora_llegada
                ))
                messagebox.showinfo("Éxito", "Fechas y horarios actualizados con éxito")
                root.destroy()
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")

        btn_guardar = tk.Button(root, text="Guardar Cambios", command=guardar_fechas)
        btn_guardar.grid(row=4, column=0, columnspan=2, pady=10)
    else:
        messagebox.showerror("Error", "Seleccione un paquete para cambiar fechas y horarios")

def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")