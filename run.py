import os
import time
import logging

import pandas as pd
from tqdm import tqdm


from scraper.config import CITIES
from scraper.search import get_properties
from scraper.detail import get_post_detail
from scraper.parser import parse_property


# Logging
os.makedirs("logs", exist_ok=True)

logging.basicConfig(filename="logs/scraper.log", level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

logger = logging.getLogger(__name__)

# Paths
OUTPUT_PATH = ("data/processed/houses.csv")


# Save Dataset
def save_dataframe(records, path=OUTPUT_PATH):

    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df = pd.DataFrame(records)
        df.to_csv(path, index=False, encoding="utf-8-sig")
        logger.info(f"Saved {len(df)} records")
    except Exception:
        logger.exception("Saving dataframe failed")


# Collect City Data
def collect_city(city_name, city_id, target_count=1000):
    """
    Collect one city data
    """

    logger.info(f"Start collecting {city_name}")


    print(f"\n--------- {city_name} ---------")

    listings = get_properties(target_count=target_count, city_id=city_id)

    print(f"{city_name}: {len(listings)} listings")

    return listings



# Main Pipeline
def main():

    logger.info("Pipeline started")
    all_results = []

    # Loop Cities
    for city_name, city_id in CITIES.items():

        # Skip undefined ids
        if city_id == "...":
            logger.warning(f"Skipping {city_name}, missing city id")
            continue
        listings = collect_city(city_name, city_id, target_count=1000)

        # Detail Extraction
        print("Extracting details...")

        for listing in tqdm(listings):
            token = listing.get("token")

            try:
                detail = get_post_detail(token)
                if not detail:
                    logger.warning(f"No detail: {token}")
                    continue

                property_data = parse_property(detail)

                # Add metadata
                property_data.update(
                    {
                        "token": token,
                        "title": listing.get("title"),
                        "city": city_name,
                        "district": listing.get("district"),
                        "city_id": city_id
                    }
                )
                all_results.append(property_data)

                # Save checkpoint
                if len(all_results) % 50 == 0:
                    save_dataframe(all_results)
            except Exception:
                logger.exception(f"Failed processing {token}")
                continue

            time.sleep(0.5)


    # Final Save
    print("\nSaving final dataset...")
    save_dataframe(all_results)
    logger.info(f"Pipeline finished. Total {len(all_results)} rows")
    print(f"\nDONE {len(all_results)} properties saved")


if __name__ == "__main__":

    main()