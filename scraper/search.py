import time
import logging
from typing import List, Dict

import requests
import pandas as pd
import os

from scraper.config import SEARCH_URL

logger = logging.getLogger(__name__)

OUTPUT_PATH = "data/processed/houses.csv"



# Load existing tokens
def load_existing_tokens():

    if not os.path.exists(OUTPUT_PATH):
        return set()

    try:

        df = pd.read_csv(OUTPUT_PATH, usecols=["token"])

        return set(df["token"].dropna().astype(str))

    except Exception:

        logger.exception("Cannot load tokens")

        return set()



# Create Payload
def create_initial_payload(city_id, category="apartment-sell"):

    return {
        "city_ids": [city_id],
        "source_view": "CATEGORY",
        "disable_recommendation": False,
        "search_data": {
            "form_data": {
                "data": {
                    "category": {
                        "str": {
                            "value": category
                        }
                    }
                }
            },
            "query": "",
            "query_input_type": "UNKNOWN"
        },

        "map_state": {
            "camera_info": {
                "bbox": {}
            },
            "page_state": "HALF_STATE"
        }
    }



# Extract posts
def extract_posts(response_json, city_id):

    posts = []


    widgets = response_json.get("list_widgets", [])


    for widget in widgets:

        if widget.get("widget_type") != "POST_ROW":
            continue

        data = widget.get("data", {})

        payload = (data.get("action", {}).get("payload", {}))

        token = payload.get("token")

        if not token:
            continue


        web_info = payload.get("web_info", {})

        posts.append(
            {
                "token": str(token),
                "title": data.get("title"),
                "district": web_info.get("district_persian"),
                "city_id": city_id
            }
        )

    return posts



# Main Collector
def get_properties(target_count=5000, city_id="1", category="apartment-sell", delay=0.5):

    session = requests.Session()

    payload = create_initial_payload(city_id, category)

    existing_tokens = load_existing_tokens()

    collected = []

    seen = set(existing_tokens)

    page = 1

    while len(collected) < target_count:

        print(f"Requesting page {page}...")

        try:
            response = session.post(SEARCH_URL, json=payload, timeout=30)

            response.raise_for_status()

            data = response.json()

        except Exception as e:

            logger.exception(e)

            break



        posts = extract_posts(data, city_id)

        if not posts:

            print("No more posts")

            break



        new_count = 0

        for post in posts:

            token = post["token"]

            if token in seen:
                continue

            seen.add(token)

            collected.append(post)

            new_count += 1

            if len(collected) >= target_count:
                break

        print(f"Collected: {len(collected)} (+{new_count} new)")


        pagination = (data.get("pagination", {}).get("data"))

        has_next = (data.get("pagination", {}).get("has_next_page", False))

        if not pagination or not has_next:

            print("No next page")

            break


        payload["pagination_data"] = pagination

        page += 1

        time.sleep(delay)


    print(f"Finished collecting {len(collected)} listings")

    return collected