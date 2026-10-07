FROM paddlepaddle/paddle:3.2.0-gpu-cuda11.8-cudnn8.9

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY service.py /app/service.py

EXPOSE 3000
CMD ["bentoml", "serve", "service:OCRService", "--production", "--host", "0.0.0.0", "--port", "3000"]
