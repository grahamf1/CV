FROM python:3.12.3-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir wheel setuptools

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=cv
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production
ARG COSMOS_DB_CONNECTION_STRING
ENV AZURE_COSMOS_CONNECTION_STRING=$COSMOS_DB_CONNECTION_STRING

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "cv:app"]
