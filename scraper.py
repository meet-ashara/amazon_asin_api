from curl_cffi import requests
import lxml.html
import re, json
from utils import clean_text, extract_numeric

# this is an header
header = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-language': 'en-US,en;q=0.9',
  'cache-control': 'no-cache',
  'device-memory': '8',
  'downlink': '10',
  'dpr': '1.5',
  'ect': '4g',
  'pragma': 'no-cache',
  'priority': 'u=0, i',
  'referer': 'https://www.amazon.in/?&tag=googhydrabk1-21&ref=pd_sl_5szpgfto9i_e&adgrpid=155259813593&hvpone=&hvptwo=&hvadid=674893540034&hvpos=&hvnetw=g&hvrand=3438776855974821161&hvqmt=e&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9061768&hvtargid=kwd-64107830&hydadcr=14452_2316413&gad_source=1',
  'rtt': '50',
  'sec-ch-device-memory': '8',
  'sec-ch-dpr': '1.5',
  'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
  'sec-ch-ua-mobile': '?1',
  'sec-ch-ua-platform': '"Android"',
  'sec-ch-ua-platform-version': '"6.0"',
  'sec-ch-viewport-width': '609',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
  'viewport-width': '609',
  'Cookie': 'session-id=525-2092286-0431920; i18n-prefs=INR; lc-acbin=en_IN; ubid-acbin=262-1874532-9274438; session-token=+CG9cMGBczG7Igdp3/4AuC1VmPqc98XvcEjU3H69Uf8vRmVvIPDuBRMrmF7e9jfAo6Jf36a5pT2P/xg9hAAVw/yGT74jg0YhINFwOzZUMpxjAfaRX2hn2JG7fhLX6oA3ZgjakguDxjDIdNz2ByFeNRlEwg4pUvS8Fj8XKoUiYi2aqHxtMPhoK9V84cx+F38a3QgRk1DPBQe2Ut4pnTrl7RClAQtSd4/q3fA9QzFSCO2ELC0E8LGskk3/kQumK7m9LKL0UnDACI2pVL180aLHPH7VoygqDXfxBGdh54o8eO/yWVupm/IMsYFfsegWM940/sHIUmar1ii5V+iYfRsFLrUA8I8nynla; rxc=AEcHHxWX6FUueV8NL5w; csm-hit=tb:DZM35TA44RKV8JKHK8AT+s-THZ91GQXKH8MCFHS8Q9F|1757051990514&t:1757051990514&adb:adblk_no; session-id-time=2082758401l; i18n-prefs=INR; lc-acbin=en_IN; session-id=525-2092286-0431920; session-id-time=2082787201l; session-token=ilThtBMRbpPjloz7xVdPfNpdVz/HyIPskXE6CkC3UcBBIIE2QAY+MBBg7bi9yHd6WUWsb/iMYDaVCefzIuGm9DPz5EjKD25q4Pk71OfZ84dXWBsFzg+LkMfR8gbMtHHvU8FzW2SFFIAetoTJOQZWMPnZdhT/NqETbKlSeloh3WW+dYIuxtR4ItbRP2N0dIBZUflAGdjmoEUYbQdqFAVoQrVsXkA5oIjDHcSWjeS/iPq2QGAEBaLKi8+AZki1PRrLr1xnOJlVHb3v0P8MT32q1z6KUjus0+Xy/DqYqUdleu77ZTvpJR964F+91iZAAdpW0pSRw4G2mQohrepeq0L3n1jBRxyOaIM4; ubid-acbin=262-1874532-9274438'
}


def safe_extract(tree, xpaths, multiple=False, join=False):
    """
    Try multiple xpaths safely, return first match or 'N/A'
    - multiple=True => return list
    - join=True => join list into string
    """
    if isinstance(xpaths, str):
        xpaths = [xpaths]

    for xp in xpaths:
        try:
            result = tree.xpath(xp)
            if result:
                if multiple:
                    return result
                if join:
                    return " ".join([r.strip() for r in result if r.strip()])
                return result[0].strip()
        except Exception:
            continue
    return [] if multiple else "N/A"


