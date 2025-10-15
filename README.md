# Gumroad Sale Verification

A lightweight Python function to **verify Gumroad webhook events and sales** using the Gumroad API. Supports both licensed and non-licensed products, with optional webhook secret validation.

---

## Installation

Save the function in a file called `gumroad_verify.py` in your project. Make sure you have `requests` installed:

```bash
pip install requests
```

---

## Usage

```python
import os
from gumroad_verify import verify_gumroad_event

# Example event JSON received from Gumroad webhook
event_json = {
    "sale_id": "123456789",
    "product_permalink": "my-product",
    "license_key": "ABCD-1234-EFGH",
    "secret": "mywebhooksecret"  # optional
}

# Load your Gumroad access token (personal token)
access_token = os.getenv("GUMROAD_ACCESS_TOKEN")
webhook_secret = os.getenv("WEBHOOK_SECRET")  # optional

licensed_products = {"my-product", "my-software"}  # list of licensed product permalinks

valid, data = verify_gumroad_event(
    event_json=event_json,
    access_token=access_token,
    webhook_secret=webhook_secret,
    licensed_products=licensed_products
)

if valid:
    print("✅ Sale verified:", data)
else:
    print("❌ Verification failed:", data)
```

---

## Parameters

| Parameter | Type | Description | How to get it |
|-----------|------|-------------|---------------|
| `event_json` | `dict` | JSON payload sent by Gumroad webhook (Ping). | Received from your Gumroad Ping URL when a sale occurs (`flask.request.form.to_dict()`). |
| `access_token` | `str` | Personal Gumroad access token to access the Sales API. | Go to **Settings → Advanced → Applications → Create Application → Generate Access Token** in your Gumroad account. |
| `webhook_secret` | `str` or `None` | Optional secret key to verify the webhook payload. | You can set this in your Gumroad Ping URL settings; leave as `None` to skip verification. |
| `licensed_products` | `list` or `set` | List of product permalinks that use license keys. | Use your Gumroad product permalink(s) that require license verification. |

---

## Notes

- The function automatically checks for **refunds or chargebacks** and fails verification if found.  
- If `webhook_secret` is not provided, the function will **skip webhook verification**.  
- License verification is performed **only for products listed in `licensed_products`**.  
- Store your `access_token` securely (environment variable or secrets manager) and **never commit it publicly**.  

---

## References

- [Gumroad Webhooks](https://gumroad.com/advanced#webhooks)  
- [Gumroad API Documentation](https://gumroad.com/api)

---

###A Note from Me

I might not be the best developer, but I wanted to help. If you find this too simple or think it could be better, I created it to the best of my ability, and I apologize in advance
for any shortcomings. My goal is for this repository is to just to make things a little easier for people working with Gumroad integration.
