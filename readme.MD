# 🛒 Amazon ASIN Scraper API  

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)  
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi)](https://fastapi.tiangolo.com/)  
[![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI%20Server-ff69b4)](https://www.uvicorn.org/)  
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-UI-38bdf8?logo=tailwindcss)](https://tailwindcss.com/)  
[![Flowbite](https://img.shields.io/badge/Flowbite-Components-1a56db)](https://flowbite.com/)  
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  


---

## 📖 Project Overview
The **Amazon ASIN Scraper API** is a lightweight and modern **FastAPI** project that extracts product details from Amazon using ASIN codes.  
It provides both:
- 🟢 **REST API JSON endpoints** for developers  
- 🎨 **Modern UI (Tailwind + Flowbite)** for testing directly in the browser  

---

## ✨ Features
- 🔍 Scrape Amazon product data using only an ASIN  
- ⚡ Built with **FastAPI + Uvicorn** for high performance  
- 🎨 User-friendly UI with **TailwindCSS & Flowbite**  
- 📦 Clean project structure (models, scraper, templates)  
- 🛠️ Error handling with proper API responses  
- 🟢 Health check endpoint for monitoring  

---

## 🚀 Installation

### 1️⃣ Clone the Repository
```bash
git https://github.com/meetashara31/amazon_asin_api
cd amazon_asin_api

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

▶️ Running the Project

Start the FastAPI server:

uvicorn main:app --host 0.0.0.0 --port 8000 --reload


Now visit:

🌐 UI: http://127.0.0.1:8000

📜 API Docs: http://127.0.0.1:8000/docs

🟢 Health Check: http://127.0.0.1:8000/health

📦 Example Usage
API Request
curl -X POST "http://127.0.0.1:8000/scrape" \
     -H "Content-Type: application/json" \
     -d '{"asin": "B08N5WRWNW"}'

API Response
{
  "product_name": "Apple iPhone 12 (64GB) - Black",
  "price": "₹52,999",
  "mrp": "₹65,900",
  "discount": "19%",
  "avg_rating": "4.6",
  "rating_count": "20,345",
  "main_img": "https://images.amazon.com/iphone12.jpg"
}

🖼️ UI Preview

The UI is built using TailwindCSS + Flowbite for a clean modern look.
It lets you enter an ASIN, test the scraper, and view results in real-time.

📌 Project Structure
├── main.py          # FastAPI app entry point
├── models.py        # Pydantic models
├── scraper.py       # Scraper logic
├── templates/       # Jinja2 templates for UI
│   └── index.html
├── requirements.txt # Dependencies
└── README.md        # Project documentation

🛡️ License

This project is licensed under the MIT License.
You are free to use, modify, and distribute this project.

⭐ Contributing

Contributions are welcome!
If you like this project, give it a ⭐ on GitHub to support it 🙌


