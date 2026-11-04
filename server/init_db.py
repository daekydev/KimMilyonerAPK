import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kbi_game.db')

# Sorular: Seviye 1-4 (Dusuk), Seviye 5-8 (Orta), Seviye 9-12 (Ust)
DUSUK_SORULAR = [
    {
        "Soru": "Türkiye'nin başkenti neresidir?",
        "DogruCevap": "Ankara",
        "Cevap": "İstanbul",
        "Cevap2": "İzmir",
        "Cevap3": "Bursa"
    },
    {
        "Soru": "Hangisi bir kış mevsimi ayıdır?",
        "DogruCevap": "Ocak",
        "Cevap": "Temmuz",
        "Cevap2": "Ağustos",
        "Cevap3": "Eylül"
    },
    {
        "Soru": "Trafik ışıklarında 'Geç' anlamına gelen renk hangisidir?",
        "DogruCevap": "Yeşil",
        "Cevap": "Kırmızı",
        "Cevap2": "Sarı",
        "Cevap3": "Mavi"
    },
    {
        "Soru": "Bir haftada kaç gün vardır?",
        "DogruCevap": "7",
        "Cevap": "5",
        "Cevap2": "6",
        "Cevap3": "8"
    },
    {
        "Soru": "Güneş sistemindeki en büyük gezegen hangisidir?",
        "DogruCevap": "Jüpiter",
        "Cevap": "Mars",
        "Cevap2": "Venüs",
        "Cevap3": "Satürn"
    },
    {
        "Soru": "Futbol maçlarında bir takım sahada kaç kişiyle mücadele eder?",
        "DogruCevap": "11",
        "Cevap": "10",
        "Cevap2": "12",
        "Cevap3": "9"
    },
    {
        "Soru": "Hangisi geleneksel bir Türk tatlısıdır?",
        "DogruCevap": "Baklava",
        "Cevap": "Tiramisu",
        "Cevap2": "Kruvasan",
        "Cevap3": "Waffle"
    },
    {
        "Soru": "Suyun donma noktası kaç santigrat derecedir?",
        "DogruCevap": "0",
        "Cevap": "10",
        "Cevap2": "-5",
        "Cevap3": "100"
    },
    {
        "Soru": "İstiklal Marşı'mızın şairi kimdir?",
        "DogruCevap": "Mehmet Akif Ersoy",
        "Cevap": "Yahya Kemal Beyatlı",
        "Cevap2": "Namık Kemal",
        "Cevap3": "Necip Fazıl Kısakürek"
    },
    {
        "Soru": "Hangi hayvan 'çöl gemisi' olarak da adlandırılır?",
        "DogruCevap": "Deve",
        "Cevap": "At",
        "Cevap2": "Fil",
        "Cevap3": "Eşek"
    },
    {
        "Soru": "Dünyanın uydusu hangisidir?",
        "DogruCevap": "Ay",
        "Cevap": "Güneş",
        "Cevap2": "Mars",
        "Cevap3": "Venüs"
    },
    {
        "Soru": "Türk alfabesinde kaç harf vardır?",
        "DogruCevap": "29",
        "Cevap": "28",
        "Cevap2": "30",
        "Cevap3": "32"
    }
]

