FROM python:3.11-slim

# Install build dependencies (GCC, make, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    make \
    && rm -rf /var/lib/apt/lists/*
    
ENV PYTHONUNBUFFERED=1 \
    WORKDIR=/

WORKDIR $WORKDIR

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
