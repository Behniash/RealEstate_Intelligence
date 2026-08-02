import time
import logging
from typing import List, Dict

import requests

from scraper.config import SEARCH_URL


logger = logging.getLogger(__name__)


# Create Payload
def create_initial_payload(city_id: str = "1",category: str = "apartment-sell") -> dict:
    """
    Create Divar search payload
    """
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



# Extract Posts
def extract_posts(response_json: dict, city_id: str) -> List[Dict]:
    """
    Extract posts from Divar response
    """

    posts = []
    try:
        widgets = response_json.get("list_widgets", [])
        for widget in widgets:
            if widget.get("widget_type") != "POST_ROW":
                continue
            data = widget.get("data", {})
            payload = (data.get("action", {}).get("payload", {}))
            web_info = payload.get("web_info", {})
            token = payload.get("token")
            if not token:
                continue
            posts.append(
                {
                    "token": token,
                    "title": data.get("title"),
                    "city": web_info.get("city_persian"),
                    "district": web_info.get("district_persian"),
                    "price_text": data.get("middle_description_text"),
                    "city_id": city_id
                }
            )

    except Exception:
        logger.exception("Error while extracting posts")

    return posts



# Main Collector
def get_properties(target_count: int = 100, city_id: str = "1", category: str = "apartment-sell", delay: float = 1, max_retries: int = 3) -> List[Dict]:
    """
    Collect properties from Divar API
    """
    session = requests.Session()
    payload = create_initial_payload(city_id, category)
    all_posts = []
    seen_tokens = set()
    page = 1
    while len(all_posts) < target_count:
        print(f"Requesting page {page}...")
        retry_count = 0
        while retry_count < max_retries:
            try:
                response = session.post(SEARCH_URL, json=payload, timeout=30)
                response.raise_for_status()
                data = response.json()

                break

            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                retry_count += 1
                logger.warning(f"Retry {retry_count}/{max_retries}: {e}")
                time.sleep(3)

            except requests.exceptions.RequestException:
                logger.exception("Request failed")
                return all_posts
            
            except ValueError:
                logger.exception("Invalid JSON")
                return all_posts
            
        else:
            logger.error("Max retries exceeded")
            break


        posts = extract_posts(data, city_id)

        if not posts:
            logger.warning("No posts found")
            break

        for post in posts:
            token = post["token"]
            if token not in seen_tokens:
                seen_tokens.add(token)
                all_posts.append(post)
        print(f"Collected {len(all_posts)} posts")

        pagination = (data.get("pagination", {}).get("data"))

        if not pagination:
            logger.warning("Pagination missing")
            break

        has_next = (data.get("pagination", {}).get("has_next_page", False))

        if not has_next:
            break

        payload["pagination_data"] = pagination
        page += 1

        time.sleep(delay)

    return all_posts[:target_count]



# Test
if __name__ == "__main__":
    posts = get_properties(target_count=100, city_id="1")
    print(f"\nTotal: {len(posts)}")
    for post in posts[:5]:
        print(post)