#!/usr/bin/python3

from utils.fitatuapi import FitatuApi
from caterers.minutaosiem import MinutaOsiemCaterer
from caterers.dietly import DietlyCaterer
import os

###

def dietplannersync():
    caterer_id = os.getenv("CATERER_ID")
    start_date = os.getenv("START_DATE")
    end_date = os.getenv("END_DATE")

    fitatu_username = os.getenv("FITATU_USERNAME")
    fitatu_password = os.getenv("FITATU_PASSWORD")
    fitatu_activity_plan_id = os.getenv("FITATU_ACTIVITY_PLAN_ID")

    fitatu = FitatuApi()
    fitatu.authorize_session(fitatu_username, fitatu_password)

    if(caterer_id == "MINUTAOSIEM"):
        minutaosiem_username = os.getenv("MINUTAOSIEM_USERNAME")
        minutaosiem_password = os.getenv("MINUTAOSIEM_PASSWORD")
        minutaosiem_diet_id = os.getenv("MINUTAOSIEM_DIET_ID")

        caterer = MinutaOsiemCaterer()
        caterer.authorize_api_session(minutaosiem_username, minutaosiem_password)
        caterer.apply_diet_to_fitatu_by_dates(minutaosiem_diet_id, 
                fitatu, fitatu_activity_plan_id, start_date, end_date)

    if(caterer_id == "DIETLY"):
        dietly_username = os.getenv("DIETLY_USERNAME")
        dietly_password = os.getenv("DIETLY_PASSWORD")
        dietly_company  = os.getenv("DIETLY_COMPANY")
        dietly_order_id = os.getenv("DIETLY_ORDER_ID")

        caterer = DietlyCaterer()
        caterer.authorize_api_session(dietly_username, dietly_password, dietly_company)
        caterer.apply_diet_to_fitatu_by_dates(dietly_order_id, fitatu, 
                fitatu_activity_plan_id, start_date, end_date)


if __name__ == '__main__':
    dietplannersync()

