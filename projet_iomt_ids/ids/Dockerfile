FROM python:3.9-slim

# Crée un dossier de travail
WORKDIR /app

# Copier les scripts, modèles et le fichier requirements.txt
COPY serveur.py model.py ./  
COPY model_iomt.pth model_iotid.pth model_edge.pth ./  
COPY requirements.txt ./

# Installer les dépendances à partir du fichier
RUN pip install --no-cache-dir -r requirements.txt

# Lancer le serveur IDS
CMD ["python", "serveur.py"]
