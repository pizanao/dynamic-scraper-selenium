# Dynamic Web Scraper with Selenium

GitHub-ready portfolio project for Python Data Scraping Engineer roles. It demonstrates a real end-to-end workflow for a dynamic website: login, JavaScript-rendered content, infinite scroll, selector adaptation, validation, retries, and structured exports.

## What it shows

- Selenium browser automation
- Explicit waits and resilient extraction
- Dynamic content / AJAX / infinite scroll
- Selector self-healing Code Agent
- JSON + CSV output
- Pydantic validation
- Local demo site for safe video recording
- Unit tests and Playwright demo recording

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.cli serve-demo --host 127.0.0.1 --port 5000
```

In another terminal:

```bash
python -m app.cli scrape --base-url http://127.0.0.1:5000 --output-dir output
```

## Record demo video

```bash
cd playwright
npm install
npx playwright install chromium
npm run demo:video
```

Use only on websites you own or are authorized to test.