ORTA_SORULAR = [
    {
        "Soru": "Fatih Sultan Mehmet İstanbul'u hangi yılda fethetmiştir?",
        "DogruCevap": "1453",
        "Cevap": "1071",
        "Cevap2": "1299",
        "Cevap3": "1517"
    },
    {
        "Soru": "Periyodik tabloda 'Au' sembolü hangi elementi simgeler?",
        "DogruCevap": "Altın",
        "Cevap": "Gümüş",
        "Cevap2": "Bakır",
        "Cevap3": "Alüminyum"
    },
    {
        "Soru": "Mona Lisa tablosu hangi ünlü ressama aittir?",
        "DogruCevap": "Leonardo da Vinci",
        "Cevap": "Pablo Picasso",
        "Cevap2": "Vincent van Gogh",
        "Cevap3": "Michelangelo"
    },
    {
        "Soru": "Dünyanın en uzun nehri kabul edilen nehir hangisidir?",
        "DogruCevap": "Nil",
        "Cevap": "Amazon",
        "Cevap2": "Tuna",
        "Cevap3": "Fırat"
    },
    {
        "Soru": "Pusulada 'N' harfi hangi yönü gösterir?",
        "DogruCevap": "Kuzey",
        "Cevap": "Güney",
        "Cevap2": "Doğu",
        "Cevap3": "Batı"
    },
    {
        "Soru": "Cumhuriyet hangi yıl ilan edilmiştir?",
        "DogruCevap": "1923",
        "Cevap": "1919",
        "Cevap2": "1920",
        "Cevap3": "1922"
    },
    {
        "Soru": "Yerçekimi kanununu bulan ünlü bilim insanı kimdir?",
        "DogruCevap": "Isaac Newton",
        "Cevap": "Albert Einstein",
        "Cevap2": "Galileo Galilei",
        "Cevap3": "Nikola Tesla"
    },
    {
        "Soru": "İtalya'nın başkenti neresidir?",
        "DogruCevap": "Roma",
        "Cevap": "Milano",
        "Cevap2": "Venedik",
        "Cevap3": "Floransa"
    },
    {
        "Soru": "Hücrenin enerji santrali olarak bilinen organel hangisidir?",
        "DogruCevap": "Mitokondri",
        "Cevap": "Ribozom",
        "Cevap2": "Kloroplast",
        "Cevap3": "Lizozom"
    },
    {
        "Soru": "Bir dik üçgende dik kenarları birleştiren en uzun kenara ne ad verilir?",
        "DogruCevap": "Hipotenüs",
        "Cevap": "Çap",
        "Cevap2": "Yarıçap",
        "Cevap3": "Kiriş"
    }
]

UST_SORULAR = [
    {
        "Soru": "Nobel Edebiyat Ödülü'nü kazanan ilk Türk yazar kimdir?",
        "DogruCevap": "Orhan Pamuk",
        "Cevap": "Yaşar Kemal",
        "Cevap2": "Nazım Hikmet",
        "Cevap3": "Aziz Nesin"
    },
    {
        "Soru": "Dante'nin ünlü eseri 'İlahi Komedya' hangi dilde yazılmıştır?",
        "DogruCevap": "İtalyanca",
        "Cevap": "Latince",
        "Cevap2": "Fransızca",
        "Cevap3": "Grekçe"
    },
    {
        "Soru": "Dünyanın en derin noktası olan Mariana Çukuru hangi okyanustadır?",
        "DogruCevap": "Büyük Okyanus",
        "Cevap": "Atlas Okyanusu",
        "Cevap2": "Hint Okyanusu",
        "Cevap3": "Arktik Okyanusu"
    },
    {
        "Soru": "DNA'nın çift sarmal yapısını 1953 yılında keşfeden ikili kimdir?",
        "DogruCevap": "Watson ve Crick",
        "Cevap": "Pasteur ve Koch",
        "Cevap2": "Bohr ve Rutherford",
        "Cevap3": "Darwin ve Wallace"
    },
    {
        "Soru": "Osmanlı Devleti'nde ilk matbaayı kuran kişi kimdir?",
        "DogruCevap": "İbrahim Müteferrika",
        "Cevap": "Katip Çelebi",
        "Cevap2": "Evliya Çelebi",
        "Cevap3": "Piri Reis"
    },
    {
        "Soru": "Işık hızının saniyedeki yaklaşık değeri ne kadardır?",
        "DogruCevap": "300.000 km",
        "Cevap": "150.000 km",
        "Cevap2": "500.000 km",
        "Cevap3": "1.000.000 km"
    },
    {
        "Soru": "İlk modern olimpiyat oyunları 1896 yılında nerede düzenlenmiştir?",
        "DogruCevap": "Atina",
        "Cevap": "Paris",
        "Cevap2": "Londra",
        "Cevap3": "Roma"
    },
    {
        "Soru": "Türkiye Cumhuriyeti'nin ilk Başbakanı kimdir?",
        "DogruCevap": "İsmet İnönü",
        "Cevap": "Fevzi Çakmak",
        "Cevap2": "Celal Bayar",
        "Cevap3": "Kazım Karabekir"
    }
]

