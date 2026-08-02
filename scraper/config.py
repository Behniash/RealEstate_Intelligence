
BASE_URL = "https://api.divar.ir/v8"
SEARCH_URL = (f"{BASE_URL}/postlist/w/search")
DETAIL_URL = (f"{BASE_URL}/posts-v2/web")

TARGET_COUNT_PER_CITY = 5000
MAX_WORKERS = 20

CITIES = {
    "tehran": "1",
    "karaj": "2",
    "mashhad": "3",
    "isfahan": "4",
    "tabriz": "5",
    "shiraz": "6",
    "ahvaz": "7",
    "qom": "8",
    "hamadan": "14",
    "arak": "15",
    "yazd": "16",
    "ardabil": "17",
    "qazvin": "19",
    "zanjan": "20",
    "gorgan": "21",
    "sari": "22",
    "bushehr": "25",
    "sanandaj": "28",
    "khoramabad": "27",
    "kish": "33",
    "birjand": "34",
    "semnan": "35",
    "bojnurd": "39",
    "rasht": "12",
    "behshahr": "832",
    "babol": "664",
    "babolsar": "710"
}