import socket
import torch
import numpy as np
import time
import statistics
import threading
from model import CNN_LSTM_Model


#==========================================

MODELS = {
    "iomt": "model_iomt.pth",
    "iotid": "model_iotid.pth",
    "edge": "model_edge.pth"
}

loaded_models = {}
for key, path in MODELS.items():
    try:
        model = CNN_LSTM_Model(input_size=1, hidden_size=256, num_layers=2, num_classes=2)
        model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
        model.eval()
        loaded_models[key] = model
        print(f"Modèle '{key}' chargé avec succès.")
    except Exception as e:
        print(f"Erreur de chargement du modèle '{key}' : {e}")

def handle_client(conn, addr):
    print(f"\nConnexion de {addr}")
    try:
        source_id = conn.recv(16).decode('utf-8').strip()
        print(f"Capteur identifié : {repr(source_id)}")

        if source_id not in loaded_models:
            print("Source inconnue. Connexion refusée.")
            conn.close()
            return

        model = loaded_models[source_id]
        latencies = []

        while True:
            data = conn.recv(4096)
            if not data:
                print("Fin de transmission.")
                break

            if len(data) % 4 != 0:
                print(f"Données corrompues ou incomplètes (taille = {len(data)}).")
                continue

            features = np.frombuffer(data, dtype=np.float32).reshape(1, -1)
            input_tensor = torch.tensor(features, dtype=torch.float32)

            start_time = time.time()
            with torch.no_grad():
                output = model(input_tensor)
                pred = torch.argmax(output, dim=1).item()
            end_time = time.time()

            latency_ms = (end_time - start_time) * 1000
            latencies.append(latency_ms)

            print("Attaque détectée" if pred == 1 else "Trafic normal")
            print(f"Latence : {latency_ms:.2f} ms")

    except Exception as e:
        print(f"Erreur avec {addr} : {e}")
        
    conn.close()
    print(f"Connexion fermée avec {addr}")
    
    if latencies:
        avg_latency = statistics.mean(latencies)
        std_latency = statistics.stdev(latencies) if len(latencies) > 1 else 0
        print(f"\nRésumé des performances pour {addr} :")
        print(f"   Latence moyenne : {avg_latency:.2f} ms")
        print(f"   Écart-type : {std_latency:.2f} ms")
        
# Serveur multi-client
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 12345))
server.listen(5)
print("Serveur IDS prêt. En attente de connexions...")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()

