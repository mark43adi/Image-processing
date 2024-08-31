from PIL import Image
import requests
from io import BytesIO
from typing import List
# import logging


def process_image(url: str) -> str:
    url = url.strip()
    try:
        response = requests.get(url)
        response.raise_for_status()  
    except requests.RequestException as e:
        print(f"Failed to fetch image from {url}: {e}")
        return ""  

    img = Image.open(BytesIO(response.content))
    output = BytesIO()
    img.save(output, format="JPEG", quality=50)
    return f"https://www.public-image-output-url-{url.split('/')[-1]}"

def process_images(urls: List[str]) -> List[str]:
    return [process_image(url) for url in urls]