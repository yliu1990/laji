
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import sqlite3
from flask import g
from flask import Flask,jsonify
import csv

app = Flask(__name__)

class Record(object):  #object of a record
    def __init__(self,name,property1, value1, property2, value2):
        self.name = name
        self.property1 = property1
        self.value1 = value1
        self.property2 = property2
        self.value2 = value2

class criterias(object): #object of a search criteria
	def __init__(self,name,property1, value1min, value1max, property2, value2min, value2max, dump_res):
        self.name = name
        self.property1 = property1
        self.value1min = value1min
        self.value1max = value1max
        self.property2 = property2
        self.value2min = value2min
        self.value2max = value2max
        self.dump_res = dump_res

    def sql(self): # dump the sql statement based on the search criterias
    	statement = ""
    	criterialist = []
    	if self.name!="":
    		criteria = "Chemical_formula LIKE " + """'%"""+self.name + """%'"""
    		criterialist.append(criteria)
    	if self.property1!="":
    		criteria = "Property_1_name = " +self.property1 + " AND Property_1_value >= " + self.value1min + " AND Property_1_value <= " + self.value1max
    		criterialist.append(criteria)
    	if self.property2!="":
    		criteria = "Property_2_name = " +self.property1 + " AND Property_2_value >= " + self.value2min + " AND Property_2_value <= " + self.value2max
    		criterialist.append(criteria)
    	count = 0
    	for criteria in crterialist
    		statement += criteria
    		count++
    		if count!=len(criterialist):
    			statement += "AND "
    	return statement

def connect_db():
    return sqlite3.connect('data.db') #connect to database

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/<int:user_id>', methods=['POST'])

def postrecord(newrecord)
	cursor = sqlite3.connect('data.db').cursor()
	# # insert to table
	sql = "INSERT INTO data (Chemical_formula, Property_1_name, Property_1_value, Property_2_name , Property_2_value ) VALUES ("str(newrecord.name) + ", "+ str(newrecord.property1) + ", " + str(newrecord.value1),+", "+ str(newrecord.property2) + ", "+str(newrecord.value2)+")" 
	cursor.execute(sql)
	result = cursor.fetchall()
	print "Insert successful!"
	cursor.close()
	sqlite3.connect('data.db').close()



@app.route('/<int:user_id>', methods=['GET'])
def query(search):    # query based on input search criterias
	cursor = sqlite3.connect('data.db').cursor()

	# #query
	sql = "SELECT * FROM data WHERE " + search.sql()
	cursor.execute(sql)
	result = cursor.fetchall()
	print "Query successful!"
	print sql
	cursor.close()
	sqlite3.connect('data.db').close()
	if search.dump_res==True:    #if chosen to dump the search result
		with open('Lastquery.csv', 'w', newline='') as f_handle:
    	writer = csv.writer(f_handle)
    	header = ['Chemical formula', 'Property 1 name', 'Property 1 value', 'Property 2 name' , 'Property 2 value']
    	writer.writerow(header)
    	for row in result:
        	writer.writerow(row)


@app.errorhandler(404)  
def page_not_found(e):   #error handler
    res = jsonify({'error': 'not found'})
    res.status_code = 404
    return res

if __name__ == '__main__':  
    app.run(host='0.0.0.0')  