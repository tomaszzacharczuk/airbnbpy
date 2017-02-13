import pytest
from numbers import Number
from .core import AirbnbAPI


class ImproperlyConfigured(BaseException):
    pass


class TestAirbnbAPI:
    """
    Because this is not official API and I don't have official documentation to know data structure, I can only check
    if responses from Airbnb have 200 status code.
    """
    def setup_class(cls):
        import json
        with open("credentials.json") as f:
            creds = json.loads(f.read())

        def get_creds(key, credentials=creds):
            try:
                return credentials[key]
            except KeyError:
                error_msg = "Set {} variable in credentials.json".format(key)
                raise ImproperlyConfigured(error_msg)

        api_key = get_creds('api_key')
        cls.username = get_creds('username')
        cls.password = get_creds('password')
        cls.air_api = AirbnbAPI(api_key)
        cls.air_api.login_by_email(cls.username, cls.password)

    # @pytest.mark.skip
    def test_listing_search(self):
        assert self.air_api.listing_search().status_code == 200
        assert self.air_api.listing_search(
            locale="pl", currency="PLN", location="Warszawa").status_code == 200
        assert self.air_api.listing_search(
            location="Los Angeles", locale="en-US", currency="USD", price_max=300, min_bedrooms=2).status_code == 200
        assert self.air_api.listing_search(locale="pl", currency="PLN", location="Kraków").status_code == 200

    # @pytest.mark.skip
    def test_view_listing_info__test_get_reviews(self):
        result_krakow = self.air_api.listing_search(locale="pl", currency="PLN", location="Kraków")
        assert result_krakow.status_code == 200
        self.listing_id = result_krakow.json()['search_results'][0]['listing']['id']
        assert isinstance(self.listing_id, Number)
        assert self.air_api.view_listing_info(self.listing_id).status_code == 200
        assert self.air_api.view_listing_info(self.listing_id, locale="pl", number_of_guests=2).status_code == 200
        assert self.air_api.view_listing_info(self.listing_id, locale="en-US", number_of_guests=1).status_code == 200

        assert self.air_api.get_reviews(self.listing_id).status_code == 200
        assert self.air_api.get_reviews(self.listing_id, _limit=10).status_code == 200
        assert self.air_api.get_reviews(self.listing_id, _limit=5, locale="pl", currency="PLN").status_code == 200

    # @pytest.mark.skip
    def test_get_user_info__test_view_user_info(self):
        user_response = self.air_api.get_user_info()
        assert  user_response.status_code == 200
        self.user_id = user_response.json()['user']['user']['id']

        assert self.air_api.view_user_info(self.user_id).status_code == 200
