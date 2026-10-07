# ocr-worker

BentoML-сервис для распознавания текста на изображениях с помощью PaddleOCR на GPU.

Используется для сканов документов без текстового слоя, которые могут быть перекошены или сфотографированы под углом — поэтому в `service.py` включены `use_doc_orientation_classify`/`use_doc_unwarping` и увеличен `traffic.timeout` (60 с): полная страница текста с коррекцией геометрии обрабатывается дольше, чем небольшой ровный кроп.

## Требования

- Docker с поддержкой NVIDIA GPU (`nvidia-container-toolkit`)
- CUDA 11.8, cuDNN 8.9

## Сборка

```bash
cd ocr-worker
docker build -t ocr-worker .
```

## Запуск

```bash
docker run --gpus all \
  -p 3000:3000 \
  -v $(pwd)/ocr_models:/root/.paddlex \
  ocr-worker
```

Volume `ocr_models` кэширует веса PaddleOCR (~100 МБ), которые скачиваются при первом запуске.

## API

### `POST /recognize`

Принимает JPEG-изображение, возвращает распознанные текстовые блоки.

**Request**

```
Content-Type: application/json
Body: {"image": "<base64-encoded JPEG bytes>"}
```

**Response**

```json
[
  {
    "bbox": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]],
    "text": "распознанный текст",
    "confidence": 0.97
  }
]
```

Пустой список `[]` — текст не найден или изображение пустое.

## Использование

Сервис запускается локально (`http://localhost:3000`) и дергается постранично клиентским скриптом (страница в JPEG → `POST /recognize` → сборка текстовых блоков в связный текст по координатам).
