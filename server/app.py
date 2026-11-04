import os
import json
import sqlite3
from flask import Flask, request, Response

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kbi_game.db')
VALID_SECRET_KEY = "1FxquuRi8mn3UCrU182e"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def check_secret_key(req):
    key = req.form.get("secretKey") or req.args.get("secretKey")
    # For safety with legacy game versions, if key is provided check it
    if key and key != VALID_SECRET_KEY:
        return False
    return True


@app.route('/', methods=['GET'])
def index():
    return "Kim Bir Milyon İster? Game Server is running."


# 1. Logingoogle.php
# POST form fields: secretKey, usernamePost
# Returns:
# - "kullaniciyok" if user doesn't exist
# - JSON {"LoadData": [{"isim": "...", "soyisim": "...", "cinsiyet": "...", "skor": "..."}]}
@app.route('/kbi/Logingoogle.php', methods=['GET', 'POST'])
def login_google():
    if not check_secret_key(request):
        return "yetkisiz", 403

    username = request.form.get("usernamePost") or request.args.get("usernamePost")
    if not username:
        return "kullaniciyok", 200

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT isim, soyisim, cinsiyet, skor FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return "kullaniciyok", 200

    data = {
        "LoadData": [
            {
                "isim": row["isim"],
                "soyisim": row["soyisim"],
                "cinsiyet": row["cinsiyet"],
                "skor": str(row["skor"])
            }
        ]
    }
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')


