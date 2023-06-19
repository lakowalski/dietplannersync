import requests
from datetime import datetime
import json
import urllib

API_HOST='panel.dietly.pl'
ORIGIN_HEADER='https://panel.dietly.pl'

###

class DietlyApi:
    _session = None

    def __init__(self):
        self.session = requests.Session() 
        self.session.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded'
        })

    def authorize_session(self, username, password, company_id=None):
        payload=urllib.parse.urlencode({
            "username": username,
            "password": password
        })
        
        if company_id is not None:
            self.set_company_id(company_id)

        self.session.post('https://%s/api/auth/login' % API_HOST, data=payload)

    def set_company_id(self, company_id):
        self._update_headers({
            'company-id': company_id
        })

    def _update_headers(self, headers):
        self.session.headers.update(headers)

    def _get_request(self, path, headers=None):
        return self.session.get('https://%s%s' % (API_HOST, path), headers=headers)

    ###

    def list_active_companies(self):
        resp = self._get_request('/api/profile/accounts')
        result = [ {"id": c['companyName'], "name": c['fullName']} \
            for c in resp.json() ]
        return result

    def list_orders(self):
        resp = self._get_request("/api/company/customer/order/all")
        return resp.json()

    def describe_order(self, order_id):
        resp = self._get_request("/api/company/customer/order/%s" % order_id)
        return resp.json()

    def describe_delivery(self, delivery_id):
        resp = self._get_request("/api/company/general/menus/delivery/%s/new" % delivery_id)
        return resp.json()


class DietlyCaterer:
    _api = None

    def __init__(self):
        self._api = DietlyApi()

    def authorize_api_session(self, *args, **kwargs):
        self._api.authorize_session(*args, **kwargs)
    
    def describe_dishes_in_delivery(self, delivery_id):
        delivery = self._api.describe_delivery(delivery_id)
        items = delivery.get('deliveryMenuMeal')

        dishes = []
        for item in items:
            dishes.append({
                "name": item.get('menuMealName'),
                "mealType": item.get('mealName'),
                "calories": item.get('nutrition').get('calories'),
                "protein": item.get('nutrition').get('protein'),
                "fat": item.get('nutrition').get('fat'),
                "carbohydrates": item.get('nutrition').get('carbohydrate')
            })

        return dishes
    
    def get_bags_by_dates(self, order_id, start_date, end_date=None):
        first = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d') if end_date else first
        
        result = {}
        order = self._api.describe_order(order_id)
        for bag in order.get("deliveries"):
            date = datetime.fromisoformat(bag['date']).replace(tzinfo=None)
            if(first <= date and date <= end):
                key = date.strftime("%Y-%m-%d");
                result[key] = (self.describe_dishes_in_delivery(bag['deliveryId']))
        
        return result

    def apply_dishes_to_fitatu_plan(self, fitatu, fitatu_activity_plan_id, day, dishes):
        meal_name_map = {
            "Śniadanie": "breakfast", 
            "II śniadanie": "second_breakfast", 
            "Obiad": "dinner", 
            "Podwieczorek": "snack",
            "Kolacja": "supper"
        }

        for dish in dishes:
            meal_name = meal_name_map[dish.get('mealType')]
            resp = fitatu.insert_meal(
                fitatu_activity_plan_id, 
                day, 
                meal_name,
                dish.get('name'), 
                dish.get('calories'),
                dish.get('protein'), 
                dish.get('fat'),
                dish.get('carbohydrates')
            )

            print(resp.status_code, resp.text)

    def apply_diet_to_fitatu_by_dates(self, order_id, fitatu, fitatu_activity_plan_id, start_date, end_date):
        bags = self.get_bags_by_dates(order_id, start_date, end_date)
        for (day, dishes) in bags.items():
            self.apply_dishes_to_fitatu_plan(fitatu, fitatu_activity_plan_id, day, dishes)