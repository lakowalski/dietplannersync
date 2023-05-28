#!/usr/bin/python3

from utils.fitatuapi import FitatuApi
from caterers.minutaosiem import MinutaOsiemCaterer
import os

###

def dietplanersync():
    start_date = os.getenv("START_DATE")
    end_date = os.getenv("END_DATE")

    minutaosiem_username = os.getenv("MINUTAOSIEM_USERNAME")
    minutaosiem_password = os.getenv("MINUTAOSIEM_PASSWORD")
    minutaosiem_diet_id = os.getenv("MINUTAOSIEM_DIET_ID")

    fitatu_username = os.getenv("FITATU_USERNAME")
    fitatu_password = os.getenv("FITATU_PASSWORD")
    fitatu_activity_plan_id = os.getenv("FITATU_ACTIVITY_PLAN_ID")

    ###

    fitatu = FitatuApi()
    fitatu.authorize_session(fitatu_username, fitatu_password)

    caterer = MinutaOsiemCaterer()
    caterer.authorize_api_session(minutaosiem_username, minutaosiem_password)
    caterer.apply_diet_to_fitatu_by_dates(minutaosiem_diet_id, fitatu, 
                                           fitatu_activity_plan_id, start_date, end_date)

if __name__ == '__main__':
    dietplanersync()

