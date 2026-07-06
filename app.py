from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# İzlenecek ağlar ve güncellenmiş RPC adresleri
# DİKKAT: "SUNUCU_IP_ADRESINIZ" yazan kısımlara kendi sunucu IP'nizi yazmalısınız.
NETWORKS = [
    {"name": "Gno.land Test13", "type": "tendermint", "url": "http://SUNUCU_IP_ADRESINIZ:26657"},
    {"name": "0G Labs", "type": "tendermint", "url": "http://SUNUCU_IP_ADRESINIZ:26657"},
    {"name": "NEAR Protocol", "type": "jsonrpc", "url": "https://rpc.mainnet.near.org"},
    {"name": "Safrochain", "type": "tendermint", "url": "http://SUNUCU_IP_ADRESINIZ:26657"}
]

def check_status():
    results = []
    for net in NETWORKS:
        node_data = {"name": net["name"], "status": "Offline", "height": "-", "catching_up": "-"}
        try:
            if net["type"] == "tendermint":
                resp = requests.get(f"{net['url']}/status", timeout=5) # Timeout süresini bulut için 5 sn yaptık
                if resp.status_code == 200:
                    data = resp.json()
                    node_data["status"] = "Online"
                    node_data["height"] = data["result"]["sync_info"]["latest_block_height"]
                    node_data["catching_up"] = str(data["result"]["sync_info"]["catching_up"])
            elif net["type"] == "jsonrpc":
                payload = {"jsonrpc": "2.0", "id": "dontcare", "method": "status", "params": []}
                resp = requests.post(net["url"], json=payload, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    node_data["status"] = "Online"
                    node_data["height"] = data.get("sync_info", {}).get("latest_block_height", "Active")
                    node_data["catching_up"] = "False"
        except Exception:
            pass
        results.append(node_data)
    return results

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def status():
    return jsonify(check_status())

# Vercel'in uygulamayı bulabilmesi için gerekli app değişkeni
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
