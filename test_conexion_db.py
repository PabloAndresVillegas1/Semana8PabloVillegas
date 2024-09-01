import unittest
import mysql.connector
from mysql.connector import Error

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
        print(f"No se pudo conectar a la base de datos: {err}")
        return None

class TestConexionDB(unittest.TestCase):
    
    def test_conexion_exitosa(self):
        try:
            conexion = conectar_db()
            
            self.assertIsNotNone(conexion)
            self.assertTrue(conexion.is_connected())
        finally:
            if conexion and conexion.is_connected():
                conexion.close()
    
    def test_conexion_fallida(self):
        db_config_incorrecto = {
            'host': 'localhost',
            'user': 'usuario_incorrecto',
            'password': 'contraseña_incorrecta',
            'database': 'base_datos_incorrecta',
            'port': 20489
        }

        with self.assertRaises(Error):
            conexion = mysql.connector.connect(**db_config_incorrecto)
            
if __name__ == '__main__':
    unittest.main()
