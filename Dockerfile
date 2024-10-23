FROM python:3.9-slim

WORKDIR /

# Install system-level dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy and install Python dependencies

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]