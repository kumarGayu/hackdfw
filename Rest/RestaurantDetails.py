from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

conf = {
    'searchKey' : 'Organic Restaurants',
    'limit_of_restaurants' : 15
}

auth = Oauth1Authenticator(
    consumer_key="JQsapxqB9NR5vpKlF3_asA",
    consumer_secret="_o6hyZ36EybYeOXvN_GpeKvaHao",
    token="NfHIlIFEE4FfPTG5_tKgNbKFLJultGuk",
    token_secret="tI0eKpD-_N1dR1vNKBX-wDpLSd0"
)

class RestaurantDetails:
    def __init__(self):
        self.client = Client(auth)

    def get_business(self, lat,long):
        res = {'result':[]}
        businesses = self.rest_search(lat,long).businesses
        for b in businesses:
            res_details={}
            res_details['name'] = b.name
            res_details['location'] = [b.location.coordinate.latitude, b.location.coordinate.longitude]
            res_details['rating'] = b.rating
            res['result'].append(res_details)
        return res

    def rest_search(self, lat, long):
        params = {
            'limit' : conf['limit_of_restaurants'],
            'term' : conf['searchKey'],
            'radius_filter' : 800 #for 5 miles
        }

        return self.client.search_by_coordinates(lat, long, **params)
if __name__ == '__main__':
    client = RestaurantDetails()
    print len(client.get_business(33.004092, -96.970428))
    print client.get_business(33.004092, -96.970428)