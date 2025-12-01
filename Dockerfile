FROM python:3.12-slim as builder

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt

COPY . .

ENV PATH="/install/bin:$PATH"
ENV PYTHONPATH="/install/lib/python3.12/site-packages:$PYTHONPATH"

RUN pytest tests/ --maxfail=1 --disable-warnings


FROM python:3.12-slim

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*


COPY --from=builder /install /usr/local
COPY --from=builder /app /app

EXPOSE 8000


CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
