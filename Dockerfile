FROM python:3.11-slim

# Install QuantLib C++ library FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends libquantlib0-dev g++ && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]from apt (this is what makes it work)
RUN apt-get update && \
    apt-get install -y --no-install-recommends libquantlib0-dev quantlib-tools g++ && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
