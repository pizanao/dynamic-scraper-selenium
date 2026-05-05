import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def as_bool(v: str | None, default=True) -> bool:
    if v is None:
        return default
    return v.lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "http://127.0.0.1:5000")
    username: str = os.getenv("SCRAPER_USERNAME", "demo")
    password: str = os.getenv("SCRAPER_PASSWORD", "demo")
    headless: bool = as_bool(os.getenv("HEADLESS"), True)
    page_limit: int = int(os.getenv("PAGE_LIMIT", "6"))
    item_target: int = int(os.getenv("ITEM_TARGET", "30"))
    output_dir: str = os.getenv("OUTPUT_DIR", "output")
    proxy_url: str | None = os.getenv("PROXY_URL") or None
    timeout_seconds: int = int(os.getenv("TIMEOUT_SECONDS", "12"))
