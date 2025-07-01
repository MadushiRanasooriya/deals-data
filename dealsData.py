import requests
from flask import Flask, jsonify
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

HUBSPOT_TOKEN = os.getenv("HUBSPOT_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {HUBSPOT_TOKEN}"
}

def get_deals():
    url = "https://api.hubapi.com/crm/v3/objects/deals"
    headers = HEADERS
    params = {
        "properties": "dealstage,dealname,amount,closedate,createdate",
        "associations": "company",
        "limit": 100
    }

    all_deals = []

    while True:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        for deal in data.get("results", []):
            deal_info = {
                "dealname": deal["properties"].get("dealname", ""),
                "dealstage": deal["properties"].get("dealstage", ""),
                "amount": deal["properties"].get("amount", "0"),
                "closedate": deal["properties"].get("closedate", ""),
                "createdate": deal["properties"].get("createdate", ""),
                "company_ids": [assoc["id"] for assoc in deal.get("associations", {}).get("companies", {}).get("results", [])]
            }
            all_deals.append(deal_info)

        if "paging" in data and "next" in data["paging"]:
            params["after"] = data["paging"]["next"]["after"]
        else:
            break

    return all_deals

@app.route("/deals")
def deals():
    deals = get_deals()
    return jsonify(deals)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
