# DietPlannerSync

DietPlannerSync is a simple tool designed to synchronize your diet plans from caterers APIs to the Fitatu diet planner application. 

## Features

- Automatic authorization with both Fitatu and caterers platforms.
- Fetches dish data from the caterer's API.
- Applies fetched dish data to Fitatu for a specific time period.
- Supports custom date ranges for applying the diet.

## Supported caterrers
- Minuta Osiem

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.x
- Fitatu account
- MinutaOsiem caterer account

### Environment Variables

The application uses the following environment variables:

```env
START_DATE = "<START_DATE>"
END_DATE = "<END_DATE>"
MINUTAOSIEM_USERNAME = "<YOUR_MINUTAOSIEM_USERNAME>"
MINUTAOSIEM_PASSWORD = "<YOUR_MINUTAOSIEM_PASSWORD>"
MINUTAOSIEM_DIET_ID = "<DIET_ID>"
FITATU_USERNAME = "<YOUR_FITATU_USERNAME>"
FITATU_PASSWORD = "<YOUR_FITATU_PASSWORD>"
FITATU_ACTIVITY_PLAN_ID = "<YOUR_FITATU_ACTIVITY_PLAN_ID>"
```

### Running DietPlannerSync

To execute the application, run the main.py script with Python:

```bash
python main.py
```

The script will authenticate with both the Fitatu and MinutaOsiem APIs, fetch data about dishes from MinutaOsiem, and apply the data to the specified Fitatu activity plan within the provided date range.

Please remember to replace placeholders such as `<START_DATE>`, `<END_DATE>`, etc. with your actual data.