from flask import Flask, render_template_string, request, jsonify
import json
import os

app = Flask(__name__)
DB_FILE = "aquarium_data.json"

# HTML Design (Same wahi jo aapko pasand aaya tha)
html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Golden Fish Aquarium</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #e0f7fa; text-align: center; margin: 0; padding: 10px; }
        .container { background-color: #fff; border-radius: 15px; padding: 20px; max-width: 600px; margin: auto; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        h1 { color: #00acc1; }
        .save-btn { background: #4CAF50; color: white; border: none; padding: 15px; width: 100%; border-radius: 25px; font-weight: bold; margin: 20px 0; cursor: pointer; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 15px; }
        .card { background: #f1f8e9; border-radius: 10px; padding: 10px; border: 1px solid #c5e1a5; }
        .card img { width: 100%; height: 120px; object-fit: cover; border-radius: 8px; }
        input { width: 90%; margin-top: 5px; text-align: center; border: 1px solid #ccc; border-radius: 4px; }
        .price { color: #d84315; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐟 The Golden Fish Aquarium 🐠</h1>
        <button onclick="saveData()" class="save-btn" id="sBtn">💾 Sab Save Karein (Duniya bhar ke liye)</button>
        <div class="grid" id="g"></div>
        <p>📍 Location: Madiyahun, Jaunpur</p>
    </div>
    <script>
        const g = document.getElementById('g');
        for(let i=1; i<=15; i++) {
            g.innerHTML += `<div class="card">
                <label><img id="v${i}" src="https://via.placeholder.com/150?text=Add+Photo">
                <input type="file" style="display:none" onchange="p(event, ${i})"></label>
                <input type="text" id="n${i}" placeholder="Naam">
                <input type="text" id="p${i}" class="price" placeholder="Daam">
            </div>`;
        }

        function p(e, i) {
            const r = new FileReader();
            r.onload = (x) => document.getElementById('v'+i).src = x.target.result;
            r.readAsDataURL(e.target.files[0]);
        }

        async function saveData() {
            document.getElementById('sBtn').innerText = "⏳ Saving...";
            let d = {};
            for(let i=1; i<=15; i++) {
                d[i] = { i: document.getElementById('v'+i).src, n: document.getElementById('n'+i).value, p: document.getElementById('p'+i).value };
            }
            await fetch('/save', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(d) });
            document.getElementById('sBtn').innerText = "✅ Saved!";
        }

        fetch('/load').then(r => r.json()).then(d => {
            for(let i in d) {
                document.getElementById('v'+i).src = d[i].i;
                document.getElementById('n'+i).value = d[i].n;
                document.getElementById('p'+i).value = d[i].p;
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_template)

@app.route('/save', methods=['POST'])
def save():
    with open(DB_FILE, 'w') as f:
        json.dump(request.json, f)
    return jsonify({"status": "ok"})

@app.route('/load')
def load():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return f.read()
    return jsonify({})

if __name__ == "__main__":
    app.run()
  
