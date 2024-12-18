from fastapi import FastAPI, Depends, Query, HTTPException

from config import STATIC_TOKEN
from scraper import Scraper
from storage import JSONFileStorage
from cache import CacheManager
from notifications import ConsoleNotifier
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class ScraperSettings(BaseModel):
    max_pages: Optional[int] = Query(None, description="Max pages to scrape")
    proxy: Optional[str] = Query(None, description="Proxy to use")

def authenticate(token: str = Query(..., description="Authentication token")):
    if token != STATIC_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/scrape", dependencies=[Depends(authenticate)])
async def scrape(settings: ScraperSettings):
    storage = JSONFileStorage("scraped_data.json")
    cache = CacheManager()
    notifier = ConsoleNotifier()
    scraper = Scraper(storage_handler=storage, cache_manager=cache, notifier=notifier)
    scraper.scrape(max_pages=settings.max_pages, proxy=settings.proxy)
    return {"status": "Scraping completed"}


