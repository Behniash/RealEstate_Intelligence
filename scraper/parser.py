import re
import logging


logger = logging.getLogger(__name__)


PERSIAN_NUMBERS = "۰۱۲۳۴۵۶۷۸۹"
ENGLISH_NUMBERS = "0123456789"


def clean_number(value):
    """
    Convert Persian numbers to integer
    """

    if value is None:
        return None


    try:

        value = str(value)


        value = value.translate(
            str.maketrans(
                PERSIAN_NUMBERS,
                ENGLISH_NUMBERS
            )
        )


        value = (
            value
            .replace(",", "")
            .replace("٬", "")
            .replace("تومان", "")
            .replace("\u200f", "")
            .strip()
        )


        if value.isdigit():

            return int(value)


        return value


    except Exception:

        logger.exception(
            "clean_number failed"
        )

        return None





def parse_floor(value):

    if not value:
        return None, None


    try:

        value = str(value).strip()


        special = {

            "همکف": 0,

            "زیرزمین": -1,

            "پیلوت": -1

        }


        if value in special:

            return special[value], None



        value = (
            value
            .replace("طبقه", "")
            .strip()
        )


        value = value.translate(
            str.maketrans(
                PERSIAN_NUMBERS,
                ENGLISH_NUMBERS
            )
        )


        if "از" in value:


            parts = value.split("از")


            return (
                int(parts[0].strip()),
                int(parts[1].strip())
            )



        if value.isdigit():

            return int(value), None



    except Exception:

        logger.warning(
            f"Cannot parse floor: {value}"
        )


    return None, None





def extract_features(data):

    """
    Extract all property features
    """

    features = {}


    try:

        for item in data.get("items", []):


            title = item.get(
                "title"
            )


            if title:

                features[title] = True



    except Exception:

        pass


    return features





def parse_property(json_data):


    result = {


        "area": None,

        "year_built": None,

        "rooms": None,


        "total_price": None,

        "price_per_meter": None,


        "floor": None,

        "total_floors": None,


        "elevator": False,

        "parking": False,

        "storage": False,

        "balcony": False,


        "latitude": None,

        "longitude": None,


        "description": None

    }



    try:


        sections = json_data.get(
            "sections",
            []
        )


        for section in sections:


            section_name = section.get(
                "section_name"
            )



            for widget in section.get(
                    "widgets",
                    []
            ):


                widget_type = widget.get(
                    "widget_type"
                )


                data = widget.get(
                    "data",
                    {}
                )


                if widget_type == "GROUP_INFO_ROW":


                    for item in data.get(
                            "items",
                            []
                    ):


                        title = item.get(
                            "title"
                        )


                        value = clean_number(
                            item.get("value")
                        )



                        if title == "متراژ":

                            result["area"] = value


                        elif title == "ساخت":

                            result["year_built"] = value


                        elif title == "اتاق":

                            result["rooms"] = value




                elif widget_type == "UNEXPANDABLE_ROW":


                    title = data.get(
                        "title"
                    )


                    value = data.get(
                        "value"
                    )



                    if title == "قیمت کل":

                        result["total_price"] = clean_number(value)



                    elif title == "قیمت هر متر":

                        result["price_per_meter"] = clean_number(value)



                    elif title == "طبقه":


                        floor, total = parse_floor(
                            value
                        )

                        result["floor"] = floor

                        result["total_floors"] = total







                elif widget_type in [
                    "GROUP_FEATURE_ROW"
                ]:


                    for item in data.get(
                            "items",
                            []
                    ):


                        title = item.get(
                            "title"
                        )


                        if title == "آسانسور":

                            result["elevator"] = True


                        elif title == "پارکینگ":

                            result["parking"] = True


                        elif title == "انباری":

                            result["storage"] = True


                        elif title == "بالکن دارد":

                            result["balcony"] = True







                elif widget_type == "DESCRIPTION_ROW":


                    result["description"] = data.get(
                        "text"
                    )






            if section_name == "MAP":


                try:

                    point = (
                        section["widgets"][0]
                        ["data"]
                        ["location"]
                        ["exact_data"]
                        ["point"]
                    )


                    result["latitude"] = point.get(
                        "latitude"
                    )


                    result["longitude"] = point.get(
                        "longitude"
                    )


                except Exception:

                    pass



    except Exception:


        logger.exception(
            "Parsing property failed"
        )



    return result