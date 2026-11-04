import os
import sys
import unittest
import json
import sqlite3
import tempfile
import shutil

# Add project root to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import server.app as app_module
from server.init_db import init_database


class ServerEndpointsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.test_db = os.path.join(cls.temp_dir, "test_game.db")
        init_database(cls.test_db)
        app_module.DB_PATH = cls.test_db
        cls.client = app_module.app.test_client()
        cls.secret_key = "1FxquuRi8mn3UCrU182e"

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def test_01_index(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Kim Bir Milyon", res.data)

    def test_02_login_google_unknown(self):
        res = self.client.post('/kbi/Logingoogle.php', data={
            "secretKey": self.secret_key,
            "usernamePost": "non_existent_user_12345"
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data.decode(), "kullaniciyok")

    def test_03_create_and_login_google(self):
        # Create user
        res = self.client.post('/kbi/Creategoogle.php', data={
            "secretKey": self.secret_key,
            "usernamePost": "test_gamer_1",
            "adiPost": "Test",
            "soyadiPost": "OYUNCU",
            "cinsiyetPost": "Erkek",
            "ResimPost": ""
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data.decode())
        self.assertIn("LoadData", data)
        self.assertEqual(data["LoadData"][0]["isim"], "Test")
        self.assertEqual(data["LoadData"][0]["soyisim"], "OYUNCU")

        # Now login should return user data
        res_login = self.client.post('/kbi/Logingoogle.php', data={
            "secretKey": self.secret_key,
            "usernamePost": "test_gamer_1"
        })
        self.assertEqual(res_login.status_code, 200)
        login_data = json.loads(res_login.data.decode())
        self.assertEqual(login_data["LoadData"][0]["isim"], "Test")
        self.assertEqual(login_data["LoadData"][0]["skor"], "0")

    def test_04_encok_kazananlar(self):
        res = self.client.post('/kbi/EncokKazananlar.php', data={
            "secretKey": self.secret_key
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data.decode())
        self.assertIn("LoadData", data)
        self.assertGreater(len(data["LoadData"]), 0)
        # Check required fields
        first = data["LoadData"][0]
        self.assertIn("isim", first)
        self.assertIn("soyisim", first)
        self.assertIn("cinsiyet", first)
        self.assertIn("skor", first)
        self.assertIn("resim", first)

    def test_05_sorular_endpoints(self):
        for endpoint in ['/kbi/DusukSorular.php', '/kbi/OrtaSorular.php', '/kbi/UstSorular.php']:
            with self.subTest(endpoint=endpoint):
                res = self.client.post(endpoint, data={"secretKey": self.secret_key})
                self.assertEqual(res.status_code, 200)
                data = json.loads(res.data.decode())
                self.assertIn("LoadData", data)
                self.assertGreaterEqual(len(data["LoadData"]), 5)
                q = data["LoadData"][0]
                self.assertIn("Soru", q)
                self.assertIn("DogruCevap", q)
                self.assertIn("Cevap", q)
                self.assertIn("Cevap2", q)
                self.assertIn("Cevap3", q)

    def test_06_kazanc_and_update(self):
        username = "kazanc_test_user"
        # Register user first
        self.client.post('/kbi/Creategoogle.php', data={
            "secretKey": self.secret_key,
            "usernamePost": username,
            "adiPost": "Kazanan",
            "soyadiPost": "KİŞİ",
            "cinsiyetPost": "Erkek",
            "ResimPost": ""
        })

        # Query initial earnings
        res = self.client.post('/kbi/Kazanc.php', data={
            "secretKey": self.secret_key,
            "uidPost": username
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(res.data.decode()), 0)

        # Update earnings
        update_res = self.client.post('/kbi/Update_Kazanc.php', data={
            "secretKey": self.secret_key,
            "usernamePost": username,
            "skorPost": "15000"
        })
        self.assertEqual(update_res.status_code, 200)
        self.assertEqual(update_res.data.decode(), "basarili")

        # Query updated earnings
        res_after = self.client.post('/kbi/Kazanc.php', data={
            "secretKey": self.secret_key,
            "uidPost": username
        })
        self.assertEqual(res_after.status_code, 200)
        self.assertEqual(int(res_after.data.decode()), 15000)

    def test_07_update_resim(self):
        username = "resim_test_user"
        self.client.post('/kbi/Creategoogle.php', data={
            "secretKey": self.secret_key,
            "usernamePost": username,
            "adiPost": "Resim",
            "soyadiPost": "KULLANICI",
            "cinsiyetPost": "Kadin",
            "ResimPost": ""
        })

        res = self.client.post('/kbi/Update_Resim.php', data={
            "secretKey": self.secret_key,
            "usernamePost": username,
            "ResimPost": "http://example.com/avatar.png"
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data.decode(), "basarili")


if __name__ == '__main__':
    unittest.main()
