import socket
import pandas as pd
import time 
SOURCE_ID = "iomt"
df = pd.read_csv("CICIoMT2024.csv") 
df = df.select_dtypes(include=["number"]).dropna()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connected = False
for attempt in range(10):
    try:
        client.connect(("ids", 12345))
        connected = True
        print("Connexion réussie à IDS.")
        client.sendall(SOURCE_ID.ljust(16).encode('utf-8'))
        break
    except ConnectionRefusedError:
        print(f"Tentative {attempt + 1}/10 : IDS pas prêt, attente de 1s...")
        time.sleep(1)

if not connected:
    raise Exception("Impossible de se connecter à IDS.")

# Envoi rapide sans pause
print("\n--- Envoi des données CICIOMT2024 ---")
for i in range(4):
    for _, row in df.iterrows():
        data = row.values.astype('float32').tobytes()
        client.sendall(data)
        time.sleep(0.02)
print("\n--- fin de transmission CICIOMT2024 ---")
time.sleep(2)  
client.close()
print("Connexion fermée CICIOMT2024.")
