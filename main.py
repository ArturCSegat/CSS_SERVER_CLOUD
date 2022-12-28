# Ignore the bad flask code, just a simple server cant be bothered to properly implement it
import os
import random
from flask import Flask 
from flask import send_file
import io


app = Flask(__name__)

@app.rout('/')
def home(){
    return "OLa from flask"
}

@app.route("/map/<m>")
def get_map(m):

    def given_map(ma):

        ma += '.bsp'
         
        for b in os.listdir('./maps'):
            if b == ma:
                return f"./maps/{b}"
        
        return 'map not found'
    
    chosen = given_map(m)

    with open(chosen, 'rb') as f:
        bsp_file = f.read()
 
  # send the BSP file as the response
    return send_file(
        io.BytesIO(bsp_file),
        mimetype='application/octet-stream',
        as_attachment=True,
        download_name=chosen
  )


@app.route('/random-map')
def get_bsp():
  # read the BSP file from storage
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