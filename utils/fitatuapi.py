import requests
import json
import uuid

API_HOST = 'pl-pl.fitatu.com'
ORIGIN_HEADER = 'https://www.fitatu.com/'
API_SECRET = 'PYRXtfs88UDJMuCCrNpLV'
API_KEY = 'FITATU-MOBILE-APP'

###

class FitatuApi:
    _session = None

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json;charset=utf-8',
            'API-Key': API_KEY,
            'API-Secret': API_SECRET,
            'Origin': ORIGIN_HEADER
        })


    def authorize_session(self, username, password):
        payload = json.dumps({
            "_username": username,
            "_password": password
        })

        resp = self.session.post('https://%s/api/login' % API_HOST, data=payload)
        auth_token = resp.json().get('token')

        self.session.headers.update({"Authorization": "Bearer " + auth_token})

    def _get_request(self, path):
        return self.session.get('https://%s%s' % (API_HOST, path))


    def _post_request(self, path, payload):
        return self.session.post('https://%s%s' % (API_HOST, path), data=json.dumps(payload))

    # day in format: YYYY-MM-DD
    # meal_name: breakfast | second_breakfast | dinner | snack | supper
    def insert_meal(self, activity_plan_id, day, meal_name, dish_name, energy, protein, fat, carbohydrate):
        payload = {
            day: {
                "dietPlan": {
                    meal_name: {
                        "items": [
                            {
                                "carbohydrate": carbohydrate,
                                "eaten": False,
                                "energy": energy,
                                "fat": fat,
                                "foodType": "CUSTOM_ITEM",
                                "ingredientsServing": None,
                                "mealNumber": None,
                                "measureId": 39,
                                "measureQuantity": 1,
                                "name": dish_name,
                                "numberOfMeals": None,
                                "planDayDietItemId": str(uuid.uuid1()),
                                "protein": protein,
                                "source": "API"
                            }
                        ]
                    }
                }
            }
        }
        resp = self._post_request("/api/diet-plan/%s/days" % activity_plan_id, payload)
        return resp
