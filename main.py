from flask import Flask, jsonify, render_template, request
import pyrebase

app = Flask(__name__)

# Configure Firebase
config = {
  'apiKey': "AIzaSyC8pgI3SwgFuWqfoY0Z9JEcWR5SWkWOxhk",
  'authDomain': "dyte-assignment-12a53.firebaseapp.com",
  'databaseURL': "https://dyte-assignment-12a53-default-rtdb.firebaseio.com",
  'projectId': "dyte-assignment-12a53",
  'storageBucket': "dyte-assignment-12a53.appspot.com",
  'messagingSenderId': "73529296950",
  'appId': "1:73529296950:web:7e7042f8536e5a9a777097",
  'measurementId': "G-VMJDQ0590Z"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Route to get error logs
@app.route('/get_logs', methods=['POST', 'GET'])
def get_error_logs():
    # Query the data
    if request.method == 'POST':
        # data = request.get_json()
        
        val = request.form['value']
        option = request.form['option']
        print(val)
        print(option)
        
        if option == "parentResourceId":
            data = db.child("logs").order_by_child("metadata/"+option).equal_to(val).get()
        else:
            data = db.child("logs").order_by_child(option).equal_to(val).get()
            print(data.val())

        # Convert the data to a list
        error_logs = [log.val() for log in data.each()]
        print(error_logs)

        # return jsonify(error_logs)
        return render_template('log_query.html', result = "ok", data = error_logs)
    return render_template('log_query.html')

@app.route('/', methods = ['POST', 'GET'])
def insert_logs():
    if request.method == 'POST':
        data = request.get_json()
        
        # Check if required keys are present
        required_keys = ['level', 'message', 'resourceId', 'timestamp', 'traceId', 'spanId', 'commit', 'metadata']
        for key in required_keys:
            if key not in data:
                raise KeyError(f"Key '{key}' is missing in the JSON data")

        level = data['level']
        message = data['message']
        resourceId = data['resourceId']
        timestamp = data['timestamp']
        traceId = data['traceId']
        spanId = data['spanId']
        commit = data['commit']
        metadata = data['metadata']

        # Access metadata values
        parentResourceId = metadata['parentResourceId']
        
        data_db  = {
            
            "level": level,
            "message": message,
            "resourceId": resourceId,
            "timestamp": timestamp,
            "traceId": traceId,
            "spanId": spanId,
            "commit": commit
            }
        # Add metadata to the pushed data
        meta_data = {
            "parentResourceId": parentResourceId
        }

        # Combine the data and metadata
        data_db["metadata"] = meta_data
                
        # Push data to Firebase
        db.child('logs').push(data_db)
        
        return render_template('insert_log.html', result = "ok")
    
    return render_template('insert_log.html')

@app.route('/multiple_log_query', methods = ['POST', 'GET'])
def multiple_log_query():
    if request.method == 'POST':
        # Initialize an empty list to store tuples
        additional_values = []
        # querys = db.child("logs")

        # Check each parameter in the request.form and add corresponding tuples
        if 'level' in request.form:
            option1 = 'level'
            value1 = request.form['level']
            if value1 != '':
                additional_values.append((option1, value1))
                # querys = querys.order_by_child('level').start_at(value1).end_at(value1)

        if 'message' in request.form:
            option2 = 'message'
            value2 = request.form['message']
            if value2 != '':
                additional_values.append((option2, value2))
                # querys = querys.order_by_child('message').start_at(value2).end_at(value2)

        if 'resourceId' in request.form:
            option3 = 'resourceId'
            value3 = request.form['resourceId']
            if value3 != '':
                additional_values.append((option3, value3))
                # querys = querys.order_by_child('resourceId').start_at(value3).end_at(value3)

        if 'timestamp' in request.form:
            option4 = 'timestamp'
            value4 = request.form['timestamp']
            if value4 != '':
                additional_values.append((option4, value4))
                # querys = querys.order_by_child('timestamp').start_at(value4).end_at(value4)

        if 'traceId' in request.form:
            option5 = 'traceId'
            value5 = request.form['traceId']
            if value5 != '':
                additional_values.append((option5, value5))
                # querys = querys.order_by_child('traceId').start_at(value5).end_at(value5)

        if 'spanId' in request.form:
            option6 = 'spanId'
            value6 = request.form['spanId']
            if value6 != '':
                additional_values.append((option6, value6))
                # querys = querys.order_by_child('spanId').start_at(value6).end_at(value6)

        if 'commit' in request.form:
            option7 = 'commit'
            value7 = request.form['commit']
            if value7 != '':
                additional_values.append((option7, value7))
                # querys = querys.order_by_child('commit').start_at(value7).end_at(value7)

        if 'parentResourceId' in request.form:
            option8 = 'metadata/parentResourceId'
            value8 = request.form['parentResourceId']
            if value8 != '':
                additional_values.append((option8, value8))
                # querys = querys.order_by_child('metadata/parentResourceId').start_at(value8).end_at(value8)

        #Now you can use the additional_values list in your query
        query = db.child("logs")
        
        print(additional_values)

        for child_key, value in additional_values:
            query = query.order_by_child(child_key).start_at(value).end_at(value)

        data = query.get()
        error_logs = [log.val() for log in data.each()]
                            
        return render_template('multiple_log_query.html', result = "ok", data = error_logs)
            
    return render_template('multiple_log_query.html')

if __name__ == '__main__':
    app.run(debug=True, port = 3000)
