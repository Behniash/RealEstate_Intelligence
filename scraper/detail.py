import time
import logging
from typing import Optional, Dict

import requests
from scraper.config import DETAIL_URL


logger = logging.getLogger(__name__)


def get_post_detail(token: str, session: requests.Session = None, retries: int = 3, delay: float = 1) -> Optional[Dict]:
    """
    Get detail information of a Divar listing.

    Raw JSON responses are NOT saved.
    Data is returned directly for parsing.
    """

    url = f"{DETAIL_URL}/{token}"


    if session is None:
        session = requests.Session()



    for attempt in range(1, retries + 1):

        try:

            response = session.get(url, timeout=30)

            response.raise_for_status()

            data = response.json()

            return data



        except requests.exceptions.Timeout:

            logger.warning(f"Timeout {token} "f"attempt {attempt}/{retries}")



        except requests.exceptions.HTTPError as e:

            logger.warning(f"HTTP error {token}: {e}")

            break



        except ValueError:

            logger.warning(f"Invalid JSON response {token}")

            break



        except requests.exceptions.RequestException:

            logger.exception(f"Request failed {token}")



        except Exception:

            logger.exception(f"Unexpected error {token}")



        time.sleep(delay * attempt)


    return None





if __name__ == "__main__":

    token = "gaR1tEQz"

    data = get_post_detail(token)


    if data:

        print("Success!")
        print("Response received but not saved.")

    else:

        print("Failed")