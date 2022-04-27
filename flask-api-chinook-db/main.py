#pip install flask
#pip install flask-session

'''
Goal: flesh out an API for the chinook music store.

# Basic Requirements
* Expose an endpoint for searching for music:
    * by name (implemented)
    * by artis(implemented)
    * by genre (implemented)
    * by year (implemented)
    * by album (implemented)
* Be able to add tracks to a "shopping cart"
    * We need to be able to add, remove, and clear a cart (implemented)
* Be able to "check out"
    * Convert the current shopping cart into an invoice in the DB (implemented)
        *This will also create one or more invoice items

# Additional Requirements (options, do what you find interesting)
* Implement user authentication (e.g. user name = customer email and password = phone number)
    * Before you can check out, the user must be logged in first
* Develop an HTML front-end for this application

# As always...
* If you want to do something completely different go ahead!  Just make sure it's
  as complex as what I've outlined above.

# Things to cover:
    * Templating with Jinja
    * Inserting records into the database
'''

from flask import Flask, jsonify, request, session, render_template
import database
import os
import sqlite3
import json

app = Flask(__name__)
app.secret_key = "super secret key"
app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True

def return_as_json(associative_array):
    json_data = [dict(ix) for ix in associative_array]
    return jsonify(json_data)

#base route (home page)
@app.route('/')
def home():
    return '<h1>Hello, World!</h1>'

@app.route('/about')
def about():
    return '<h1>About Me</h1><p>My name is Teddy and I am a CS student at HSU</p>'

# runs the query to display all tracks
@app.route('/tracks')
def get_all_tracks():
    result = database.run_query("SELECT * FROM tracks")
    return return_as_json(result)

@app.route('/tracks/html')
def get_all_tracks_html():
    result = database.run_query("SELECT * FROM tracks")
    return render_template("all_tracks.html", data=result)

# locates the tracks by name
@app.route('/tracks/byName/<search_string>')
def search_tracks(search_string):
    sql = "SELECT * FROM tracks WHERE instr(Name, ?)>0"
    params = (search_string, )
    result = database.run_query(sql, params)
    return return_as_json(result)

# locates the tracks by artist
@app.route('/tracks/byArtist/<search_string>')
def search_tracks_artist(search_string):
    sq1 = "SELECT * FROM tracks WHERE instr(Composer, ?)>0"
    params = (search_string, )
    result = database.run_query(sq1, params)
    return return_as_json(result)

# locates the tracks by genre
@app.route('/tracks/byGenre/<search_string>')
def search_tracks_genre(search_string):
    sq1 = "SELECT * FROM tracks WHERE instr(GenreId, ?)>0"
    params = (search_string, )
    result = database.run_query(sq1, params)
    return return_as_json(result)

# locates tracks by year
@app.route('/tracks/byYear/<search_string>')
def search_tracks_year(search_string):
    sq1 = "SELECT * FROM tracks WHERE instr(Name, ?)>0"
    params = (search_string, )
    result = database.run_query(sq1, params)
    return return_as_json(result)

# locates tracks by album
@app.route('/tracks/byAlbum/<search_string>')
def search_tracks_album(seach_string):
    sq1 = "SELECT * FROM tracks WHERE instr(AlbumId, ?)>0"
    params = (search_string, )
    result = database.run_query(sq1, params)
    return return_as_json(result)

# add items to shopping cart
@app.route('cart/add/<search_string>', methods=['POST'])
def add_to_cart(search_string):
    sq1 = """INSERT INTO cart 
             SELECT Name, TrackId, UnitPrice
             From tracks
             WHERE INSTR(TrackId, ?)>0
             LIMIT 1
          """
    params = (search_string, )
    result = database.run_insert(sq1, params)
    return jsonify({'result': result})

# deletes items from shopping cart
@app.route('/cart/delete/<search_string>', methods=['DELETE'])
def remove_from_cart(search_string):
    sq1 = """DELETE FROM cart
             WHERE TrackId = ?
          """
    params = (search_string, )
    result = database.run_delete(sq1, params)
    return jsonify({'result', result})

# clears out all of the items in the shopping cart
@app.route('/cart/clear', methods=['DELETE'])
def clear_cart(search_string):
    sq1 = "DELETE FROM cart"
    result = database.run_clear(sq1)
    return jsonify({'result', result})

# checking out
@app.route('/cart/checkout/<search_string>', methods=['GET', 'POST']) 
def checkout(search_string):
    # if session['logged_in'] == False:
    #     abort(777, description="Not logged in.")
    
    total = database.run_total("""SELECT 
                                    SUM(UnitPrice)
                                  FROM 
                                    cart""")
    sql = """INSERT INTO invoices (
                        CustomerId,
                        InvoiceDate,
                        BillingAddress,
                        BillingCity,
                        BillingState,
                        BillingCountry,
                        BillingPostalCode,
                        Total)
                        VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)"""
    params = (request.values['CustomerId'], 
              request.values['InvoiceDate'], 
              request.values['BillingAddress'], 
              request.values['BillingCity'],
              request.values['BillingState'],
              request.values['BillingCountry'],
              request.values['BillingPostalCode'],
              total)
              
    database.run_insert(sql, params)

    sql2 = "SELECT * FROM invoices WHERE CustomerId = ?"
    params2 = (search_string, )
    result = database.run_query(sql2, params2)
    return return_as_json(result)

# building the login
@app.route('/login', methods=['GET', 'POST'])
def login():
    session['logged_in'] = False

    #request.method determines route type
    if request.method == 'POST':
        
        #request.values contains a dictionary of variables sent to the server
        if request.values['user_name'] == 'user' and request.values['password'] == 'password':

            #remember log in state through session
            session['logged_in'] = True
            return jsonify({'logged_in': session['logged_in'] })

        else:
            session['logged_in'] = False
            return jsonify({'logged_in': session['logged_in']})
    else:
        return jsonify({'logged_in': session['logged_in']})

@app.route('/customer', methods=['POST'])
def create_customer():
    sql = """INSERT INTO customers (
                          FirstName,
                          LastName,
                          Company,
                          Address,
                          City,
                          State,
                          Country,
                          PostalCode,
                          Phone,
                          Fax,
                          Email,
                          SupportRepId
                      )
                      VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)"""
    params = (request.values['FirstName'], 
              request.values['LastName'], 
              request.values['Company'], 
              request.values['Address'],
              request.values['City'],
              request.values['State'],
              request.values['Country'],
              request.values['PostalCode'],
              request.values['Phone'],
              request.values['Fax'],
              request.values['Email']
              )
    result = database.run_insert(sql, params)
    return jsonify({'result': result })
    