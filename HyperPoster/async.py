from flask import Flask, request
import time
import threading
app = Flask(__name__)
@app.route('/start_task', methods=['POST'])
def start_task():
    data = request.get_json()
    def long_running_task(**kwargs):
        your_params = kwargs.get('post_data', {})
        print("Starting long task")
        print("Your params:", your_params)
        for _ in range(10):
            time.sleep(1)
            print(".")
    thread = threading.Thread(target=long_running_task, kwargs={
                    'post_data': data})
    thread.start()
    return {"message": "Accepted"}, 202
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
    
    
    
#curl -X POST -H “Content-Type: application/json” http://localhost:5000/start_task -d ‘{“a”:”b”}’
