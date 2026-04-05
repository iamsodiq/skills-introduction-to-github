import hashlib
import hmac
import json
import requests
import time

# ==============================
# CONFIGURATION
# ==============================

BASE_URL = "https://api.weatherlink.com/v2/"
API_KEY = "weawiavcatn2o45hqjcbsvsluqr5o2i4"
API_SECRET = "oun4ocr5sdkd0kcsphxfjqj5pptdy6um"
ENDPOINT = "stations"  # e.g. "stations/" or "current/<station-id>"


# ==============================
# HELPER FUNCTIONS
# ==============================

def generate_signature(params, api_secret):
    """Generate HMAC SHA256 signature."""
    signature_string = ""

    for key, value in params:
        signature_string += key + value

    signature = hmac.new(
        api_secret.encode("utf-8"),
        signature_string.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return signature


def build_url(base_url, endpoint, params, signature):
    """Construct final API URL."""
    query_string = "&".join(f"{k}={v}" for k, v in params)
    return f"{base_url}{endpoint}?{query_string}&api-signature={signature}"


def make_request(url):
    """Make API request with error handling."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses

        # Try parsing JSON
        try:
            return response.json()
        except json.JSONDecodeError:
            print("⚠️ Failed to parse JSON response")
            print("Raw response:", response.text)
            return None

    except requests.exceptions.RequestException as e:
        print("❌ Request failed:", e)
        return None


# ==============================
# MAIN LOGIC
# ==============================

def main():
    # Use ONE timestamp for consistency
    timestamp = str(int(time.time()))

    # Parameters (must be sorted)
    params = sorted([
        ("api-key", API_KEY),
        ("t", timestamp)
    ])

    # Generate signature
    signature = generate_signature(params, API_SECRET)

    # Build final URL
    url = build_url(BASE_URL, ENDPOINT, params, signature)

    print("🔗 Request URL:")
    print(url)

    # Make request
    data = make_request(url)

    if data:
        print("\n✅ API Response:")
        print(json.dumps(data, indent=4))
    else:
        print("\n⚠️ No valid data returned.")


# ==============================
# RUN SCRIPT
# ==============================

if __name__ == "__main__":
    main()