FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y git && apt-get clean
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app app
EXPOSE 8000
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]