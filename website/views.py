from flask import Blueprint,render_template, request, flash, jsonify
from flask_login import login_required, current_user
# from .models import Address
from . import db
import json
import requests
import logging
from datetime import datetime
import ee



views = Blueprint('views', __name__)
logging.basicConfig(level=logging.DEBUG)


@views.route('/', methods=['GET','POST'])
@login_required
def home():
    lat = lon = address = None
    if request.method == 'POST': 
        address = request.form.get('address')


        if len(address) < 1:
            flash('Address is not a real address', category='error') 
        else:
            logging.debug(f"Querying coordinates for address: {address}")

            # exists = Address.query.filter_by(data=address).first()
            # if exists:
            #     flash('Address already exists', category='error')
            # else:
            #     new_address = Address(data=address)  #providing the schema for the note 
            #     db.session.add(new_address) #adding the note to the database 
            #     db.session.commit()


            #     flash('Address found!', category='success')

            coor = find_coor(address)
            if coor:
                logging.debug(f"API Response: {coor}")

                lat = coor[0]['lat']
                lon = coor[0]['lon']

    return render_template("home.html", user=current_user, lat=lat, lon=lon)


def find_coor(address):
    url = f"https://geocode.maps.co/search?q={address}&api_key=66a064443604a154067098cgi1ba4c3"
    response = requests.get(url)
    logging.debug(f"Geocoding API URL: {url}")
    if response.status_code == 200:
        results = response.json()
        return results
    else:
        return None
    



def google_earth():
    ee.Authenticate()
    ee.Initialize(project='boredonline247')
    



    





# api_key = '66a064443604a154067098cgi1ba4c3'
# address = '555 5th Ave New York NY 10017 US'
# location_data = find_coor(address, api_key)
# if location_data:
#     print(location_data)
# else:
#     print("Failed to retrieve data")


    



# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
#     noteId = note['noteId']
#     note = Address.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()

#     return jsonify({})