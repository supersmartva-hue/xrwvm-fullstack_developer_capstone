import json
import os
from dotenv import load_dotenv

load_dotenv()

# Load the dealership JSON once at startup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEALERSHIP_FILE = os.path.join(BASE_DIR, "dealership.json")

with open(DEALERSHIP_FILE, "r") as f:
    DEALERS_DATA = json.load(f)["dealerships"]

sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url', default="http://localhost:5050/"
)


# Get request for dealerships
def get_request(endpoint, **kwargs):
    """
    This function replaces network calls with local JSON for dealer info.
    Supports endpoints:
      - /fetchDealers
      - /fetchDealers/<state>
      - /fetchDealer/<dealer_id>
    """
    print(f"GET called for endpoint: {endpoint}")

    # Get all dealers
    if endpoint.startswith("/fetchDealers"):
        # Check if state is included
        parts = endpoint.split("/")
        if len(parts) == 3 and parts[2] != "":
            state = parts[2]
            filtered = [d for d in DEALERS_DATA if d["state"] == state]
            return filtered
        else:
            return DEALERS_DATA

    # Get single dealer by ID
    elif endpoint.startswith("/fetchDealer/"):
        dealer_id = int(endpoint.split("/")[-1])
        dealer = next((d for d in DEALERS_DATA if d["id"] == dealer_id), None)
        return dealer if dealer else {}

    # Placeholder for reviews (empty list for now)
    elif endpoint.startswith("/fetchReviews/dealer/"):
        return []

    return {}
    

# Sentiment analysis stub (you can keep calling external service if available)
def analyze_review_sentiments(text):
    # Simple stub for testing
    return {"sentiment": "neutral"}


# Post review stub
def post_review(data_dict):
    # Simple stub for testing
    print("Review received:", data_dict)
    return {"status": "success", "data": data_dict}
