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

class RemoveRequest(BaseModel):
    url: str
    organizationId: str
    imageId: str

@app.post("/remove-background")
async def remove_background(data: RemoveRequest):
    return {
        "fileName": 'MAGZHAN',
        "publicUrl": 'remove-bg.png'
    }