def parse_amazon_page(asin: str) -> dict:
    url = f"https://www.amazon.in/dp/{asin}?th=1&psc=1"
    response = requests.get(url, impersonate="chrome110",headers=header)

    if response.status_code != 200:
        return {"error": "Failed to fetch page (invalid ASIN or blocked)", "product_url": url}

    try:
        tree = lxml.html.fromstring(response.text)

        # Product name
        product_title = safe_extract(tree, '//h1/span[@id="productTitle"]/text()')
        turbo_block = re.search(
            r'<script[^>]+key[=\\"]+turbo-checkout-page-state[\\"]+[^>]*>\s*(\{.*?\})\s*</script>',
            response.text
        )
        turbo_data = json.loads(turbo_block.group(1)) if turbo_block else {}
        turbo_product_name = turbo_data.get("strings", {}).get("TURBO_CHECKOUT_HEADER", "").replace("Buy now:", "").strip()
        product_name = turbo_product_name or product_title or "N/A"

        # Price (multiple fallbacks)
        json_price = None
        try:
            json_price_block = safe_extract(tree, '//div[contains(@class,"twister-plus-buying-options-price-data")]/text()')
            if json_price_block != "N/A":
                json_price_data = json.loads(json_price_block)
                price_info = json_price_data['desktop_buybox_group_1'][0]
                json_price = price_info.get('displayPrice')
        except Exception:
            pass

        formatted_price = safe_extract(tree, '//span[@class="a-price a-text-price a-size-medium apexPriceToPay"]//span[@class="a-offscreen"]/text()', multiple=True, join=True)
        fallback_price = safe_extract(tree, '//span[@aria-hidden="true"]//span[@class="a-price-whole"]/text()')
        raw_price = json_price or formatted_price or fallback_price or "N/A"
        clean_price = extract_numeric(raw_price)

        # MRP
        mrp_raw = safe_extract(tree, [
            '(//span[contains(text(),"M.R.P.")])[1]/text()',
            '//span[@class="aok-relative"]//span[@class="a-size-small aok-offscreen"]/text()'
        ])
        mrp_clean = extract_numeric(mrp_raw.replace("M.R.P.:", "")) if mrp_raw != "N/A" else "N/A"

        # Discount
        discount_raw = safe_extract(tree, '//span[contains(@class,"savingsPercentage")]/text()')
        discount_percent = extract_numeric(discount_raw) if discount_raw != "N/A" else "N/A"

        # Ratings
        avg_rating = safe_extract(tree, '//a/span[@class="a-size-base a-color-base"]/text()')
        average_rating = extract_numeric(avg_rating, is_float=True) if avg_rating != "N/A" else "N/A"

        reviews = safe_extract(tree, '//a/span[@id="acrCustomerReviewText"]/text()')
        review_count = extract_numeric(reviews) if reviews != "N/A" else "N/A"

        # Images
        imgs1 = safe_extract(tree, '//img[@class="a-dynamic-image"]/@src', multiple=True)
        imgs2 = safe_extract(tree, '//div[@id="imgTagWrapperId"]/img/@src', multiple=True)
        main_image = imgs1[1] if len(imgs1) > 1 else (imgs2[0] if imgs2 else (imgs1[0] if imgs1 else "N/A"))

        thumbnails = safe_extract(tree, '//span[@class="a-button-text"]/img/@src', multiple=True)
        other_images = ",".join(thumbnails[1:]) if len(thumbnails) > 1 else ""

        # Brand
        brand_name = safe_extract(tree, [
            '//p/span[@class="a-size-medium a-text-bold"]/text()',
            '//tr[@id="bylineInfo"]/td/span/text()'
        ])

        # Stock
        stock_status = safe_extract(tree, '//span[@class="a-size-medium a-color-success"][contains(text(),"In stock")]/text()')

        # Categories
        categories = safe_extract(tree, '//a[@class="a-link-normal a-color-tertiary"]/text()', multiple=True)
        category_hierarchy = {f"l{i+1}": cat.strip() for i, cat in enumerate(categories)} if categories else {}

        return {
            "product_url": url,
            "currency": "₹",
            "product_name": product_name,
            "brand": brand_name,
            "main_image": main_image,
            "other_images": other_images,
            "product_price": clean_price,
            "mrp": mrp_clean,
            "discount_percent": discount_percent,
            "avg_rating": average_rating,
            "rating_count": review_count,
            "availability": stock_status,
            "category_hierarchy": category_hierarchy
        }

    except Exception as e:
        return {"error": str(e), "product_name": "N/A", "product_url": url}