VARSAYILAN_KULLANICILAR = [
    ("ali_yilmaz", "Ali", "YILMAZ", "Erkek", 1000000, ""),
    ("ayse_kaya", "Ayşe", "KAYA", "Kadin", 750000, ""),
    ("mehmet_demir", "Mehmet", "DEMİR", "Erkek", 500000, ""),
    ("fatma_celik", "Fatma", "ÇELİK", "Kadin", 350000, ""),
    ("can_ozturk", "Can", "ÖZTÜRK", "Erkek", 250000, ""),
    ("elif_sahin", "Elif", "ŞAHİN", "Kadin", 125000, ""),
    ("burak_aydin", "Burak", "AYDIN", "Erkek", 60000, ""),
    ("zeynep_yildiz", "Zeynep", "YILDIZ", "Kadin", 35000, ""),
    ("emre_koc", "Emre", "KOÇ", "Erkek", 15000, ""),
    ("selin_arslan", "Selin", "ARSLAN", "Kadin", 7500, ""),
    ("kemal_polat", "Kemal", "POLAT", "Erkek", 5000, ""),
    ("busra_kara", "Büşra", "KARA", "Kadin", 1000, "")
]


def init_database(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            isim TEXT NOT NULL,
            soyisim TEXT NOT NULL,
            cinsiyet TEXT NOT NULL,
            skor INTEGER DEFAULT 0,
            resim TEXT DEFAULT ''
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL, -- 'dusuk', 'orta', 'ust'
            soru TEXT NOT NULL,
            dogru_cevap TEXT NOT NULL,
            cevap TEXT NOT NULL,
            cevap2 TEXT NOT NULL,
            cevap3 TEXT NOT NULL
        )
    ''')

    # Kullanıcıları ekle
    for u in VARSAYILAN_KULLANICILAR:
        cur.execute('''
            INSERT OR IGNORE INTO users (username, isim, soyisim, cinsiyet, skor, resim)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', u)

    # Soruları ekle (temizleyip yeniden ekleme kontrolü)
    cur.execute('DELETE FROM questions')
    for q in DUSUK_SORULAR:
        cur.execute('''
            INSERT INTO questions (category, soru, dogru_cevap, cevap, cevap2, cevap3)
            VALUES ('dusuk', ?, ?, ?, ?, ?)
        ''', (q['Soru'], q['DogruCevap'], q['Cevap'], q['Cevap2'], q['Cevap3']))

    for q in ORTA_SORULAR:
        cur.execute('''
            INSERT INTO questions (category, soru, dogru_cevap, cevap, cevap2, cevap3)
            VALUES ('orta', ?, ?, ?, ?, ?)
        ''', (q['Soru'], q['DogruCevap'], q['Cevap'], q['Cevap2'], q['Cevap3']))

    for q in UST_SORULAR:
        cur.execute('''
            INSERT INTO questions (category, soru, dogru_cevap, cevap, cevap2, cevap3)
            VALUES ('ust', ?, ?, ?, ?, ?)
        ''', (q['Soru'], q['DogruCevap'], q['Cevap'], q['Cevap2'], q['Cevap3']))

    conn.commit()
    conn.close()
    print(f"Database initialized successfully at {db_path}!")


if __name__ == '__main__':
    init_database()
