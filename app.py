from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# ZeycaNode Multi-Chain Infrastructure - Güncel ve Kesin Portlar
NETWORKS = [
    # 185.16.39.172 Sunucusu
    {"name": "Gno.land Test13", "type": "tendermint", "url": "http://185.16.39.172:26657"},
    {"name": "Safrochain Mainnet", "type": "tendermint", "url": "http://185.16.39.172:26658"},
    
    # 13.140.137.185 Sunucusu 
    {"name": "Safrochain Testnet", "type": "tendermint", "url": "http://13.140.137.185:26657"},
    
    # 164.68.123.138 Sunucusu (Terminalden teyit edilen kesin portlar)
    {"name": "Airchains", "type": "tendermint", "url": "http://164.68.123.138:19657"},
    {"name": "Republic", "type": "tendermint", "url": "http://164.68.123.138:13357"},
    {"name": "0G AI Alignment Node", "type": "jsonrpc", "url": "http://164.68.123.138:8080"},
    
    # Dış Bağlantılar
    {"name": "NEAR Protocol", "type": "jsonrpc", "url": "https://rpc.mainnet.near.org"}
]

def check_status():
    results = []
    for net in NETWORKS:
        node_data = {"name": net["name"], "status": "Offline", "height": "-", "catching_up": "-"}
        try:
            if net["type"] == "tendermint":
                # Cosmos/Tendermint tabanlı ağlar için RPC /status sorgusu
                resp = requests.get(f"{net['url']}/status", timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    node_data["status"] = "Online"
                    node_data["height"] = data["result"]["sync_info"]["latest_block_height"]
                    node_data["catching_up"] = str(data["result"]["sync_info"]["catching_up"])
            
            elif net["type"] == "jsonrpc":
                # EVM, NEAR veya 0G gibi JSON-RPC kullanan ağlar için sorgu
                payload = {"jsonrpc": "2.0", "id": "dontcare", "method": "status", "params": []}
                resp = requests.post(net["url"], json=payload, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    node_data["status"] = "Online"
                    
                    # Farklı ağların JSON-RPC yanıt formatları değişebildiği için güvenli okuma
                    if "sync_info" in data:
                        node_data["height"] = data.get("sync_info", {}).get("latest_block_height", "Active")
                        node_data["catching_up"] = str(data.get("sync_info", {}).get("catching_up", "False"))
                    else:
