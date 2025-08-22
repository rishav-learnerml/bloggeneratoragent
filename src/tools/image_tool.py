# src/tools/image_tool.py
from dataclasses import dataclass
import os
import requests
import urllib.parse

@dataclass
class ImageResult:
    url: str
    attribution: str

class ImageFetcher:
    """
    Fetch a cover image for a blog topic.
    - If UNSPLASH_ACCESS_KEY is set, uses Unsplash.
    - Otherwise, falls back to picsum.photos placeholder.
    """
    def __init__(self) -> None:
        self.unsplash_key = os.getenv("UNSPLASH_ACCESS_KEY")

    def fetch_cover_image(self, query: str, *, width: int = 1200, height: int = 630) -> ImageResult:
        if self.unsplash_key:
            try:
                resp = requests.get(
                    "https://api.unsplash.com/search/photos",
                    params={"query": query, "per_page": 1, "orientation": "landscape"},
                    headers={"Authorization": f"Client-ID {self.unsplash_key}"},
                    timeout=10,
                )
                resp.raise_for_status()
                data = resp.json()
                if data.get("results"):
                    item = data["results"][0]
                    url = item["urls"]["regular"]
                    credit = f'Photo by {item["user"]["name"]} on Unsplash'
                    return ImageResult(url=url, attribution=credit)
            except Exception:
                # fall through to placeholder
                pass

        # Fallback placeholder (no key needed)
        seed = urllib.parse.quote_plus(query or "blog")
        url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
        return ImageResult(url=url, attribution="Placeholder image via picsum.photos")
