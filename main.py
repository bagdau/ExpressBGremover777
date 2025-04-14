import os
import uuid
import requests
import shutil
import time
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from rembg import remove
from PIL import Image
from io import BytesIO

app = FastAPI()

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

class RemoveRequest(BaseModel):
    url: str
    organizationId: str
    imageId: str

@app.post("/remove-background")
async def remove_background(data: RemoveRequest):
    start_time = time.time()
    print("[removeBackground] Started", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))

    try:
        # 1. Скачиваем изображение
        response = requests.get(data.url, stream=True)
        if not response.ok:
            raise HTTPException(status_code=400, detail="Failed to download image")

        input_image = Image.open(BytesIO(response.content))
        input_array = input_image.convert("RGBA")

        # 2. Удаляем фон
        output_array = remove(input_array)
        output_image = Image.fromarray(output_array)

        # 3. Генерируем путь для файла
        prefix = f"{data.organizationId}/no-background/{data.imageId}"
        filename = f"{prefix}-{uuid.uuid4().hex}.png"
        output_path = os.path.join(OUTPUT_DIR, filename.replace("/", "_"))

        # 4. Сохраняем результат
        output_image.save(output_path)

        end_time = time.time()
        print("[removeBackground] Completed", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time)))
        print(f"[removeBackground] Duration: {round(end_time - start_time, 2)} sec")

        # 5. Возвращаем путь (или URL, если загружаешь на S3, CDN и т.п.)
        return {
            "fileName": filename,
            "publicUrl": f"/static/{filename.replace('/', '_')}"
        }

    except Exception as e:
        print("Error processing image:", e)
        raise HTTPException(status_code=400, detail=f"Failed to process image: {str(e)}")