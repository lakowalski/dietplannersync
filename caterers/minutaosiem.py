import requests
from datetime import datetime
import json

API_HOST='api.minutaosiem.pl'
ORIGIN_HEADER='https://panel.minutaosiem.pl'

###

class MinutaOsiemApi:
    _session = None

    def __init__(self):
        self.session = requests.Session() 
        self.session.headers.update({
            'Content-Type': 'application/json;charset=utf-8',
            'Origin': ORIGIN_HEADER
        })

    def authorize_session(self, username, password):
        payload=json.dumps({
            "username": username,
            "password": password
        })

        resp = self.session.post('https://%s/login_check' % API_HOST, data=payload)
        auth_token = resp.json().get('token')
        self.session.headers.update({"Authorization": "Bearer " + auth_token})

    def _get_request(self, path):
        return self.session.get('https://%s%s' % (API_HOST, path))

    ###

    def list_diets(self):
        resp = self._get_request("/frontend/secure/my-diets?pagination=false")
        return resp.json().get("hydra:member")

    def describe_diet(self, diet_id):
        resp = self._get_request("/frontend/secure/ecommerce-diets/%s/delivery-days" % diet_id)
        return resp.json()

    def describe_bag(self, bag_id):
        resp = self._get_request("/frontend/secure/bags/%s" % bag_id)
        return resp.json()

    def describe_dish(self, bag_id, dish_id):
        resp = self._get_request("/frontend/secure/bags/%s/change-menu-options" % bag_id)
        options = resp.json().get('options')
        dishes = sum([ item.get('dishes') for item in options.values() ], [])
        dish = [i for i in dishes if i['id'] == dish_id][0]
        return dish

    def describe_dishes_in_bag(self, bag_id):
        bag = self.describe_bag(bag_id)
        items = bag.get('items')

        dishes = []
        for item in items:
            if item.get('dish'):
                dish_id = item.get('dish').get('id')
                dish = self.describe_dish(bag_id, dish_id)
                dishes.append({
                    "name": item.get('dish').get('nameForClient'),
                    "mealType": item.get('mealType').get('name'),
                    "calories": dish.get('calories'),
                    "protein": dish.get('protein'),
                    "fat": dish.get('fat'),
                    "carbohydrates":  dish.get('carbohydrates')
                })

        return dishes

class MinutaOsiemCaterer:
    _api = None

    def __init__(self):
        self._api = MinutaOsiemApi()

    def authorize_api_session(self, *args, **kwargs):
        self._api.authorize_session(*args, **kwargs)
    
    def get_diet_bags_by_dates(self, diet_id, start_date, end_date=None):
        first = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d') if end_date else first
        
        result = {}
        bags = self._api.describe_diet(diet_id).get('bags')
        for bag in bags:
            bag_day = datetime.fromisoformat(bag['date']).replace(tzinfo=None)
            if(first <= bag_day and bag_day <= end):
                key = bag_day.strftime("%Y-%m-%d");
                result[key] = (self._api.describe_dishes_in_bag(bag['id']))
        
        return result

    def apply_dishes_to_fitatu_plan(self, fitatu, fitatu_activity_plan_id, day, dishes):
        meal_name_map = {
            "II śniadanie": "second_breakfast", 
            "Lunch": "dinner", 
            "Przekąska": "snack",
            "Lunch Keto ": "dinner", 
            "Przekąska Keto": "snack", 
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

    def apply_diet_to_fitatu_by_dates(self, diet_id, fitatu, fitatu_activity_plan_id, start_date, end_date):
        bags = self.get_diet_bags_by_dates(diet_id, start_date, end_date)
        for (day, dishes) in bags.items():
            self.apply_dishes_to_fitatu_plan(fitatu, fitatu_activity_plan_id, day, dishes)