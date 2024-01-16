from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from model import cropping_image, image_blurred, canny_edge_detection
from utils import receiving_image, encode_image_to_base64
import uvicorn
import os
# read the port from environment variable
backend_port = int(os.environ.get("VUE_APP_BACKEND_PORT", 8000))
frontend_port = int(os.environ.get("VUE_APP_FRONTEND_PORT", 8080))
version_number = int(os.environ.get("VUE_APP_VERSION_NUMBER", 1))


origins = [
    f"http://localhost:{frontend_port}",
]


class ImageUrl(BaseModel):
    base64_string: Optional[str] = None


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(f"/api/v{version_number}/health_check")
async def healthcheck():
    return {"status": "ok"}


@app.get(f"/api/v{version_number}/model_details")
async def model_details():
    return {"model_name": "model1", "model_version": f"v{version_number}"}


@app.post(f"/api/v{version_number}/preprocessing")
async def preprocessing(message: ImageUrl):
    """receiving the image from frontend through base64 string,
    and processing the image with opencv canny remove the background,
    enhance the edges and encode the processed image to base64 string again"""

    if not message.base64_string:
        raise HTTPException(status_code=400, detail="Please provide base64_string")
    else:
        img = receiving_image(message.base64_string)

    # preprocessing the image
    y, x = img.shape[:2]
    cropped = cropping_image(img, 0, 0, x // 2, y)
    cropped_blurred = image_blurred(cropped, kernel_size=4)
    edges = canny_edge_detection(cropped_blurred)

    # encode the image to base64
    img_str = encode_image_to_base64(edges)
    return {"processedImage": img_str}


if __name__ == "__main__":
    uvicorn.run(
        app="api_server:app",
        host="0.0.0.0",
        port=backend_port,
        log_level="info",
        reload=True,
    )
