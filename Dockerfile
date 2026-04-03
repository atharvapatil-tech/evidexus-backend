FROM python:3.11-slim

WORKDIR /app

# Upgrade pip and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Ensure non-root execution
RUN useradd -m evidexus && chown -R evidexus /app
USER evidexus

# Expose port (default 8000 if not set)
ENV PORT 8000
EXPOSE $PORT

# Start server
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
