from flask import Flask, app, make_response, jsonify, g

from Database import Database
from CustomMap import CustomMap
from RestaurantDetails import RestaurantDetails
from datetime import datetime

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = Database()
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return "Hack DFW Earth hack"


@app.route('/hackdfw/location/source/<src>/destination/<dest>')
def get_location_polygon(src, dest):
    gmap = CustomMap()
    map = gmap.get_map_polygon(src, dest)
    get_db().put_data([src,dest,datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S'),''])
    pool = get_db().get_data([src,dest,datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S'),''])
    map.update(pool)
    return make_response(jsonify(map))


@app.route('/hackdfw/restaurants/lat/<lat>/long/<long>')
def get_restaurants(lat, long):
    lat = float(lat)
    long = float(long)
    rest = RestaurantDetails()
    return make_response(jsonify(rest.get_business(lat, long)))

@app.route('/hackdfw/addtrip/source/<src>/destination/<dest>/date/<date>/userid/<userid>') #data coming from car pool
def put_user(src,dest,date,userid):
    date=datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
    print date,type(date)
    get_db().put_data([src,dest,date,userid])
    return make_response(jsonify(get_db().get_data([src,dest,date,userid])))

@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({'error': 'Page Not found'}), 404)


@app.errorhandler(500)
def data_not_found(error):
    return make_response(jsonify({'error': 'Data not found'}), 500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
