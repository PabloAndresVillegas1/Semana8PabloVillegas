import unittest
from unittest.mock import patch, MagicMock
from gestion_compradores import obtener_compradores

class TestObtenerCompradores(unittest.TestCase):

    @patch('gestion_compradores.conectar_db') 
    def test_obtener_compradores(self, mock_conectar_db):
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar_db.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, 'Juan', 'Pérez', '12345678', '555-1234', 'Calle Falsa 123', 'juan@example.com'),
            (2, 'Ana', 'Gómez', '87654321', '555-5678', 'Avenida Siempre Viva 742', 'ana@example.com')
        ]

        compradores = obtener_compradores()
        self.assertEqual(len(compradores), 2)
        self.assertEqual(compradores[0], (1, 'Juan', 'Pérez', '12345678', '555-1234', 'Calle Falsa 123', 'juan@example.com'))
        self.assertEqual(compradores[1], (2, 'Ana', 'Gómez', '87654321', '555-5678', 'Avenida Siempre Viva 742', 'ana@example.com'))

if __name__ == '__main__':
    unittest.main()