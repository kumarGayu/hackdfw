from flask import Flask, app, make_response, jsonify

from CustomMap import CustomMap
from RestaurantDetails import RestaurantDetails

app = Flask(__name__)


@app.route('/')
def index():
    return "Hack DFW Earth hack"


@app.route('/hackdfw/location/source/<src>/destination/<dest>')
def get_location_polygon(src, dest):
    gmap = CustomMap()
    return make_response(jsonify(gmap.get_map_polygon(src, dest)))


@app.route('/hackdfw/restaurants/lat/<lat>/long/<long>')
def get_restaurants(lat, long):
    lat = float(lat)
    long = float(long)
    rest = RestaurantDetails()
    return make_response(jsonify(rest.get_business(lat, long)))


@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({'error': 'Page Not found'}), 404)


@app.errorhandler(500)
def data_not_found(error):
    return make_response(jsonify({'error': 'Data not found'}), 500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
