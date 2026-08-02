import os
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
from tqdm import tqdm
import requests


from scraper.config import CITIES, TARGET_COUNT_PER_CITY, MAX_WORKERS
from scraper.search import get_properties
from scraper.detail import get_post_detail
from scraper.parser import parse_property



# Logging
os.makedirs("logs", exist_ok=True)

logging.basicConfig(filename="logs/scraper.log", level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

logger = logging.getLogger(__name__)

OUTPUT_PATH = "data/processed/houses.csv"



# Load Existing Dataset
def load_existing_data(path=OUTPUT_PATH):
    if not os.path.exists(path):
        return [], set()

    try:
        df = pd.read_csv(path)

        if "token" not in df.columns:

            return [], set()


        records = df.to_dict(orient="records")

        tokens = set(df["token"].dropna().astype(str))

        logger.info(f"Loaded {len(tokens)} tokens")

        return records, tokens


    except Exception:

        logger.exception("Loading dataset failed")

        return [], set()




# Save Dataset
def save_dataframe(records):

    try:

        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

        df = pd.DataFrame(records)

        if "token" in df.columns:

            df.drop_duplicates(subset=["token"], keep="last", inplace=True)

        df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

        print(f"Saved {len(df)} rows")

    except Exception:

        logger.exception("Saving failed")



# Collect city
def collect_city(city_name, city_id):

    print(f"\n------------- {city_name.upper()} -------------")


    listings = get_properties(target_count=TARGET_COUNT_PER_CITY, city_id=city_id)


    print(f"{city_name}: {len(listings)} raw listings")


    return listings



# Process one listing
def process_listing(listing, city_name, city_id):

    token = str(listing.get("token"))

    try:
        # Each thread gets its own session
        session = requests.Session()

        detail = get_post_detail(token, session=session)

        if not detail:
            print(f"FAILED DETAIL: {token}")

            return None


        property_data = parse_property(detail)

        if not property_data:

            print(f"FAILED PARSE: {token}")

            return None


        property_data.update(
            {
                "token": token,
                "title": listing.get("title"),
                "city": city_name,
                "district": listing.get("district"),
                "city_id": city_id
            }
        )

        return property_data

    except Exception:


        logger.exception(f"Failed processing {token}")

        return None




# Main
def main():

    logger.info("Pipeline started")


    all_results, existing_tokens = load_existing_data()


    print(f"Existing dataset: {len(existing_tokens)}")


    for city_name, city_id in CITIES.items():

        listings = collect_city(city_name, city_id)

        if not listings:

            continue

        new_listings = [x for x in listings if str(x.get("token")) not in existing_tokens]

        print(f"New listings: {len(new_listings)}")

        if not new_listings:
            continue

        new_records = []

        print("Extracting details...")

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

            futures = [executor.submit(process_listing, listing, city_name, city_id) for listing in new_listings]

            for future in tqdm(as_completed(futures), total=len(futures)):

                result = future.result()

                if result:

                    new_records.append(result)

                    all_results.append(result)

                    existing_tokens.add(result["token"])

                    if len(all_results) % 500 == 0:

                        save_dataframe(all_results)

                        print(f"Checkpoint: {len(all_results)}")


        print(f"{city_name}: {len(new_records)} added")


    print("\nFinal saving...")

    save_dataframe(all_results)

    print(f"DONE! Total dataset: {len(all_results)}")



if __name__ == "__main__":

    main()