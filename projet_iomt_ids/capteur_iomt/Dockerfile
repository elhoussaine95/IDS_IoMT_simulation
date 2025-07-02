FROM python:3.9-slim
WORKDIR /app
COPY capteur.py CICIoMT2024.csv ./
RUN pip install pandas
CMD ["python", "capteur.py"]
