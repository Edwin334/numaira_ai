# Build stage
FROM python:3.10-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.10-slim
WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
# Install uvicorn using -U to ensure it's in the PATH
RUN pip install -U uvicorn
COPY . .

EXPOSE 8000
CMD ["/usr/local/bin/uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]