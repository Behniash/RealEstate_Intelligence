# Real Estate Intelligence Platform

An end-to-end real estate data intelligence project focused on collecting, processing, analyzing, and building insights from Iranian housing market data.

The goal of this project is to create a data-driven platform that can analyze housing prices, discover market trends, estimate property values, and provide intelligent insights for buyers, sellers, and real estate analysts.

---

# Project Overview

Real Estate Intelligence Platform is a data science project that collects real estate listings from online marketplaces, processes property information, and prepares the data for:

- Exploratory Data Analysis (EDA)
- Statistical analysis and hypothesis testing
- Price prediction models
- Market trend analysis
- Location-based analysis
- Real estate recommendation systems

The first MVP version focuses on building a reliable data collection pipeline and creating a structured real estate dataset.

---

# Data Source

The data is collected from:

**Divar.ir**

Website:

https://divar.ir

Divar is one of the largest Iranian online marketplaces where users publish real estate advertisements.

The project uses Divar's internal API endpoints to collect publicly available listing information.

---

# Data Collection Pipeline

The scraping pipeline consists of three main stages:

## 1. Search API Collection

The first step collects property listing summaries from Divar search endpoints.

Collected information:

- Advertisement token
- Title
- City
- District
- Price information


The scraper supports multiple cities.

Current supported cities:

- Tehran
- Gorgan
- Mashhad
- Shiraz
- Isfahan
- Tabriz
- Qom
- Rasht
- Yazd
- Sari


---

## 2. Property Detail Extraction

For each advertisement, the pipeline requests detailed information.

Extracted features include:

- Area
- Year built
- Number of rooms
- Total price
- Price per square meter
- Floor
- Total floors
- Building facilities
- Description
- Geographic coordinates


---

## 3. Data Parsing and Processing

The raw API responses contain nested JSON structures.

A custom parser converts the raw response into a clean tabular dataset.

The parser handles:

- Persian number conversion
- Price cleaning
- Floor extraction
- Missing values handling
- Feature extraction
- Boolean facilities


---

# Dataset

Current MVP dataset:

- Approximately 9,000 real estate listings
- Multiple Iranian cities
- Structured CSV format


Dataset columns:

| Feature | Description |
|---|---|
| area | Property size in square meters |
| year_built | Construction year |
| rooms | Number of rooms |
| total_price | Total property price |
| price_per_meter | Price per square meter |
| floor | Apartment floor |
| total_floors | Total building floors |
| elevator | Elevator availability |
| parking | Parking availability |
| storage | Storage availability |
| balcony | Balcony availability |
| latitude | Geographic latitude |
| longitude | Geographic longitude |
| description | Advertisement description |
| title | Advertisement title |
| city | City name |
| district | Neighborhood |
| city_id | Divar city identifier |


---

# Project Structure

```
RealEstate_Intelligence/

│
├── scraper/
│   ├── search.py          # Collect listing IDs
│   ├── detail.py          # Extract property details
│   ├── parser.py          # Convert API JSON to structured data
│   ├── config.py          # API configuration
│
├── data/
│   └── processed/
│       └── houses.csv     # MVP dataset
│
├── logs/
│   └── scraper.log
│
├── main.py                # Main scraping pipeline
├── requirements.txt
└── README.md
```

---

# Technologies Used

## Programming Language

- Python


## Data Processing

- Pandas
- NumPy


## Web Data Collection

- Requests
- REST API interaction


## Development Tools

- Git
- GitHub
- Virtual Environment


---

# Current Pipeline Workflow

```
Divar API
    |
    |
    v

Search Listings
    |
    |
    v

Extract Advertisement Details
    |
    |
    v

Parse JSON Data
    |
    |
    v

Clean Structured Dataset
    |
    |
    v

CSV Dataset
```

---

# Future Roadmap

## Data Analysis

Planned analyses:

- Price distribution analysis
- City comparison
- Neighborhood price ranking
- Correlation analysis
- Statistical hypothesis testing
- Market trend discovery


---

## Machine Learning

Future models:

- House price prediction
- Price anomaly detection
- Fair price estimation
- Recommendation system


Possible algorithms:

- Linear Regression
- Random Forest
- Gradient Boosting
- XGBoost
- Neural Networks


---

## Advanced Features

Future development:

- Interactive dashboard
- Geographic price heatmap
- Real estate recommendation engine
- Market trend forecasting


---

# Important Notes

This project collects publicly available advertisement information for educational and research purposes.

The collected data belongs to the original platform and users who published advertisements.

The project does not store private user information.


---

# Author

Behniash

Data Science / Machine Learning Project

GitHub:

https://github.com/Behniash/RealEstate_Intelligence