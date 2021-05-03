FROM python:3-alpine
RUN apk add --no-cache nginx gcc
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["/app/entrypoint.sh"]
