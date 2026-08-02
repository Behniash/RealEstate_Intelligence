import os
import json
import time
import logging
from typing import Optional, Dict

import requests

from scraper.config import DETAIL_URL


logger = logging.getLogger(__name__)


RAW_DETAIL_PATH = "data/raw/details"



def save_raw_detail(
        token: str,
        data: dict
):
    """
    Save original Divar response
    """

    try:

        os.makedirs(
            RAW_DETAIL_PATH,
            exist_ok=True
        )


        file_path = os.path.join(
            RAW_DETAIL_PATH,
            f"{token}.json"
        )


        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=2
            )


    except Exception:

        logger.exception(
            f"Failed saving raw detail {token}"
        )




def get_post_detail(
        token: str,
        session: requests.Session = None,
        save_raw: bool = True,
        retries: int = 3,
        delay: float = 1
) -> Optional[Dict]:
    """
    Get detail information of a Divar listing
    """


    url = f"{DETAIL_URL}/{token}"


    if session is None:

        session = requests.Session()



    for attempt in range(1, retries + 1):


        try:

            response = session.get(
                url,
                timeout=30
            )


            response.raise_for_status()


            data = response.json()



            if save_raw:

                save_raw_detail(
                    token,
                    data
                )


            return data



        except requests.exceptions.Timeout:


            logger.warning(
                f"Timeout {token} "
                f"attempt {attempt}/{retries}"
            )



        except requests.exceptions.HTTPError as e:


            logger.warning(
                f"HTTP error {token}: {e}"
            )


            break



        except ValueError:


            logger.warning(
                f"Invalid JSON {token}"
            )


            break



        except requests.exceptions.RequestException:


            logger.exception(
                f"Request failed {token}"
            )



        except Exception:


            logger.exception(
                f"Unexpected error {token}"
            )



        time.sleep(
            delay * attempt
        )



    return None





if __name__ == "__main__":


    token = "gaR1tEQz"


    data = get_post_detail(
        token
    )



    if data:

        print(
            "Success!"
        )

    else:

        print(
            "Failed"
        )