FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["sh", "-c", "sleep 5 && python init_db.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
