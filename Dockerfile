# Base image
FROM python:3.12-slim

# Install system dependency required by LightGBM
RUN apt-get update && \
    apt-get install -y --no-install-recommends libgomp1 && \
    rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Working directory
WORKDIR /app

# Copy only production requirements
COPY requirements-dockers.txt .

# Install production dependencies
RUN uv pip install --system --no-cache -r requirements-dockers.txt

# copy the app contents
COPY app.py ./
COPY ./models/preprocessor.joblib ./models/preprocessor.joblib
COPY ./scripts/data_clean_utils.py ./scripts/data_clean_utils.py
COPY ./run_information.json ./

# Expose FastAPI port
EXPOSE 8000

# Start API
CMD ["python", "app.py"]