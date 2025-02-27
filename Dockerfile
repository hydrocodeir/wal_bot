FROM python:3.11.8-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/src/start.sh

CMD ["/app/src/start.sh"]