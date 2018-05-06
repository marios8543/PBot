from flask import Flask
import mysql.connector

app = Flask(__name__)
conn = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='pbot')
db = conn.cursor(buffered=True)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/auth/<token>', methods=['GET'])
def authorize(token):
    db.execute("SELECT valid FROM setting_sessions WHERE token="+str(token))
    print('Attempting to verify token '+token)
    valid = db.fetchall[0][0]
    if valid == 1:
        redirect = redirect('/dashboard.html')
        response = app.make_response(redirect)
        response.set_cookie('token',value=token,max_age=43200)
        return response

app.run(debug=True, port=3000)
