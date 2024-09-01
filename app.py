from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': 'bd-especializacion-comercializadoragremlins.g.aivencloud.com',
    'user': 'avnadmin',
    'password': 'AVNS_U0Rkp43qcL6pyg8qK0u',
    'database': 'defaultdb',
    'port': 20489
}

def obtener_compradores():
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM compradores")
        compradores = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return compradores
    except mysql.connector.Error as err:
        return {"error": str(err)}

@app.route('/compradores', methods=['GET'])
def get_compradores():
    compradores = obtener_compradores()
    return jsonify(compradores)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