# 2. Creategoogle.php
# POST form fields: secretKey, usernamePost, adiPost, soyadiPost, cinsiyetPost, ResimPost
# Returns:
# - "kullaniciyok" or JSON {"LoadData": [{"isim": "...", "soyisim": "...", "cinsiyet": "..."}]}
@app.route('/kbi/Creategoogle.php', methods=['GET', 'POST'])
def create_google():
    if not check_secret_key(request):
        return "yetkisiz", 403

    username = request.form.get("usernamePost") or request.args.get("usernamePost")
    adi = request.form.get("adiPost") or request.args.get("adiPost") or "Misafir"
    soyadi = request.form.get("soyadiPost") or request.args.get("soyadiPost") or ""
    cinsiyet = request.form.get("cinsiyetPost") or request.args.get("cinsiyetPost") or "Erkek"
    resim = request.form.get("ResimPost") or request.args.get("ResimPost") or ""

    if not username:
        return "kullaniciyok", 200

    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO users (username, isim, soyisim, cinsiyet, skor, resim)
        VALUES (?, ?, ?, ?, 0, ?)
        ON CONFLICT(username) DO UPDATE SET
            isim = excluded.isim,
            soyisim = excluded.soyisim,
            cinsiyet = excluded.cinsiyet,
            resim = CASE WHEN excluded.resim != '' THEN excluded.resim ELSE users.resim END
    ''', (username, adi, soyadi, cinsiyet, resim))
    conn.commit()

    cur.execute("SELECT isim, soyisim, cinsiyet, skor FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()

    data = {
        "LoadData": [
            {
                "isim": row["isim"],
                "soyisim": row["soyisim"],
                "cinsiyet": row["cinsiyet"],
                "skor": str(row["skor"])
            }
        ]
    }
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')


# 3. EncokKazananlar.php
# POST form fields: secretKey
# Returns JSON:
# {"LoadData": [{"isim": "...", "soyisim": "...", "cinsiyet": "...", "skor": "...", "resim": "..."}, ...]}
@app.route('/kbi/EncokKazananlar.php', methods=['GET', 'POST'])
def encok_kazananlar():
    if not check_secret_key(request):
        return "yetkisiz", 403

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT isim, soyisim, cinsiyet, skor, resim FROM users ORDER BY skor DESC LIMIT 12")
    rows = cur.fetchall()
    conn.close()

    items = []
    for r in rows:
        items.append({
            "isim": r["isim"],
            "soyisim": r["soyisim"],
            "cinsiyet": r["cinsiyet"],
            "skor": str(r["skor"]),
            "resim": r["resim"] or ""
        })

    data = {"LoadData": items}
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')


# 4. DusukSorular.php
# Returns JSON:
# {"LoadData": [{"Soru": "...", "DogruCevap": "...", "Cevap": "...", "Cevap2": "...", "Cevap3": "..."}, ...]}
@app.route('/kbi/DusukSorular.php', methods=['GET', 'POST'])
def dusuk_sorular():
    if not check_secret_key(request):
        return "yetkisiz", 403

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT soru, dogru_cevap, cevap, cevap2, cevap3 FROM questions WHERE category = 'dusuk'")
    rows = cur.fetchall()
    conn.close()

    items = []
    for r in rows:
        items.append({
            "Soru": r["soru"],
            "DogruCevap": r["dogru_cevap"],
            "Cevap": r["cevap"],
            "Cevap2": r["cevap2"],
            "Cevap3": r["cevap3"]
        })

    data = {"LoadData": items}
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')


# 5. OrtaSorular.php
@app.route('/kbi/OrtaSorular.php', methods=['GET', 'POST'])
def orta_sorular():
    if not check_secret_key(request):
        return "yetkisiz", 403

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT soru, dogru_cevap, cevap, cevap2, cevap3 FROM questions WHERE category = 'orta'")
    rows = cur.fetchall()
    conn.close()

    items = []
    for r in rows:
        items.append({
            "Soru": r["soru"],
            "DogruCevap": r["dogru_cevap"],
            "Cevap": r["cevap"],
            "Cevap2": r["cevap2"],
            "Cevap3": r["cevap3"]
        })

    data = {"LoadData": items}
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')


# 6. UstSorular.php
@app.route('/kbi/UstSorular.php', methods=['GET', 'POST'])
def ust_sorular():
    if not check_secret_key(request):
        return "yetkisiz", 403

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT soru, dogru_cevap, cevap, cevap2, cevap3 FROM questions WHERE category = 'ust'")
    rows = cur.fetchall()
    conn.close()

    items = []
    for r in rows:
        items.append({
            "Soru": r["soru"],
            "DogruCevap": r["dogru_cevap"],
            "Cevap": r["cevap"],
            "Cevap2": r["cevap2"],
            "Cevap3": r["cevap3"]
        })

    data = {"LoadData": items}
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')


# 7. Kazanc.php
# POST form fields: secretKey, uidPost
# Returns:
# - "kullaniciyok" if user doesn't exist
# - string number e.g. "50000" (which client parses using int.Parse(www.text))
@app.route('/kbi/Kazanc.php', methods=['GET', 'POST'])
def kazanc_cek():
    if not check_secret_key(request):
        return "yetkisiz", 403

    uid = request.form.get("uidPost") or request.args.get("uidPost")
    if not uid:
        return "kullaniciyok", 200

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT skor FROM users WHERE username = ?", (uid,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return "kullaniciyok", 200

    return str(row["skor"]), 200


# 8. Update_Kazanc.php
# POST form fields: secretKey, usernamePost, skorPost
# Updates user's score (adding or setting max score)
@app.route('/kbi/Update_Kazanc.php', methods=['GET', 'POST'])
def update_kazanc():
    if not check_secret_key(request):
        return "yetkisiz", 403

    username = request.form.get("usernamePost") or request.args.get("usernamePost")
    skor_str = request.form.get("skorPost") or request.args.get("skorPost") or "0"

    try:
        skor = int(skor_str)
    except ValueError:
        skor = 0

    if not username:
        return "hatali_kullanici", 400

    conn = get_db()
    cur = conn.cursor()
    # If user exists, increase total earnings or update max
    cur.execute("SELECT skor FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    if row:
        new_skor = row["skor"] + skor
        cur.execute("UPDATE users SET skor = ? WHERE username = ?", (new_skor, username))
    else:
        cur.execute("INSERT INTO users (username, isim, soyisim, cinsiyet, skor) VALUES (?, ?, ?, ?, ?)",
                    (username, username, "", "Erkek", skor))
    conn.commit()
    conn.close()

    return "basarili", 200


# 9. Update_Resim.php
# POST form fields: secretKey, usernamePost, ResimPost
@app.route('/kbi/Update_Resim.php', methods=['GET', 'POST'])
def update_resim():
    if not check_secret_key(request):
        return "yetkisiz", 403

    username = request.form.get("usernamePost") or request.args.get("usernamePost")
    resim = request.form.get("ResimPost") or request.args.get("ResimPost") or ""

    if not username:
        return "hatali_kullanici", 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET resim = ? WHERE username = ?", (resim, username))
    conn.commit()
    conn.close()

    return "basarili", 200


if __name__ == '__main__':
    # Initialize DB if not present
    if not os.path.exists(DB_PATH):
        from init_db import init_database
        init_database(DB_PATH)

    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    print(f"Starting server on {host}:{port}...")
    app.run(host=host, port=port, debug=False)
