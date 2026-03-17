import json
import os
from dotenv import load_dotenv

load_dotenv()

# Load the dealership JSON once at startup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEALERS_DATA = json.load(f)

with open(DEALERSHIP_FILE, "r") as f:
    DEALERS_DATA = json.load(f)["dealerships"]

sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url', default="http://localhost:5050/"
)

# Get request for dealerships
def get_request(endpoint, **kwargs):
    print(f"GET called for endpoint: {endpoint}")

    # Get all dealers
    if endpoint.startswith("/fetchDealers"):
        parts = endpoint.split("/")
        if len(parts) == 3 and parts[2] != "":
            state = parts[2]
            filtered = [d for d in DEALERS_DATA if d["state"].lower() == state.lower()]
            return filtered
        else:
            return DEALERS_DATA

    # Get single dealer by ID
    elif endpoint.startswith("/fetchDealer/"):
        try:
            dealer_id = int(endpoint.split("/")[-1])
        except ValueError:
            return {"error": "Invalid dealer_id"}
        dealer = next((d for d in DEALERS_DATA if d["id"] == dealer_id), None)
        return dealer if dealer else {"error": "Dealer not found"}

    # Placeholder for reviews (empty list for now)
    elif endpoint.startswith("/fetchReviews/dealer/"):
        return []

    return {}

# Sentiment analysis stub
def analyze_review_sentiments(text):
    return {"sentiment": "neutral"}

# Post review stub
def post_review(data_dict):
    print("Review received:", data_dict)
    return {"status": "success", "data": data_dict}
