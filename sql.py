
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import sqlite3
from flask import g
from flask import Flask, jsonify

app = Flask(__name__)

def connect_db():
    return sqlite3.connect('data.db') #connect to database

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/<int:user_id>', methods=['GET'])
def query(user_id):
	cursor = sqlite3.connect('test.db').cursor()

	# #query
	sql = "select name,stu_id,sex,mz,cla_id,place,ro_id,do_id,date,school,address from myer where stu_id = "+ str(user_id) 
	cursor.execute(sql)
	result = cursor.fetchall()
	print "query has been ok"
	print sql
	cursor.close()
	sqlite3.connect('test.db').close()
	return jsonify(
		{
			'user_id': user_id,
			'name': result[0][0],
			'stu_id': result[0][1],
			'sex': result[0][2],
			'mz': result[0][3],
			'cla_id': result[0][4],
			'place': result[0][5],
			'ro_id': result[0][6],
			'do_id': result[0][7],
			'date': result[0][8],
			'address': result[0][9]
		})

@app.route('/<user_name>', methods=['GET'])
def query_a(user_name):
	cursor = sqlite3.connect('test.db').cursor()

	# #query
	sql = "select name,stu_id,sex,mz,cla_id,place,ro_id,do_id,date,school,address from myer where name = "+ "\""+user_name+"\"" 
	cursor.execute(sql)
	result = cursor.fetchall()
	print "query has been ok"
	print sql
	cursor.close()
	sqlite3.connect('test.db').close()
	return jsonify(
		{
			'name': result[0][0],
			'stu_id': result[0][1],
			'sex': result[0][2],
			'mz': result[0][3],
			'cla_id': result[0][4],
			'place': result[0][5],
			'ro_id': result[0][6],
			'do_id': result[0][7],
			'date': result[0][8],
			'address': result[0][9]
		})

@app.route('/', methods=['GET'])
def home():
  return "11"

@app.route('/ok', methods=['GET'])
def ok():
  return "Hello,World"

@app.errorhandler(404)
def page_not_found(e):
    res = jsonify({'error': 'not found'})
    res.status_code = 404
    return res

if __name__ == '__main__':  
    app.run(host='0.0.0.0')  