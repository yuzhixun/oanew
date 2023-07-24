from app import app
from app import db

if __name__ == "__main__":
    app.run(debug = True,host='192.168.10.109',port='50000')

