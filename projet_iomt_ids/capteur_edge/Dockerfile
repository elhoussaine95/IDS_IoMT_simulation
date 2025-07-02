FROM python:3.9-slim
WORKDIR /app
COPY capteur.py Edge-IIoT.csv ./
RUN pip install pandas
CMD ["python", "capteur.py"]
