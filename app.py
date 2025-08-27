from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "data.json"

# Učitavanje podataka
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

# Čuvanje podataka
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route('/')
def home():
    pesme = load_data()
    # Provera parametra za sortiranje
    sort_by = request.args.get('sort', 'ocena')  # default: ocena
    if sort_by == 'ocena':
        pesme = sorted(pesme, key=lambda x: x['ocena'], reverse=True)
    elif sort_by == 'zanr':
        pesme = sorted(pesme, key=lambda x: x['zanr'])
    return render_template('index.html', pesme=pesme, current_sort=sort_by)

@app.route('/add', methods=['POST'])
def add_song():
    naziv = request.form.get('naziv')
    izvodjac = request.form.get('izvodjac')
    ocena = request.form.get('ocena')
    zanr = request.form.get('zanr')

    if naziv and izvodjac and ocena and zanr:
        try:
            ocena = int(ocena)
            if not (1 <= ocena <= 5):
                raise ValueError
        except:
            return jsonify({'status': 'error', 'message': 'Ocena mora biti broj od 1 do 5'})

        pesme = load_data()
        pesme.append({
            "naziv": naziv,
            "izvodjac": izvodjac,
            "ocena": ocena,
            "zanr": zanr,
            "datum": datetime.now().isoformat(),
            "favorit": False  # inicijalno False
        })
        save_data(pesme)
        return jsonify({'status': 'success', 'naziv': naziv})
    return jsonify({'status': 'error', 'message': 'Svi podaci su obavezni'})

# Nova ruta za favorit
@app.route('/favorite', methods=['POST'])
def favorite_song():
    naziv = request.form.get('naziv')
    pesme = load_data()
    for pesma in pesme:
        if pesma['naziv'] == naziv:
            pesma['favorit'] = not pesma.get('favorit', False)  # toggle
            break
    save_data(pesme)
    return jsonify({'status': 'success'})

if __name__ == "__main__":
    app.run(debug=True, port=3000)
