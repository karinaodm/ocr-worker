from __future__ import annotations

import os
import base64

import cv2
import numpy as np
import bentoml

os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"

from paddleocr import PaddleOCR  # noqa: E4


@bentoml.service(
    traffic={"timeout": 60},
    resources={"gpu": 1},
)
class OCRService:
    def __init__(self) -> None:
        self.ocr = PaddleOCR(
            lang="ru",
            use_doc_orientation_classify=True,
            use_doc_unwarping=True,
        )

    @bentoml.api
    def recognize(self, image: bytes) -> list[dict]:
        """Run OCR on a JPEG-encoded image.

        Returns list of {"bbox": [[x,y],...], "text": str, "confidence": float}.
        """
        image = base64.b64decode(image)
        nparr = np.frombuffer(image, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return []
        result = self.ocr.ocr(img)
        if not result or not result[0].get("rec_texts"):
            return []
        res = result[0]
        parsed = [
            {"bbox": poly.tolist(), "text": text, "confidence": float(score)}
            for poly, text, score in zip(
                res["rec_polys"], res["rec_texts"], res["rec_scores"]
            )
        ]
        return parsed
