# DietPlannerSync

DietPlannerSync is a simple tool designed to synchronize your diet plans from caterers APIs to the Fitatu diet planner application. 

## Features

- Automatic authorization with both Fitatu and caterers platforms.
- Fetches dish data from the caterer's API.
- Applies fetched dish data to Fitatu for a specific time period.
- Supports custom date ranges for applying the diet.

## Supported caterrers
- Minuta Osiem
- Dietly.pl

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.x
- Fitatu account
- Minuta Osiem or Dietly.pl account

### Environment Variables

The application uses the following environment variables:

```env
START_DATE = "<START_DATE>"
END_DATE = "<END_DATE>"
FITATU_USERNAME = "<YOUR_FITATU_USERNAME>"
FITATU_PASSWORD = "<YOUR_FITATU_PASSWORD>"
FITATU_ACTIVITY_PLAN_ID = "<YOUR_FITATU_ACTIVITY_PLAN_ID>"
```

Minuta Osiem parameters:
```env
CATERER = "MINUTAOSIEM"
MINUTAOSIEM_USERNAME = "<YOUR_MINUTAOSIEM_USERNAME>"
MINUTAOSIEM_PASSWORD = "<YOUR_MINUTAOSIEM_PASSWORD>"
MINUTAOSIEM_DIET_ID = "<DIET_ID>"
```

Dietly.pl parameters:
```env
CATERER = "DIETLY"
DIETLY_USERNAME = "<YOUR_MINUTAOSIEM_USERNAME>"
DIETLY_PASSWORD = "<YOUR_MINUTAOSIEM_PASSWORD>"
DIETLY_COMPANY = "<YOUR_DIETLY_COMPANY_ID>"
DIETLY_ORDER_ID = "<YOUR_DIETLY_ORDER_ID>"
```

### Running DietPlannerSync

To execute the application, run the main.py script with Python:

```bash
python main.py
```

The script will authenticate with both the Fitatu and Carerer's APIs, fetch data about dishes, and apply the data to the specified Fitatu activity plan within the provided date range.

Please remember to replace placeholders such as `<START_DATE>`, `<END_DATE>`, etc. with your actual data.