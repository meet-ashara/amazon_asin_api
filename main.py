from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models import AsinRequest
from scraper import parse_amazon_page
import uvicorn

app = FastAPI(title="Amazon ASIN Scraper API")

# Load templates
templates = Jinja2Templates(directory="templates")

# 👋 UI Homepage
@app.get("/", response_class=HTMLResponse)
def home(request: Request, asin: str = None):
    data = None
    error = None
    if asin:
        data = parse_amazon_page(asin)
        if "error" in data:
            error = data["error"]
            data = None
    return templates.TemplateResponse("index.html", {"request": request, "data": data, "error": error})

# 📦 Form submit (UI test) -> Redirect
@app.post("/scrape-ui")
def scrape_ui(asin: str = Form(...)):
    return RedirectResponse(url=f"", status_code=303)

# 🟢 Health check route
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running"}

# 📦 API JSON endpoint
@app.post("/scrape")
def scrape_asin(request: AsinRequest):
    data = parse_amazon_page(request.asin)
    if "error" in data:
        raise HTTPException(status_code=500, detail=data["error"])
    return data

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

