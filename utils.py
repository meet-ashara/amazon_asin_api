import re

def clean_text(text: str) -> str:
    if not text:
        return "N/A"
    return re.sub(r"[₹$,]", "", text).strip()

def extract_numeric(val: str, is_float=False):
    """Extract numbers from a string and return int/float."""
    try:
        val = re.sub(r"[^\d.]", "", val)
        return float(val) if is_float else int(float(val))
    except:
        return None
