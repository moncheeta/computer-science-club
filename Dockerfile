FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/
COPY . /app/

RUN pip install --no-cache-dir \
  gunicorn \
  flask \
  schoolopy \
  cachecontrol \
  google-auth \
  google_auth_oauthlib

ENV PATH="/app/venv/bin:$PATH"

EXPOSE 80

CMD ["gunicorn", "-b", "0.0.0.0:80", "main:app"]
