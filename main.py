# Ignore the bad flask code, just a simple server cant be bothered to properly implement it
import os
import random
from flask import Flask 
from flask import send_file
import io
import requests
import rarfile  as rr
from filehandler import extract_bsp

app = Flask(__name__)

@app.route('/') # just so the home isnt empty
def home():
    return f" list of maps that can be returned:{os.listdir('./maps')}"



#   checks if map is in the current map pool, should b used to determine if it should download the file or
#   just get it from the server
@app.route('/have/<m>') 
def find(m):

    term = m + ".bsp" # m is given as a name, without file extension

    for mp in os.listdir("./maps"):

        if mp == m:
            return "1"
    
    return "0"


#return a map form gamebana
#the global variables are used in the clean up code
@app.route("/map/<id_>/<perm>")
def get_map(id_, perm):

    global save
    save = perm

    map_response_rar = requests.get(f"https://gamebanana.com/dl/{id_}")

    #extract bsp should give just the name, not the path of the file
    global chosen
    chosen  = f"./maps/{extract_bsp(map_response_rar, './maps')}" #extract bsp should give just the name, not the path of the file

 
    with open(chosen, "rb") as f:

        bsp_file = f.read()

  # send the BSP file as the response
    return send_file(
        io.BytesIO(bsp_file),
        mimetype='application/octet-stream',
        as_attachment=True,
        download_name=chosen
  )

@app.teardown_request
def cleanup(exception=None): # if the map is no to be saved delete it

    if save != '1':
        os.remove(chosen)



#returns a rndom map from the map pool
@app.route('/random-map')
def get_bsp():

    def random_map():
        chosen_map = random.choice(os.listdir('./maps'))
        return f"./maps/{chosen_map}"
    
    m = random_map()

    with open(m, 'rb') as f:
        bsp_file = f.read()
 
  # send the BSP file as the response
    return send_file(
        io.BytesIO(bsp_file),
        mimetype='application/octet-stream',
        as_attachment=True,
        download_name=m
  )

if(__name__ == '__main__'):
    app.run()   