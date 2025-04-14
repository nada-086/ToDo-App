# Stage 1: Building the Image
FROM python:3.9-slim AS builder

# Setting Working Directory
COPY src /opt/src
WORKDIR /opt/src

# Installing Dependencies
RUN apt-get update && apt-get install -y sqlite3 \
    && python3 -m venv venv \
    && . venv/bin/activate \
    && pip install --no-cache-dir -r requirements.txt

# Stage 2: Running the App
FROM python:3.9-slim

# Setting Working Directory
WORKDIR /opt/src

# Install SQLite
RUN apt-get update && apt-get install -y sqlite3

# Copy Files From builder
COPY --from=builder /opt/src /opt/src

# Setting Environment Variables
ENV FLASK_APP=main.py
ENV PATH="/opt/src/venv/bin:$PATH"

# Database Instantiation
RUN flask db init \
    && flask db migrate -m "Initial migration" \
    && flask db upgrade

ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=5000"]