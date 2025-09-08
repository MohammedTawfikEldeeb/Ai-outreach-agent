
FROM python:3.11-slim as builder
WORKDIR /app


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# --- Final Stage ---
# This stage builds the final, lean image for production.
FROM python:3.11-slim
WORKDIR /app

# Copy the installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application source code and data
COPY ./app ./app
COPY ./src ./src
COPY ./data ./data

# The command to run the FastAPI application
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT