import requests

def verify_gumroad_event(event_json, access_token, webhook_secret=None, licensed_products=None):
    licensed_products = set(licensed_products or [])

    if webhook_secret:
        incoming_secret = event_json.get("secret")
        if incoming_secret != webhook_secret:
            return False, "Invalid webhook secret."

    sale_id = event_json.get("sale_id")
    product_permalink = event_json.get("product_permalink")
    license_key = event_json.get("license_key")

    if not sale_id and not product_permalink:
        return False, "Missing both sale_id and product_permalink."

    if product_permalink in licensed_products:
        if not license_key:
            return False, "Missing license_key for licensed product."
        url = "https://api.gumroad.com/v2/licenses/verify"
        payload = {"product_permalink": product_permalink, "license_key": license_key}
        try:
            resp = requests.post(url, data=payload, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            return False, f"License API error: {e}"
        if not data.get("success"):
            return False, data.get("message", "License verification failed")
        sale = data.get("purchase", {})
        if sale.get("refunded") or sale.get("chargebacked"):
            return False, "Sale refunded or chargebacked."
        return True, sale

    if not sale_id:
        return False, "Missing sale_id for non-licensed product."

    url = f"https://api.gumroad.com/v2/sales/{sale_id}"
    params = {"access_token": access_token}
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        return False, f"Sales API error: {e}"
    if not data.get("success"):
        return False, data.get("message", "Sale verification failed")
    sale = data.get("sale", {})
    if sale.get("refunded") or sale.get("chargebacked"):
        return False, "Sale refunded or chargebacked."
    return True, sale
