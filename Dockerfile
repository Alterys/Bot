FROM ubuntu:latest
FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./bot.py"]
LABEL authors="altery"

ENTRYPOINT ["top", "-b"]