from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
   return 'Hello World'

@app.route('/hello', methods=['GET', 'POST'])
def hello():

    # POST request
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        return 'OK', 200

    # GET request
    else:
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message) 

@app.route('/test')
def test_page():
    # look inside `templates` and serve `index.html`
    return "render_template('data_app/public/index.html')"

if __name__ == '__main__':
   app.run()
