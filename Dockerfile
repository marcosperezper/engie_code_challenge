FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the whole project
COPY . .

# Run tests
RUN pytest tests/ --maxfail=1 --disable-warnings


FROM python:3.12-slim

WORKDIR /app

# Copy dependencies from builder
COPY /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY /app /app

# Expose port
EXPOSE 8000

# Run FastAPI app using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
