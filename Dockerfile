FROM python:3-slim
RUN apt-get update -y && apt-get install nginx -y
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
COPY nginx.conf /etc/nginx/nginx.conf

ENTRYPOINT ["/app/entrypoint.sh"]
