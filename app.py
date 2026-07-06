from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Gno.land Halka Açık (Public) RPC Adresi
# Bu adres dışarıya açık olduğu için Vercel hiçbir engele takılmaz.
GNO_RPC_URL = "https://rpc.gno.land" 

def get_validators():
    try:
        # Halka açık ağdan aktif validatör setini çekiyoruz (ilk 100 validatör)
        resp = requests.get(f"{GNO_RPC_URL}/validators?per_page=100", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            validators = data.get("result", {}).get("validators", [])
            
            # Validatörleri Voting Power (Oy Gücü) değerine göre sırala
            validators.sort(key=lambda x: int(x.get("voting_power", 0)), reverse=True)
            
            leaderboard = []
            for index, val in enumerate(validators):
                leaderboard.append({
                    "rank": index + 1,
                    "address": val.get("address", ""),
                    "voting_power": val.get("voting_power", "0"),
                    "proposer_priority": val.get("proposer_priority", "0")
                })
            return leaderboard
    except Exception as e:
        pass
    return []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/validators")
def validators():
    return jsonify(get_validators())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
