from app import app,db
import sys,os
if __name__ == '__main__':
    with app.app_context():

        #db.create_all()
        app.config['JSON_AS_ASCII'] = False
        app.run(debug=True,port=80)
